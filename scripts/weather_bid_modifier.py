#!/usr/bin/env python3
"""
Kozbeyli Konağı — Hava Durumu & Etkinlik Bazlı Dinamik Teklif Motoru
(God Tier / Dynamic Bidding)

Amaç: İzmir/Foça'da hava durumunun iyi olduğu veya yaklaşan bir etkinlik 
(Örn. Foça Ot Festivali) olduğu günlerde reklamlara otomatik "bid modifier" eklemek.

Kullanım:
    python3 scripts/weather_bid_modifier.py
"""

import json
import random
import sys
from pathlib import Path

# Add project root to sys.path to import kads
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))
from kads import core

def fetch_foca_weather():
    """Simüle edilmiş hava durumu (Gerçekte OpenWeatherMap vb. API'den alınır)"""
    conditions = ["Güneşli", "Parçalı Bulutlu", "Yağmurlu", "Rüzgarlı"]
    return {
        "temp_c": random.randint(15, 35),
        "condition": random.choice(conditions)
    }

def calculate_bid_modifier(weather_data) -> float:
    modifier = 1.0
    if weather_data["temp_c"] > 25 and weather_data["condition"] == "Güneşli":
        modifier = 1.30  # %30 artır (İnsanlar Foça'ya kaçmak ister)
    elif weather_data["condition"] == "Yağmurlu":
        modifier = 0.80  # %20 azalt
    return modifier

def main():
    print("--- Dinamik Bidding Motoru Çalışıyor ---")
    weather = fetch_foca_weather()
    print(f"Foça Anlık Durum: {weather['temp_c']}°C, {weather['condition']}")
    
    bid_modifier = calculate_bid_modifier(weather)
    
    change_payload = {
        "action": "update_bid_modifier",
        "entity": "campaign",
        "location": "İzmir, Foça",
        "bid_modifier": bid_modifier,
        "reason": f"Hava durumu tetikleyicisi: {weather['temp_c']}°C {weather['condition']}"
    }
    
    print(f"\nÖnerilen Değişiklik:\n{json.dumps(change_payload, indent=2, ensure_ascii=False)}")
    print("\nBu değişikliği uygulamak için 'change.json' olarak kaydedip 'kads guard' üzerinden geçirin.")

if __name__ == "__main__":
    main()
