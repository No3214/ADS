#!/usr/bin/env python3
"""
kads.seo — Yerel SEO + Google İşletme Profili (GBP) modülü.

Amaç: "kozbeyli", "kozbeyli konağı", "foça butik otel" gibi aramalarda ve
Haritalar'da görünürlüğü maksimize etmek. Dürüst çerçeve: MARKALI aramada
("Kozbeyli Konağı") ilk sırada çıkmak çok ulaşılabilir; jenerik organik #1
hiç kimse tarafından GARANTİ edilemez. Bu modül bunu maksimize eden eksiksiz
paketi üretir: geçerli LodgingBusiness JSON-LD şeması, GBP optimizasyon
kontrol listesi, NAP/atıf listesi ve markalı arama hâkimiyeti taktikleri.

Çıktılar (out/seo/ veya seo/):
  schema-lodgingbusiness.jsonld   Siteye gömülecek geçerli Hotel şeması
  gbp-kontrol-listesi.csv         Google İşletme Profili eksiksizlik denetimi
  nap-atif-listesi.csv            Tutarlı NAP için dizin/OTA atıfları
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

from kads import data

# ---- SEO-ozel dogrulanmis veri (web arastirmasi, Haziran 2026) -------------
SEO = {
    "name": "Kozbeyli Konağı",
    "legal_note": "Aile işletmesi taş otel & restoran (hizmette: 2013'ten beri)",
    "url": "https://www.kozbeylikonagi.com.tr/",
    "alt_url": "https://www.kozbeylikonagi.com/",
    "phone": "+905322342686",            # +90 532 234 2686
    "street": "Kozbeyli Köyü, Küme Evler No:188",
    "locality": "Foça", "region": "İzmir", "postal": "35680", "country": "TR",
    "lat": 38.7145, "lon": 26.8942,       # Kozbeyli köyü; GBP pini ile DOĞRULA
    "maps_note": "Kesin pini Google İşletme Profili'ndeki konumla doğrula.",
    "price_range": "₺₺",
    "rooms": 16,
    "checkin": "14:00", "checkout": "12:00",
    "languages": ["tr", "en"],
    "sameas": [
        "https://www.instagram.com/kozbeylikonagi/",
        "https://www.facebook.com/kozbeylikonagi/",
        "https://www.kozbeylikonagi.com/",
    ],
    "amenities": [
        "Ücretsiz Wi-Fi", "Ücretsiz otopark", "Organik kahvaltı", "Restoran",
        "Çatı terası", "Klima", "Evcil hayvan dostu", "Deniz/doğa manzarası",
        "Aile odaları", "Etkinlik alanı (200 kişi)",
    ],
}


def schema_jsonld() -> dict:
    """Geçerli schema.org Hotel (LodgingBusiness) JSON-LD. SAHTE puan YOK —
    aggregateRating bilerek eklenmez (Google sahte yorum işaretlemesini cezalandırır;
    gerçek yorum verisi varsa GBP üzerinden gelir)."""
    s = SEO
    return {
        "@context": "https://schema.org",
        "@type": "Hotel",
        "name": s["name"],
        "description": (
            "600 yıllık Kozbeyli köyünde Osmanlı taş mimarisiyle restore edilmiş "
            "butik otel ve restoran. 16 oda, organik köy kahvaltısı, çatı terasında "
            "Ege manzarası, Antakya–Ege mutfağı. Evcil hayvan dostu. Foça'ya 13 km."
        ),
        "url": s["url"],
        "telephone": s["phone"],
        "priceRange": s["price_range"],
        "currenciesAccepted": "TRY",
        "petsAllowed": True,
        "numberOfRooms": s["rooms"],
        "checkinTime": s["checkin"],
        "checkoutTime": s["checkout"],
        "image": [
            s["url"] + "img/konak.jpg",
            s["url"] + "img/oda.jpg",
            s["url"] + "img/kahvalti.jpg",
        ],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": s["street"],
            "addressLocality": s["locality"],
            "addressRegion": s["region"],
            "postalCode": s["postal"],
            "addressCountry": s["country"],
        },
        "geo": {"@type": "GeoCoordinates", "latitude": s["lat"], "longitude": s["lon"]},
        "hasMap": f"https://www.google.com/maps/search/?api=1&query={s['lat']},{s['lon']}",
        "availableLanguage": s["languages"],
        "amenityFeature": [
            {"@type": "LocationFeatureSpecification", "name": a, "value": True}
            for a in s["amenities"]
        ],
        "sameAs": s["sameas"],
        "potentialAction": {
            "@type": "ReserveAction",
            "target": {
                "@type": "EntryPoint",
                "urlTemplate": s["url"] + "rezervasyon",
                "actionPlatform": [
                    "http://schema.org/DesktopWebPlatform",
                    "http://schema.org/MobileWebPlatform",
                ],
            },
            "result": {"@type": "LodgingReservation", "name": "Doğrudan Rezervasyon"},
        },
    }


# ---- GBP optimizasyon kontrol listesi --------------------------------------
GBP_CHECKLIST = [
    ("Doğrulama", "İşletme sahipliği doğrulanmış (kart/telefon/video)", "Kritik"),
    ("İsim", "Tam olarak 'Kozbeyli Konağı' (anahtar kelime doldurma YOK)", "Kritik"),
    ("Birincil kategori", "Otel (Hotel)", "Kritik"),
    ("Ek kategoriler", "Restoran; Düğün/etkinlik mekânı; Kahvaltı yeri", "Yüksek"),
    ("NAP", "Ad-Adres-Telefon site + tüm dizinlerle BİREBİR aynı", "Kritik"),
    ("Adres/pin", "Harita pini gerçek konuma tam oturuyor (No:188)", "Kritik"),
    ("Telefon", "+90 532 234 2686 (yerel + tutarlı)", "Yüksek"),
    ("Web sitesi", "kozbeylikonagi.com.tr (UTM ile izlenebilir)", "Yüksek"),
    ("Rezervasyon linki", "Doğrudan hmshotel.net rezervasyon bağlantısı eklendi", "Yüksek"),
    ("Çalışma saatleri", "7/24 resepsiyon / sezon saatleri güncel", "Orta"),
    ("Öznitelikler", "Evcil dostu, ücretsiz Wi-Fi, ücretsiz otopark, kahvaltı, erişilebilirlik", "Yüksek"),
    ("Fotoğraflar", "Cephe, odalar, kahvaltı, teras, restoran, logo, kapak — min 25 görsel", "Yüksek"),
    ("Video", "Kısa konak/oda turu (15-30 sn)", "Orta"),
    ("Açıklama", "750 karakter, USP'ler + Foça/Kozbeyli + doğal anahtar kelimeler", "Yüksek"),
    ("Ürün/Hizmet", "Oda tipleri (Standart/Superior/Aile) + restoran + etkinlik", "Orta"),
    ("Google Posts", "Haftalık post (teklif/etkinlik/sezon)", "Orta"),
    ("Soru-Cevap", "Sık sorulanları kendin sor + yanıtla (evcil, otopark, kahvaltı)", "Orta"),
    ("Yorumlar", "Her misafirden iste; TÜMÜNE 48 saatte yanıt ver", "Kritik"),
    ("Mesajlaşma", "GBP mesajlaşma açık + hızlı yanıt", "Orta"),
    ("Spam", "Rakip/sahte listeleme veya yinelenen pin yok (Maps'te temizlik)", "Orta"),
]

# ---- NAP / atif (citation) listesi -----------------------------------------
CITATIONS = [
    ("Google İşletme Profili", "Kritik", "Birincil yerel sinyal — Maps + yerel paket"),
    ("Apple Maps Connect", "Yüksek", "iOS Haritalar görünürlüğü"),
    ("Yandex Haritalar", "Yüksek", "TR'de yaygın; işletme kaydı"),
    ("Bing Places", "Orta", "Bing/Copilot görünürlüğü"),
    ("Foursquare", "Orta", "Atıf sinyali"),
    ("TripAdvisor", "Yüksek", "Otel + yorum otoritesi (Top 10 ödülü vurgula)"),
    ("trivago", "Orta", "Meta-arama görünürlüğü"),
    ("Booking.com", "Orta", "OTA; markayı koru, direkt'e yönlendir"),
    ("Hotels.com", "Orta", "OTA atıfı"),
    ("neredekal / obilet / etstur", "Orta", "TR OTA atıfları; NAP tutarlı"),
    ("Facebook Sayfası", "Yüksek", "NAP + sameAs sinyali"),
    ("Instagram (@kozbeylikonagi)", "Yüksek", "Marka + bio'da site linki"),
]

# ---- Markali arama hakimiyeti taktikleri -----------------------------------
BRAND_DOMINATION = [
    ("Organik (kozbeyli konağı)", "Ana sayfa <title> ve H1 = 'Kozbeyli Konağı'; marka şeması; hız.",
     "Markalı sorguda #1 çok ulaşılabilir"),
    ("Maps (kozbeyli / kozbeyli konağı)", "Eksiksiz GBP + yorum + foto + pin doğru.",
     "Yerel pakette/Maps'te üst sıra"),
    ("Paid savunma (kozbeyli konağı, kozbeyli otel)", "Marka Search kampanyası (kads build google).",
     "Paid'de en üst; OTA savunması"),
    ("Bare 'kozbeyli'", "Köy adı = bilgi niyeti (Vikipedi/gezi). GBP + Maps + marka içerik ile yan-yana çık.",
     "Tam organik #1 GARANTİ DEĞİL; GBP + ad ile kapsa"),
    ("İçerik", "Blog: Kozbeyli köyü rehberi, Foça gezi, köy kahvaltısı — marka otoritesi.",
     "Uzun kuyruk + marka güçlenir"),
    ("Şema/zengin sonuç", "LodgingBusiness JSON-LD + sitelink; SERP alanını büyüt.",
     "Tıklama oranı artar"),
]


def gbp_rows() -> list[dict]:
    return [{"alan": a, "yapılacak": b, "öncelik": c} for a, b, c in GBP_CHECKLIST]


def citation_rows() -> list[dict]:
    return [{"platform": a, "öncelik": b, "not": c} for a, b, c in CITATIONS]


def brand_rows() -> list[dict]:
    return [{"yüzey": a, "taktik": b, "beklenti": c} for a, b, c in BRAND_DOMINATION]


def build(out_dir: Path) -> list[tuple[str, int]]:
    out_dir.mkdir(parents=True, exist_ok=True)
    schema = schema_jsonld()
    (out_dir / "schema-lodgingbusiness.jsonld").write_text(
        json.dumps(schema, ensure_ascii=False, indent=2), encoding="utf-8")

    def _csv(path, rows):
        with path.open("w", encoding="utf-8-sig", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            w.writeheader(); w.writerows(rows)
        return len(rows)

    return [
        ("schema-lodgingbusiness.jsonld", len(json.dumps(schema))),
        ("gbp-kontrol-listesi.csv", _csv(out_dir / "gbp-kontrol-listesi.csv", gbp_rows())),
        ("nap-atif-listesi.csv", _csv(out_dir / "nap-atif-listesi.csv", citation_rows())),
        ("marka-hakimiyeti.csv", _csv(out_dir / "marka-hakimiyeti.csv", brand_rows())),
    ]
