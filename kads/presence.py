#!/usr/bin/env python3
"""
kads.presence — Dijital varlik denetimi (docs/09) yapilandirilmis veri + komut.

"Tum online varligimizi gorup duzenleyelim, hata/eksik/gelistirme alanlarini
gorelim" isteginin calisir hali. Denetim bulgularini tek yerden tutar; `kads
presence` ile listeler, kontrol-merkezi panosu bunu okur. Kaynak: docs/09.
"""

from __future__ import annotations

# Mulk envanteri (durum + en kritik bulgu)
PROPERTIES = [
    {
        "mülk": "kozbeylikonagi.com",
        "tür": "Web (ana)",
        "durum": "GÜÇLÜ",
        "bulgu": "Gerçek site; JSON-LD VAR (Haz 2026 web-reach: PostalAddress+Geo+amenity) — Hotel/Restaurant/FAQ tamlığını doğrula; hreflang/cross-domain",
        "öncelik": "Yüksek",
    },
    {
        "mülk": "kozbeylikonagiotel.com",
        "tür": "Web (parazit)",
        "durum": "MUHT. ÖLÜ",
        "bulgu": "Haz 2026 web-reach: domain DNS'te ÇÖZÜLMÜYOR (muhtemelen kaldırıldı); Google listing/GBP'de kalan yanlış no (0232 218 2109) temizle",
        "öncelik": "Yüksek",
    },
    {
        "mülk": "hmshotel.net (booking)",
        "tür": "Rezervasyon",
        "durum": "OK",
        "bulgu": "Ayrı domain → cross-domain ölçüm şart",
        "öncelik": "Yüksek",
    },
    {
        "mülk": "Google İşletme/Maps",
        "tür": "Yerel",
        "durum": "DENETLE",
        "bulgu": "Panel var; sahiplik + NAP standardı şart",
        "öncelik": "Kritik",
    },
    {
        "mülk": "Instagram @kozbeylikonagi",
        "tür": "Sosyal",
        "durum": "AKTİF",
        "bulgu": "~11K; bio link hedefi doğrulanmalı",
        "öncelik": "Yüksek",
    },
    {
        "mülk": "Facebook /kozbeylikonagi",
        "tür": "Sosyal",
        "durum": "AKTİF",
        "bulgu": "About NAP tek standarda çekilmeli",
        "öncelik": "Orta",
    },
    {
        "mülk": "TripAdvisor",
        "tür": "OTA/yorum",
        "durum": "DÜŞÜK",
        "bulgu": "3/5 + düşük hacim; yorum kampanyası",
        "öncelik": "Yüksek",
    },
    {
        "mülk": "Booking / trivago / OTA'lar",
        "tür": "OTA",
        "durum": "DAĞINIK",
        "bulgu": "Marka SERP OTA-dominant; NAP/şehir tutarsız",
        "öncelik": "Yüksek",
    },
]

# Onceliklendirilmis duzeltme listesi (docs/09 ile birebir)
FIXES = [
    (
        1,
        "Tek kanonik domain + tek telefon",
        ".com",
        "Yüksek",
        "Tek odak www.kozbeylikonagi.com; tek numara +90 532 234 2686 (her kanalda birebir)",
    ),
    (
        2,
        "Parazit otel.com (Haz 2026: DNS çözülmüyor = muht. ölü)",
        "otel.com",
        "Orta",
        "Site ölü görünüyor; Google'da kalan listing + GBP numarasını teyit/temizle",
    ),
    (
        3,
        ".com.tr KAPSAM DIŞI (sahip ayrı yönetiyor)",
        ".com.tr",
        "Düşük",
        "Sistemin tek odağı .com; .com.tr gündem değil (Yunuscan: sil kafandan). Reklam/SEO zaten .com.",
    ),
    (
        4,
        "Google Business sahiplik + NAP standardı",
        "Google/OTA",
        "Kritik",
        "GBP sahiplen; NAP tek standart (Foça vs Yenifoça)",
    ),
    (
        5,
        "JSON-LD VAR ama tamlık şüpheli (Haz 2026)",
        ".com",
        "Yüksek",
        "Mevcut schema'yı Rich Results Test ile denetle; Hotel+Restaurant+FAQPage+HotelRoom tamamla (kads seo schema)",
    ),
    (
        6,
        "HMS cross-domain ölçüm yok",
        ".com + hms",
        "Yüksek",
        "GA4 allowLinker + referral exclusion + begin_checkout",
    ),
    (
        7,
        "Marka SERP OTA-dominant",
        "OTA + .com",
        "Yüksek",
        "Marka organik/ücretli savunma; OTA profil eşitle",
    ),
    (
        8,
        "TripAdvisor 3/5 + düşük hacim",
        "TripAdvisor",
        "Yüksek",
        "Yorum toplama kampanyası; profil güncelle",
    ),
    (
        9,
        "IG/FB bio link + NAP doğrulanamadı",
        "IG + FB",
        "Yüksek",
        "Bio link=.com/WhatsApp; FB About NAP",
    ),
    (10, "EN placeholder metinler", ".com/en", "Orta", "Gerçek yorum/içerik"),
    (
        11,
        "hreflang TR↔EN doğrulanamadı",
        ".com",
        "Orta",
        "rel=alternate hreflang çiftleri",
    ),
    (
        12,
        "Mesafe/şehir tutarsız",
        "Site + OTA",
        "Orta",
        "Tek metin: 'Yeni Foça'ya yakın'",
    ),
    (
        13,
        "Çalışma saati çelişkisi; boş sayfalar",
        ".com",
        "Düşük",
        "SSS ile hizala; doldur",
    ),
    (14, "Marka adı varyasyonu", "Tüm kanallar", "Düşük", "'Kozbeyli Konağı' sabit"),
]

_PRI = {"Kritik": 0, "Yüksek": 1, "Orta": 2, "Düşük": 3, "Kapandı": 4}


def property_rows() -> list[dict]:
    """Dijital mülk envanteri satırları (site/Maps/OTA/sosyal)."""
    return PROPERTIES


def fix_rows() -> list[dict]:
    """Önceliklendirilmiş dijital varlık düzeltme satırları."""
    return [
        {"#": n, "bulgu": b, "mülk": m, "öncelik": p, "aksiyon": a}
        for n, b, m, p, a in sorted(FIXES, key=lambda x: _PRI.get(x[3], 9))
    ]


def counts() -> dict:
    """Önem derecesine göre düzeltme sayıları özeti."""
    c = {"Kritik": 0, "Yüksek": 0, "Orta": 0, "Düşük": 0}
    for f in FIXES:
        c[f[3]] = c.get(f[3], 0) + 1
    return c
