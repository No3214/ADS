#!/usr/bin/env python3
"""
kads.data — TEK KAYNAK (single source of truth).

Tum kampanya verisi burada yasar: otel gercekleri, kanal plani, butce, anahtar
kelimeler, negatifler, Google RSA varliklari ve Meta reklam metinleri. Platform
modulleri (kads/platforms/*.py) bu veriyi okuyup Google Ads Editor CSV'leri ve
Meta kurulum sayfalarini uretir. assets/*.yaml dosyalari insan icin okunabilir
aynalardir; uretim icin kanonik kaynak BU dosyadir.

Tum sayilar PLANLAMA TAHMINIDIR, garanti degildir (bkz. README + plan notu).
Para birimi: TRY. Diller: reklamlar TR, site TR+EN.
"""

from __future__ import annotations

# ---- Otel gercekleri (web arastirmasiyla dogrulandi, Haziran 2026) ---------
HOTEL = {
    "name": "Kozbeyli Konağı",
    "type": "Butik / tarihi taş konak oteli",
    "site": "www.kozbeylikonagi.com",
    "address": "Kozbeyli Köyü, Küme Evler No:188, 35680 Foça / İzmir",
    "geo": {"village": "Kozbeyli", "town": "Foça", "city": "İzmir", "country": "TR"},
    "distance_foca_km": 13,
    "rooms_total": 16,
    "room_types": ["Standart Oda", "Superior Oda (manzaralı)", "Aile Odası (5 kişi)"],
    "avg_nightly_try": 2000,  # web: ~1.900-2.000 TL/gece (Haziran 2026)
    "checkin": "14:00",
    "checkout": "12:00",
    "usps": [
        "600 yıllık Kozbeyli köyünde Osmanlı taş mimarisi",
        "Çatı terasında Ege/deniz manzarası",
        "Organik köy kahvaltısı + Antakya–Ege mutfağı",
        "Evcil hayvan dostu (ücretsiz)",
        "Doğrudan & komisyonsuz rezervasyon",
        "Foça'ya 13 km, sessiz ve özel",
    ],
    "high_season": "Haziran–Eylül",
    "low_season": "Kasım–Mart",
    "phone_hint": "Arama + WhatsApp uzantisi (gercek numara .env/Ads icine)",
}

# ---- Olcum kimlikleri (config/ads-assets.yaml ile ayni) --------------------
TRACKING = {
    "ga4": "G-V3R66C3MEF",
    "google_ads_tag": "AW-800024713",
    "meta_pixel": "1781546559309505",
    "meta_business": "604201716594111",
    "gtm_candidates": ["GTM-KCG6B4MJ", "GTM-MSL2FLF5"],
    "booking_engine": "hmshotel.net  (https://{slug}.hmshotel.net/ — cross-domain ZORUNLU)",
}

# ---- 30.000 TL/ay capraz kanal plani ---------------------------------------
PLAN = {
    "total_monthly_try": 30000,
    "google_monthly_try": 15000,
    "meta_monthly_try": 15000,
    "channels": [
        {
            "kanal": "Google — Marka Search",
            "aylik_try": 4500,
            "gunluk_try": 148,
            "islev": "Marka/OTA savunması",
            "faz": "Hafta 3-5",
        },
        {
            "kanal": "Google — Dar non-brand Search",
            "aylik_try": 9000,
            "gunluk_try": 296,
            "islev": "Yüksek niyetli yeni talep",
            "faz": "Hafta 5-8",
        },
        {
            "kanal": "Google — Kontrollü test",
            "aylik_try": 1500,
            "gunluk_try": 49,
            "islev": "Arama terimi & sezon testi",
            "faz": "Sürekli",
        },
        {
            "kanal": "Meta — Prospecting (Website Sales)",
            "aylik_try": 10500,
            "gunluk_try": 350,
            "islev": "Yeni kitle, direkt rezervasyon",
            "faz": "Hafta 4-6 (ay 1)",
        },
        {
            "kanal": "Meta — WhatsApp/Mesaj",
            "aylik_try": 4500,
            "gunluk_try": 150,
            "islev": "Nitelikli rezervasyon görüşmesi",
            "faz": "Hafta 4-6 (ay 1)",
        },
        {
            "kanal": "Meta — Retargeting",
            "aylik_try": 3000,
            "gunluk_try": 100,
            "islev": "Site/IG/checkout terk",
            "faz": "Hafta 8-12 (ay 2+)",
        },
    ],
    # Ay 2+ Meta yeniden dengeleme: Prospecting 9.000 / Retargeting 3.000 / WhatsApp 3.000
    "commercial_targets": [
        {"hedef": "3x medya ROAS", "izlenen_rezervasyon_geliri_try": 90000},
        {"hedef": "4x medya ROAS", "izlenen_rezervasyon_geliri_try": 120000},
    ],
}

# ---- Bicimlendirilmis butce tavanlari (guardrails ile ayni) ----------------
BUDGET_CAPS = {
    "google_daily_try": 493,
    "google_monthly_try": 15000,
    "meta_daily_try": 500,
    "meta_monthly_try": 15000,
}

# ---- GOOGLE: anahtar kelimeler ---------------------------------------------
# Reklam grubu bazinda. Eslesme: [E]=Exact, [P]=Phrase. Genis eslesme KULLANILMAZ
# (kucuk butce + dar niyet). Marka grubu tek basina yuksek niyet -> dusuk CPC.
KEYWORDS = {
    "Marka": {  # Brand — OTA savunmasi, en dusuk CPC, en yuksek CVR
        "match": "phrase_and_exact",
        "terms": [
            "kozbeyli konağı",
            "kozbeyli konagi",
            "kozbeyli konağı otel",
            "kozbeyli konağı foça",
            "kozbeyli konağı rezervasyon",
            "kozbeyli konağı fiyat",
            "kozbeyli konağı izmir",
            "kozbeyli butik otel",
            "kozbeyli konağı yorum",
            "kozbeyli otel",
            "foça kozbeyli konağı",
        ],
    },
    "NonBrand-Foca-Butik": {  # Yuksek niyetli yeni talep
        "match": "phrase_and_exact",
        "terms": [
            "foça butik otel",
            "foça taş ev otel",
            "foça konak otel",
            "eski foça butik otel",
            "foça köy oteli",
            "foça otantik otel",
            "kozbeyli köyü otel",
            "kozbeyli konaklama",
            "eski foça otel",
            "foça kozbeyli",
            "foça antik otel",
            "eski foça konak otel",
            "yeni foça butik otel",
            "yeni foça köy oteli",
            "yeni foça taş otel",
            "kozbeyli foça",
        ],
    },
    "NonBrand-Foca-Genel": {  # Daha genis ama yine niyetli
        "match": "phrase",
        "terms": [
            "foça otel",
            "foça otelleri",
            "foça konaklama",
            "foça deniz manzaralı otel",
            "foça balayı oteli",
            "foça evcil hayvan kabul eden otel",
            "foça hafta sonu kaçamağı otel",
            "otel foça",
            "eski foça otelleri",
            "yeni foça otelleri",
            "foça merkez otel",
            "yeni foça otel",
            "yeni foça konaklama",
            "yeni foça deniz manzaralı otel",
        ],
    },
    "NonBrand-Niche": {  # Konsept/deneyim niyeti
        "match": "phrase",
        "terms": [
            "izmir taş konak otel",
            "izmir butik köy oteli",
            "ege köy kahvaltısı konaklama",
            "foça doğa tatili otel",
            "izmir sakin kaçış oteli",
        ],
    },
}

# ---- GOOGLE: hesap duzeyi negatif anahtar kelime listesi -------------------
# Niyetsiz/yanlis-niyet trafigi keser. Kucuk butcede negatif = en onemli kaldirac.
NEGATIVES = [
    # is/emlak/finans niyeti
    "iş ilanı",
    "iş",
    "kariyer",
    "personel",
    "eleman",
    "maaş",
    "kiralık",
    "satılık",
    "emlak",
    "arsa",
    "daire",
    "müstakil",
    # bilgi/ucretsiz niyeti
    "nasıl gidilir",
    "yol tarifi",
    "harita",
    "hava durumu",
    "nüfus",
    "gezilecek yerler",
    "ne demek",
    "tarihçe",
    "vikipedi",
    "wikipedia",
    "nedir",
    "yorumları",
    "şikayet",
    "şikayetvar",
    # ucuz/bedava/alakasiz
    "ucuz",
    "bedava",
    "free",
    "camping",
    "kamp",
    "çadır",
    "karavan",
    "pansiyon",
    "hostel",
    "apart",
    "günlük kiralık",
    "yazlık kiralık",
    # alakasiz lokasyon/markalar (genel non-brand grubu icin)
    "çeşme",
    "alaçatı",
    "bodrum",
    "kuşadası",
    "marmaris",
    "didim",
    "antalya",
    "kapadokya",
    "abant",
    "sapanca",
    # OTA/aggregator (marka disinda; direkt rezervasyona yonlendir)
    "booking",
    "trivago",
    "etstur",
    "tatilsepeti",
    "jolly",
    "obilet",
    # alakasiz arama
    "düğün salonu fiyat",
    "iş başvurusu",
    "telefon numarası rehber",
    # --- canli hesap arama terimi madenciligi (Haz 2026): bos-harcama ---
    "plaj",
    "plajları",
    "beach",
    "koylar",
    "deniz",
    "glamping",
    "bungalow",
    "orman kampı",
    "dome",
    "öğretmenevi",
    "sosyal tesis",
    "tesisleri",
    "gezilecek",
    "kordon",
    "kemeraltı",
    "seyir tepesi",
    "bostanlı",
    # alakasiz lokasyonlar (gercek terimlerden)
    "urla",
    "manisa",
    "bergama",
    "dikili",
    "karaburun",
    "sasalı",
    "şakran",
    "nazarköy",
    "çiçekli",
    "aliağa kiralık",
    # rakip isimleri (markalarini biz odemeyelim)
    "gaia",
    "saklı cennet",
    "club med",
    "voodoo",
    "kybele",
    "palandız",
]

# ---- GOOGLE: RSA varliklari (reklam grubu bazinda) -------------------------
# Basliklar <=30, aciklamalar <=90 karakter. Dogrulanamayan iddia ("en ucuz") YOK.
RSA = {
    "Marka": {
        "final_url": "https://www.kozbeylikonagi.com/rezervasyon",
        "path1": "Foca",
        "path2": "Rezervasyon",
        "headlines": [
            "Kozbeyli Konağı Resmî",  # marka + resmi sinyali
            "Kozbeyli Konağı Foça",
            "Doğrudan & Komisyonsuz",
            "Resmî Siteden Rezerve Et",
            "600 Yıllık Taş Konak",
            "Deniz Manzaralı Odalar",
            "Organik Köy Kahvaltısı",
            "Çatı Terası & Ege Manzarası",
            "Evcil Hayvan Dostu Otel",
            "Foça'ya 13 km Huzur",
            "16 Özel Tasarım Oda",
            "Antakya & Ege Mutfağı",
            "Hızlı Tarih Seçimi",
            "Otelden Direkt Fiyat",
            "Kozbeyli Köyünde Konak",
        ],
        "descriptions": [
            "Kozbeyli Konağı resmî sitesi. Doğrudan rezerve edin, komisyon ödemeyin.",
            "Osmanlı taş mimarisinde 16 oda, deniz manzarası ve organik köy kahvaltısı.",
            "Çatı terasında Ege manzarası, Antakya sofrası. Hızlı ve güvenli rezervasyon.",
            "Evcil dostlarınız ücretsiz. Sessizlik, miras ve zarafet bir arada.",
        ],
    },
    "NonBrand": {
        "final_url": "https://www.kozbeylikonagi.com/odalar",
        "path1": "Foca",
        "path2": "Butik-Otel",
        "headlines": [
            "Foça'da Taş Konak Oteli",
            "Kozbeyli Konağı Foça",
            "600 Yıllık Köyde Huzur",
            "Foça'da Sessiz Lüks",
            "Deniz Manzaralı Taş Oda",
            "Organik Köy Kahvaltısı",
            "Doğrudan Rezervasyon",
            "Foça'ya 13 km Mesafede",
            "Evcil Hayvan Dostu Otel",
            "Çatı Terasında Ege Keyfi",
            "Antakya ve Ege Mutfağı",
            "16 Özel Tasarım Oda",
            "Eski Foça Köy Oteli",
            "Zeytinlikte Taş Konak",
            "Hafta İçi Sakin Kaçış",
        ],
        "descriptions": [
            "Foça'nın 600 yıllık Kozbeyli köyünde huzurlu kaçış. Doğrudan otelden rezerve edin.",
            "Osmanlı taş mimarisinde 16 oda, deniz manzarası ve organik köy kahvaltısı.",
            "Çatı terasında Ege manzarası, Antakya sofrası, pişi ve dibek kahvesi sizi bekliyor.",
            "Evcil dostlarınız ücretsiz kabul edilir. Sessizlik, miras ve zarafet bir arada.",
        ],
    },
}

# ---- GOOGLE: uzantilar (sitelink/callout/snippet) --------------------------
SITELINKS = [
    {
        "text": "Odalar",
        "desc1": "16 özel tasarım oda",
        "desc2": "Deniz manzaralı seçenekler",
        "url": "https://www.kozbeylikonagi.com/odalar",
    },
    {
        "text": "Restoran ve Mutfak",
        "desc1": "Antakya ve Ege sofrası",
        "desc2": "Organik köy kahvaltısı",
        "url": "https://www.kozbeylikonagi.com/gastronomi",
    },
    {
        "text": "Galeri ve Foça",
        "desc1": "Konak ve köy fotoğrafları",
        "desc2": "Çevre gezi önerileri",
        "url": "https://www.kozbeylikonagi.com/galeri",
    },
    {
        "text": "Rezervasyon",
        "desc1": "Doğrudan ve komisyonsuz",
        "desc2": "Hızlı tarih seçimi",
        "url": "https://www.kozbeylikonagi.com/rezervasyon",
    },
    {
        "text": "İletişim ve Yol Tarifi",
        "desc1": "Telefon ve WhatsApp",
        "desc2": "Foça'ya 13 km",
        "url": "https://www.kozbeylikonagi.com/lokasyon",
    },
    {
        "text": "Etkinlik ve Düğün",
        "desc1": "Tarihi konak atmosferi",
        "desc2": "Özel organizasyon",
        "url": "https://www.kozbeylikonagi.com/organizasyonlar",
    },
]
CALLOUTS = [
    "Ücretsiz otopark",
    "Organik köy kahvaltısı",
    "Evcil hayvan dostu",
    "Deniz manzaralı odalar",
    "Doğrudan rezervasyon avantajı",
    "Çatı terası",
]
STRUCTURED_SNIPPETS = [
    {
        "header": "Olanaklar",
        "values": [
            "Ücretsiz Wi-Fi",
            "Klima",
            "Restoran",
            "Tarihi konak",
            "Çatı terası",
        ],
    },
    {"header": "Çevre", "values": ["Foça", "Yeni Foça", "Kozbeyli Köyü"]},
]

# ---- GOOGLE: hedefleme ------------------------------------------------------
GEO_TARGETS = [
    "Foça, İzmir",
    "İzmir",
    "Manisa",
    "İstanbul",
    "Ankara",
    "Bursa",
]
GEO_NOTE = "Kaynak şehirler (İstanbul/Ankara/Bursa) + yerel (İzmir/Foça). Radius değil şehir hedefi."
AD_SCHEDULE_NOTE = "Türkiye'de turizm dönüşüm pikleri 08–11 ve 19–22. Bütçe darsa bu saatlere ağırlık ver."

# ---- META: reklam metinleri (konsept bazinda, gercek TR kopya) -------------
# Her konsept: primary_text varyantlari + basliklar + aciklama. 9:16 Reels/Stories,
# 4:5 Feed. Dogrulanamayan "en ucuz/en iyi fiyat" iddiasi YOK.
META_COPY = {
    "Konsept1-TasKonak": {
        "tema": "Taş konak & 600 yıllık köy",
        "primary_text": [
            "600 yıllık Kozbeyli köyünde, Osmanlı taş mimarisiyle restore edilmiş bir konak. "
            "Avlu, zeytinlikler ve köyün dokusu sizi bekliyor. Doğrudan rezerve edin, komisyon ödemeyin.",
            "Zamanın yavaşladığı bir köy. Taş duvarlar, sabah ışığı ve Ege sessizliği. "
            "Kozbeyli Konağı'nda yerinizi şimdiden ayırtın.",
        ],
        "headlines": ["Taş Konakta Huzur", "600 Yıllık Köyde Konaklayın"],
        "description": "Foça'ya 13 km, doğrudan rezervasyon.",
        "cta": "Book Now",
        "destination": "Website (rezervasyon/oda sayfası)",
    },
    "Konsept2-Manzara": {
        "tema": "Oda, çatı terası & Ege manzarası",
        "primary_text": [
            "Odanızdan çatı terasına çıkın, Ege manzarası ve gün batımı önünüzde. "
            "Kozbeyli Konağı'nda sakin bir kaçış için müsaitliğe bakın.",
            "Deniz manzaralı odalar, çatı terasında kahve keyfi. Hafta içi sessizlik, "
            "hafta sonu huzur. Tarihinizi seçin.",
        ],
        "headlines": ["Ege Manzaralı Kaçış", "Çatı Terasında Gün Batımı"],
        "description": "Müsaitliğe bakın, doğrudan rezerve edin.",
        "cta": "Book Now",
        "destination": "Website (oda sayfası)",
    },
    "Konsept3-Kahvalti": {
        "tema": "Organik köy kahvaltısı & Antakya–Ege mutfağı",
        "primary_text": [
            "Pişi, ev reçelleri, dibek kahvesi ve Antakya sofrası. Kozbeyli Konağı'nda "
            "güne organik köy kahvaltısıyla başlayın.",
            "Sofranın bereketi köyden. Organik kahvaltı, Ege otları, taş fırın lezzetleri. "
            "Tadına bakmaya gelin.",
        ],
        "headlines": ["Organik Köy Kahvaltısı", "Antakya & Ege Sofrası"],
        "description": "Köy lezzetleri, taş konak atmosferi.",
        "cta": "Learn More",
        "destination": "Website (restoran sayfası)",
    },
    "Konsept4-Evcil": {
        "tema": "Evcil hayvan dostu konaklama",
        "primary_text": [
            "Evcil dostunuz da davetli — ücretsiz. Konak avlusunda huzurlu bir tatil, "
            "mama kabı bizden. Kozbeyli Konağı'nda yerinizi ayırtın.",
        ],
        "headlines": ["Evcil Dostunuzla Gelin", "Pati Dostu Konak"],
        "description": "Ücretsiz kabul, avluda huzur.",
        "cta": "Book Now",
        "destination": "Website (rezervasyon sayfası)",
    },
    "Konsept5-WhatsApp": {
        "tema": "Hafta içi sakin kaçış & müsaitlik (WhatsApp/Mesaj)",
        "primary_text": [
            "Bu hafta birkaç oda boş. Hafta içi sessizliğinde Kozbeyli Konağı'na kaçın. "
            "Tarih ve fiyat için mesaj atın, hemen yanıtlayalım.",
        ],
        "headlines": ["Bu Hafta Birkaç Oda", "Mesaj Atın, Yanıtlayalım"],
        "description": "WhatsApp'tan hızlı rezervasyon görüşmesi.",
        "cta": "Send Message",
        "destination": "WhatsApp / Messenger",
    },
}

# ---- META: kitleler ve yerlesimler -----------------------------------------
META_AUDIENCES = {
    "Prospecting": {
        "tip": "Geniş + ilgi sinyali (Advantage+ kitle önerilir, dar tutma)",
        "konum": "İstanbul, Ankara, İzmir, Bursa + 25 km Foça çevresi",
        "yas": "28-60",
        "diller": ["Türkçe"],
        "ilgi": [
            "Butik otel",
            "Seyahat",
            "Hafta sonu kaçamağı",
            "Doğa turizmi",
            "Gurme/yeme-içme",
            "Evcil hayvan sahipleri",
            "Ege/Foça",
        ],
        "not": "Öğrenme aşaması için kitleyi aşırı daraltma; tek ad set, 3-4 kreatif.",
    },
    "Retargeting": {
        "tip": "Custom Audience (ay 2+, liste dolunca)",
        "kaynaklar": [
            "Site ziyaretçisi 30/60 gün",
            "IG/FB etkileşim 365 gün",
            "rezervasyon başlatıp tamamlamayan (begin_checkout)",
        ],
        "not": "Site/IG kitlesi yeterince dolmadan AÇMA.",
    },
    "Lookalike": {
        "tip": "LLA %1-3 (yeterli dönüşüm/etkileşim sonrası)",
        "kaynak": "Purchase veya WhatsApp lead custom audience",
        "not": "Veri eşiği oluşmadan açma; prospecting'i önce doğrula.",
    },
}
META_PLACEMENTS = {
    "öneri": "Advantage+ Placements (otomatik) — küçük bütçede manuel bölme yapma.",
    "kreatif_oranlari": {"Reels/Stories": "9:16", "Feed": "4:5", "kare_yedek": "1:1"},
}

# ---- KPI / kapanis matematigi ----------------------------------------------
KPI = {
    "whatsapp_formula": "Maksimum CPL = rezervasyon CPA × (lead→rezervasyon oranı)",
    "ornek": "Rezervasyon CPA 2.000 TL, kapanış %15 → maksimum WhatsApp lead maliyeti 300 TL.",
    "blended_note": "Başarı blended (Google+Meta) CPA ve ROAS ile ölçülür; tek platform metriğine takılma.",
}
