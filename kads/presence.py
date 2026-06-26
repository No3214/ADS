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
    {"mülk": "kozbeylikonagi.com", "tür": "Web (ana)", "durum": "GÜÇLÜ",
     "bulgu": "Gerçek site; schema/hreflang/cross-domain eksik", "öncelik": "Yüksek"},
    {"mülk": "kozbeylikonagi.com.tr", "tür": "Web (kabuk)", "durum": "ZAYIF",
     "bulgu": "Image-only, metin yok, alt sayfalar ana sayfaya düşüyor", "öncelik": "Kritik"},
    {"mülk": "kozbeylikonagiotel.com", "tür": "Web (parazit)", "durum": "RİSK",
     "bulgu": "Eski domain + YANLIŞ telefon (0232 218 2109)", "öncelik": "Kritik"},
    {"mülk": "hmshotel.net (booking)", "tür": "Rezervasyon", "durum": "OK",
     "bulgu": "Ayrı domain → cross-domain ölçüm şart", "öncelik": "Yüksek"},
    {"mülk": "Google İşletme/Maps", "tür": "Yerel", "durum": "DENETLE",
     "bulgu": "Panel var; sahiplik + NAP standardı şart", "öncelik": "Kritik"},
    {"mülk": "Instagram @kozbeylikonagi", "tür": "Sosyal", "durum": "AKTİF",
     "bulgu": "~11K; bio link hedefi doğrulanmalı", "öncelik": "Yüksek"},
    {"mülk": "Facebook /kozbeylikonagi", "tür": "Sosyal", "durum": "AKTİF",
     "bulgu": "About NAP tek standarda çekilmeli", "öncelik": "Orta"},
    {"mülk": "TripAdvisor", "tür": "OTA/yorum", "durum": "DÜŞÜK",
     "bulgu": "3/5 + düşük hacim; yorum kampanyası", "öncelik": "Yüksek"},
    {"mülk": "Booking / trivago / OTA'lar", "tür": "OTA", "durum": "DAĞINIK",
     "bulgu": "Marka SERP OTA-dominant; NAP/şehir tutarsız", "öncelik": "Yüksek"},
]

# Onceliklendirilmis duzeltme listesi (docs/09 ile birebir)
FIXES = [
    (1, "Üç marka domaini + çelişkili telefon", "Tüm domainler", "Kritik",
     ".com canonical; diğerleri 301; tek numara +90 532 234 2686"),
    (2, "kozbeylikonagiotel.com yanlış numara yayında", "otel.com", "Kritik",
     "Sahiplik teyit; kaldır/301; Google'da numarayı düzelt"),
    (3, ".com.tr image-only kabuk", ".com.tr", "Kritik",
     "301 ile çöz; tutulacaksa metin + schema"),
    (4, "Google Business sahiplik + NAP standardı", "Google/OTA", "Kritik",
     "GBP sahiplen; NAP tek standart (Foça vs Yenifoça)"),
    (5, "schema.org JSON-LD yok", ".com", "Yüksek",
     "Hotel + Restaurant + FAQPage JSON-LD ekle (kads seo schema)"),
    (6, "HMS cross-domain ölçüm yok", ".com + hms", "Yüksek",
     "GA4 allowLinker + referral exclusion + begin_checkout"),
    (7, "Marka SERP OTA-dominant", "OTA + .com", "Yüksek",
     "Marka organik/ücretli savunma; OTA profil eşitle"),
    (8, "TripAdvisor 3/5 + düşük hacim", "TripAdvisor", "Yüksek",
     "Yorum toplama kampanyası; profil güncelle"),
    (9, "IG/FB bio link + NAP doğrulanamadı", "IG + FB", "Yüksek",
     "Bio link=.com/WhatsApp; FB About NAP"),
    (10, "EN placeholder metinler", ".com/en", "Orta", "Gerçek yorum/içerik"),
    (11, "hreflang TR↔EN doğrulanamadı", ".com", "Orta", "rel=alternate hreflang çiftleri"),
    (12, "Mesafe/şehir tutarsız", "Site + OTA", "Orta", "Tek metin: 'Foça merkeze ~13 km'"),
    (13, "Çalışma saati çelişkisi; boş sayfalar", ".com", "Düşük", "SSS ile hizala; doldur"),
    (14, "Marka adı varyasyonu", "Tüm kanallar", "Düşük", "'Kozbeyli Konağı' sabit"),
]

_PRI = {"Kritik": 0, "Yüksek": 1, "Orta": 2, "Düşük": 3}


def property_rows() -> list[dict]:
    return PROPERTIES


def fix_rows() -> list[dict]:
    return [{"#": n, "bulgu": b, "mülk": m, "öncelik": p, "aksiyon": a}
            for n, b, m, p, a in sorted(FIXES, key=lambda x: _PRI.get(x[3], 9))]


def counts() -> dict:
    c = {"Kritik": 0, "Yüksek": 0, "Orta": 0, "Düşük": 0}
    for f in FIXES:
        c[f[3]] = c.get(f[3], 0) + 1
    return c
