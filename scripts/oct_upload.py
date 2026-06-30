#!/usr/bin/env python3
"""
Kozbeyli Konağı — Google Ads Offline Conversion Tracking (OCT)
(God Tier / Value-Based Bidding)

Amaç: Sadece web sitesindeki form doldurmalarını (lead) değil, o lead'in
ne kadarlık bir rezervasyona dönüştüğünü (gerçek ciro) Google'a geri göndermek.
Böylece Google Algoritması (PMax/Search) "en çok form dolduranı" değil,
"en çok para harcayacak VIP müşteriyi" bulmaya odaklanır.

Kullanım:
    python3 scripts/oct_upload.py --gclid "TesT_GcLid_123" --value 25000
"""

import argparse
import datetime
import json
import os
import sys
from pathlib import Path

# Add project root to sys.path to import kads
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))
from kads import core


def main():
    parser = argparse.ArgumentParser(description="Google OCT Sync")
    parser.add_argument("--gclid", required=True, help="Google Click ID (GCLID)")
    parser.add_argument(
        "--value", required=True, type=float, help="Gerçekleşen Ciro (TRY)"
    )
    args = parser.parse_args()

    env = core.load_env()
    customer_id = env.get("GOOGLE_ADS_CUSTOMER_ID", "EKSİK_ID")

    if customer_id == "EKSİK_ID":
        print("HATA: GOOGLE_ADS_CUSTOMER_ID eksik (.env kontrol et).")
        return

    conversion_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S+00:00")

    # OCT Payload (Örnek Yapı)
    payload = {
        "customer_id": customer_id,
        "conversions": [
            {
                "gclid": args.gclid,
                "conversion_action": "Offline_Rezervasyon",
                "conversion_date_time": conversion_time,
                "conversion_value": args.value,
                "currency_code": "TRY",
            }
        ],
    }

    print("--- Google Offline Conversion Tracking (OCT) Başlıyor ---")
    print(f"Hedef Hesap: {customer_id}")
    print(f"Yüklenen Veri: {json.dumps(payload, indent=2)}")
    print("\n[Simülasyon - API Bağlantısı (google-ads kütüphanesi) bekleniyor]")
    print("Durum: HAZIR (Value-Based Bidding için ciro verisi hazırlandı)")


if __name__ == "__main__":
    main()
