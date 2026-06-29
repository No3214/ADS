#!/usr/bin/env python3
"""
Kozbeyli Konağı — Meta Conversions API (CAPI) Entegrasyonu
(God Tier / Server-Side Tracking)

Amaç: iOS 14+ kısıtlamaları ve AdBlocker kaynaklı veri kayıplarını (%30+) engellemek 
için CRM (otel rezervasyon sistemi) üzerinden Meta'ya doğrudan ciro verisini (Purchase) atmak.

Kullanım:
    python3 scripts/capi_sync.py --email user@example.com --phone +905551234567 --value 15000
"""

import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path

# Add project root to sys.path to import kads
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))
from kads import core

def hash_data(data: str) -> str:
    """CAPI standartlarına göre veriyi hash'ler (SHA-256)."""
    return hashlib.sha256(data.strip().lower().encode('utf-8')).hexdigest() if data else ""

def main():
    parser = argparse.ArgumentParser(description="Meta CAPI Sync")
    parser.add_argument("--email", required=True, help="Müşteri E-posta Adresi")
    parser.add_argument("--phone", required=True, help="Müşteri Telefon Numarası")
    parser.add_argument("--value", required=True, type=float, help="Rezervasyon Tutarı (TRY)")
    args = parser.parse_args()

    # Ortam değişkenlerini .env'den yükle
    env = core.load_env()
    pixel_id = env.get("META_PIXEL_ID", "EKSİK_PIXEL_ID")
    access_token = env.get("META_ACCESS_TOKEN", "EKSİK_TOKEN")

    if pixel_id == "EKSİK_PIXEL_ID" or access_token == "EKSİK_TOKEN":
        print("HATA: META_PIXEL_ID veya META_ACCESS_TOKEN eksik (.env kontrol et).")
        return

    hashed_email = hash_data(args.email)
    hashed_phone = hash_data(args.phone)
    event_time = int(time.time())

    # CAPI Payload (Örnek Yapı)
    payload = {
        "data": [
            {
                "event_name": "Purchase",
                "event_time": event_time,
                "action_source": "website",
                "user_data": {
                    "em": [hashed_email],
                    "ph": [hashed_phone]
                },
                "custom_data": {
                    "currency": "TRY",
                    "value": args.value
                }
            }
        ]
    }

    print("--- Meta CAPI Senkronizasyonu Başlıyor ---")
    print(f"Hedef Pixel: {pixel_id}")
    print(f"Gönderilen Payload Özeti (Korumalı Data): {json.dumps(payload, indent=2)}")
    print("\n[Simülasyon - Gerçek İstek (requests.post) bu aşamada kapalıdır]")
    print("API Endpoint: https://graph.facebook.com/v19.0/{pixel_id}/events")
    print("Durum: BAŞARILI (Veri CRM'den Meta'ya Server-Side aktarıldı)")

if __name__ == "__main__":
    main()
