#!/usr/bin/env python3
"""
kads.data_ext — kampanya şablon genişletmeleri: Google Display, Meta yerleşim
şablonları (Feed/Stories/Reels), A/B varyant yapıları, retargeting kitleleri,
bütçe/teklif optimizasyon kuralları. data.py tek kaynağını tamamlar.
"""

from __future__ import annotations

# ---- GOOGLE Display (Responsive Display Ad) — remarketing/awareness şablonu ----
# NOT: Plan ilk 30-45 gün Google Display'i AÇMAZ (remarketing Meta'da). Bu şablon
# PAUSED ve hazırdır; doygunluk + veri sonrası değerlendir (docs/03).
GOOGLE_DISPLAY = {
    "campaign": "Kozbeyli | Display | Remarketing",
    "daily_try": 60,
    "status": "Paused",
    "bid": "Maximize clicks",  # 0 dönüşümde tCPA/MaxConv öğrenemez; ölçüm kurulunca BID_GRADUATE ile geç
    "note": "Plan gereği ertelenir; Meta retargeting önce. PAUSED hazır şablon.",
    "audience": "Site ziyaretçileri 30/60 gün (Google Ads remarketing list)",
    "short_headlines": [  # <=30
        "Kozbeyli Konağı Foça",
        "600 Yıllık Taş Konak",
        "Deniz Manzaralı Odalar",
        "Organik Köy Kahvaltısı",
        "Doğrudan Rezervasyon",
    ],
    "long_headline": "Foça'da 600 yıllık köyde taş konak: huzur, manzara, köy kahvaltısı",  # <=90
    "descriptions": [  # <=90
        "Osmanlı taş mimarisinde 16 oda, çatı terasında Ege manzarası. Doğrudan rezerve edin.",
        "Evcil dostlarınız ücretsiz. Sessiz, özel, mirasla iç içe bir kaçış.",
    ],
    "business_name": "Kozbeyli Konağı",
    "final_url": "https://www.kozbeylikonagi.com/odalar",
    "image_note": "Yatay 1.91:1 + kare 1:1 + logo yükle (cephe/oda/teras/kahvaltı).",
}

# ---- META yerleşim şablonları (placement-specific) -------------------------
META_PLACEMENT_SPECS = {
    "Feed": {
        "ratio": "4:5",
        "px": "1080x1350",
        "primary_text_max": 125,
        "headline_max": 40,
        "media": "Görsel veya video",
        "note": "Feed'de 4:5 en çok alan.",
    },
    "Stories": {
        "ratio": "9:16",
        "px": "1080x1920",
        "primary_text": "az/etiket",
        "safe_zone": "üst 250px + alt 340px boş bırak",
        "media": "Dikey video/görsel",
        "duration": "<=15 sn",
        "note": "İlk 1-2 sn hook; ses+altyazı.",
    },
    "Reels": {
        "ratio": "9:16",
        "px": "1080x1920",
        "primary_text_max": 72,
        "media": "Dikey video",
        "duration": "10-30 sn",
        "note": "İlk 3 sn hook; trend ses/altyazı; CTA sticker.",
    },
}

# ---- A/B varyant açıları (her kampanya için >=3 varyant) -------------------
# Google RSA: her reklam grubunda 3 ad varyantı, farklı Headline 1 (açı).
AB_ANGLES = {
    "A-Miras": "600 Yıllık Taş Konak",
    "B-Manzara": "Deniz Manzaralı Odalar",
    "C-Direkt": "Doğrudan & Komisyonsuz",
}
# Meta: her konseptte 3 reklam varyantı (farklı hook/primary text).
META_AB_HOOKS = {
    "A-Hikaye": "600 yıllık köyde bir sabah...",
    "B-Fayda": "Deniz manzaralı oda + organik kahvaltı.",
    "C-Aciliyet": "Bu hafta birkaç oda boş.",
}

# ---- Retargeting / Custom + Lookalike kitleleri ----------------------------
RETARGETING_AUDIENCES = [
    {
        "ad": "RTG - Site 30 gün",
        "tip": "Website Custom Audience",
        "kaynak": "Tüm site ziyaretçileri",
        "pencere": "30 gün",
        "kullanim": "Retargeting kampanya — genel hatırlatma",
    },
    {
        "ad": "RTG - Site 60 gün",
        "tip": "Website Custom Audience",
        "kaynak": "Tüm site ziyaretçileri",
        "pencere": "60 gün",
        "kullanim": "Daha geniş retargeting havuzu",
    },
    {
        "ad": "RTG - Oda/Rezervasyon görüntüleyen",
        "tip": "Website Custom Audience (URL içerir)",
        "kaynak": "/odalar veya /rezervasyon görüntüleyen",
        "pencere": "30 gün",
        "kullanim": "Yüksek niyet — güçlü teklif/aciliyet",
    },
    {
        "ad": "RTG - Checkout terk (begin_checkout)",
        "tip": "Website Custom Audience (olay)",
        "kaynak": "begin_checkout var, Purchase yok",
        "pencere": "14-30 gün",
        "kullanim": "Sepet/rezervasyon terk — en sıcak retargeting",
    },
    {
        "ad": "RTG - IG/FB etkileşim",
        "tip": "Engagement Custom Audience",
        "kaynak": "IG + FB profil/post etkileşimi",
        "pencere": "365 gün",
        "kullanim": "Sosyal etkileşenleri geri kazan",
    },
    {
        "ad": "RTG - Video izleyen %50+",
        "tip": "Video Custom Audience",
        "kaynak": "Reels/video %50+ izleyen",
        "pencere": "90 gün",
        "kullanim": "İlgi gösterenleri dönüşüme taşı",
    },
    {
        "ad": "LLA - Purchase %1",
        "tip": "Lookalike",
        "kaynak": "Purchase custom audience (yeterli veri sonrası)",
        "pencere": "%1 TR",
        "kullanim": "Prospecting genişletme — en kaliteli",
    },
    {
        "ad": "LLA - WhatsApp lead %1-3",
        "tip": "Lookalike",
        "kaynak": "Nitelikli WhatsApp lead",
        "pencere": "%1-3 TR",
        "kullanim": "Lead benzeri yeni kitle",
    },
]
RETARGETING_NOTE = (
    "Retargeting yalnız ay 2+ ve liste yeterince dolunca açılır (docs/03). "
    "Google remarketing AÇILMAZ; retargeting Meta'da. Min kitle ~1.000 kişi."
)

# ---- Bütçe / teklif optimizasyon kuralları (deterministik) -----------------
# (metrik, koşul operatörü, eşik, aksiyon, öncelik). kads rules bunları metriğe uygular.
OPT_RULES = [
    {
        "id": "ROAS_SCALE",
        "metric": "blended_roas",
        "op": ">=",
        "threshold": 3.0,
        "action": "Bütçeyi kademeli +%20 artır (guardrail tavanına kadar)",
        "pri": "Fırsat",
    },
    {
        "id": "ROAS_CUT",
        "metric": "blended_roas",
        "op": "<",
        "threshold": 2.0,
        "action": "Bütçeyi kıs / düşük performans öğeyi duraklat",
        "pri": "Risk",
    },
    {
        "id": "CPA_OVER",
        "metric": "blended_cpa_try",
        "op": ">",
        "threshold": 2000,
        "action": "Hedef CPA aşıldı: kitle/keyword daralt, teklif düşür",
        "pri": "Risk",
    },
    {
        "id": "CTR_LOW_NB",
        "metric": "nonbrand_ctr_pct",
        "op": "<",
        "threshold": 2.0,
        "action": "Non-brand CTR düşük: başlık/uzantı testi, keyword daralt",
        "pri": "Orta",
    },
    {
        "id": "FREQ_HIGH",
        "metric": "meta_frequency",
        "op": ">",
        "threshold": 2.5,
        "action": "Kreatif yorgunluğu: kreatifi yenile (A/B varyant değiştir)",
        "pri": "Orta",
    },
    {
        "id": "CPC_SPIKE",
        "metric": "cpc_try",
        "op": ">",
        "threshold": 12.0,
        "action": "CPC TR ort. üstünde: CPC limiti gözden geçir, negatif ekle",
        "pri": "Orta",
    },
    {
        "id": "LEARN_LIMITED",
        "metric": "weekly_conversions",
        "op": "<",
        "threshold": 50,
        "action": "Öğrenme sınırlı: ad set birleştir, bütçe topla, kreatif azalt",
        "pri": "Orta",
    },
    {
        "id": "BID_GRADUATE",
        "metric": "conversions_30d",
        "op": ">=",
        "threshold": 15,
        "action": "Maximize Conversions / tCPA'ya geçişi değerlendir",
        "pri": "Fırsat",
    },
    {
        "id": "PACING_LOW",
        "metric": "spend_pace_pct",
        "op": "<",
        "threshold": 70,
        "action": "Harcama düşük pacing: bütçe/teklif artır veya hedef genişlet",
        "pri": "Orta",
    },
    {
        "id": "PACING_HIGH",
        "metric": "spend_pace_pct",
        "op": ">",
        "threshold": 120,
        "action": "Aşırı harcama: günlük tavanı/teklifi düşür",
        "pri": "Risk",
    },
]


# ---- Rakipler (izleme) -----------------------------------------------------
COMPETITORS = [
    {
        "rakip": "Bülbül Yuvası Hotel",
        "konum": "Eski Foça merkez/sahil",
        "vurgu": "merkezi konum, huzur",
        "karsi_mesaj": "köy sessizliği + miras",
        "izle": "fiyat, yorum, IG kreatif, Booking sıralama",
    },
    {
        "rakip": "Huri Nuri Hotel",
        "konum": "Eski Foça, denize yürüme",
        "vurgu": "konum + butik",
        "karsi_mesaj": "Yeni Foça'ya yakın özel kaçış + köy kahvaltısı",
        "izle": "paket/erken rez., yorum, sosyal aktiflik",
    },
    {
        "rakip": "Foça Ensar Otel",
        "konum": "Foça",
        "vurgu": "aile/uygun",
        "karsi_mesaj": "taş konak deneyimi + Ege-Antakya mutfağı",
        "izle": "fiyat konumu, OTA görünürlük, /spy reklam",
    },
    {
        "rakip": "La Petra",
        "konum": "Foça (taş mimari + avlu)",
        "vurgu": "taş mimari, sakin avlu, samimi hizmet",
        "karsi_mesaj": "köy + miras + 200 kişi etkinlik + evcil dostu",
        "izle": "fiyat, yorum, IG kreatif (Haz 2026 web-reach: direkt taş-butik rakip)",
    },
    {
        "rakip": "Griffon Hotel Foça",
        "konum": "Foça sahil",
        "vurgu": "tarihi doku, güçlü mutfak, 4 mevsim",
        "karsi_mesaj": "köy kahvaltısı + Ege-Antakya mutfağı + çatı terası",
        "izle": "menü/mutfak iletişimi, yorum, sezon fiyat (Haz 2026 web-reach)",
    },
    {
        "rakip": "Dionysos 1789 Boutique Hotel",
        "konum": "Foça",
        "vurgu": "butik, tarihi yapı",
        "karsi_mesaj": "köy konumu + miras + komisyonsuz direkt",
        "izle": "OTA görünürlük, paket, yorum (Haz 2026 web-reach)",
    },
    {
        "rakip": "OTA'lar (trivago/Booking/...)",
        "konum": "online",
        "vurgu": "marka terimini kapma",
        "karsi_mesaj": "Marka Search + GBP + komisyonsuz",
        "izle": "marka SERP'te OTA üstte mi, parite, yorum",
    },
]

# ---- Sosyal kanallar + içerik takvimi haftalık şablonu ---------------------
CHANNELS = ["Instagram", "Facebook", "TikTok", "LinkedIn", "X", "Google İşletme"]
# Haftalık plan: gün_index(0=Pzt) -> [(kanal, konsept_key, format)]
WEEK_PLAN = {
    0: [
        ("Instagram", "Konsept1-TasKonak", "Reels 9:16"),
        ("X", "Konsept1-TasKonak", "Metin+link"),
        ("Google İşletme", "Konsept5-WhatsApp", "Post"),
    ],
    1: [
        ("TikTok", "Konsept3-Kahvalti", "Video 9:16"),
        ("Facebook", "Konsept3-Kahvalti", "Feed 4:5"),
    ],
    2: [
        ("Instagram", "Konsept2-Manzara", "Feed 4:5"),
        ("LinkedIn", "Konsept1-TasKonak", "Kurumsal/etkinlik"),
    ],
    3: [
        ("Instagram", "Konsept5-WhatsApp", "Stories 9:16"),
        ("X", "Konsept5-WhatsApp", "Metin+link"),
    ],
    4: [
        ("TikTok", "Konsept2-Manzara", "Video 9:16"),
        ("Facebook", "Konsept2-Manzara", "Feed 4:5"),
        ("Google İşletme", "Konsept3-Kahvalti", "Post"),
    ],
    5: [
        ("Instagram", "Konsept4-Evcil", "Reels 9:16"),
        ("X", "Konsept4-Evcil", "Metin+link"),
    ],
    6: [
        ("Instagram", "Konsept3-Kahvalti", "Feed 4:5"),
        ("TikTok", "Konsept1-TasKonak", "Video 9:16"),
    ],
}
PEAK_TIMES = {
    "Instagram": "19:30",
    "Facebook": "20:00",
    "TikTok": "19:00",
    "LinkedIn": "09:30",
    "X": "11:00",
    "Google İşletme": "10:00",
}


# ---- Apify actor reçeteleri (free-tier, pay-per-event) ----------------------
# MCP akışı: search-actors -> fetch-actor-details -> call-actor -> get-dataset-items.
# Free plan ~$5/ay kredi; aşağıdaki maliyetler sonuç başına (çok düşük).
APIFY_ACTORS = [
    {
        "gorev": "Kendi Google yorumları (izle)",
        "actor": "compass/Google-Maps-Reviews-Scraper",
        "girdi": "startUrls=[GBP/Maps URL], maxReviews=20, reviewsSort=newest",
        "maliyet": "$0.0006/yorum",
    },
    {
        "gorev": "Rakip Google yorumları",
        "actor": "compass/Google-Maps-Reviews-Scraper",
        "girdi": "startUrls=[rakip Maps URL'leri], maxReviews=10",
        "maliyet": "$0.0006/yorum",
    },
    {
        "gorev": "TripAdvisor yorumları (kendi+rakip)",
        "actor": "maxcopell/tripadvisor-reviews",
        "girdi": "startUrls=[TA URL], maxItemsPerQuery=20",
        "maliyet": "$0.005/yorum",
    },
    {
        "gorev": "Booking rakip fiyat (Foça)",
        "actor": "santamaria-automations/booking-com-scraper",
        "girdi": "destination='Foca', checkin, checkout, maxResults=15",
        "maliyet": "$0.003/otel",
    },
    {
        "gorev": "Marka SERP sıralama ('kozbeyli')",
        "actor": "scraperlink/google-search-results-serp-scraper",
        "girdi": "keyword='kozbeyli konağı', country='tr'",
        "maliyet": "$0.0005/SERP",
    },
    {
        "gorev": "Genel web okuma (ajan/RAG)",
        "actor": "apify/rag-web-browser",
        "girdi": "query=URL veya arama, maxResults=3",
        "maliyet": "sonuç başına",
    },
]
# Doğrulanan canlı listeleme URL'leri (rag-web-browser run 8gcfVqcb..., Haz 2026):
APIFY_LIVE_URLS = {
    "tripadvisor": "https://www.tripadvisor.com.tr/Hotel_Review-g10920533-d4298328-Reviews-Kozbeyli_KonagI-Kozbeyli_Foca_Izmir_Province_Turkish_Aegean_Coast.html",
    "obilet": "https://www.obilet.com/otel/kozbeyli-konagi",
    "hotels_com": "https://tr.hotels.com/ho702017/kozbeyli-konagi-foca-turkiye/",
}


# ---- AEO/GEO (AI motorlarinda gorunurluk) ----------------------------------
AEO_CLUSTERS = [
    {
        "kume": "A Bilgilendirme",
        "ornek": "Kozbeyli köyü nerede? / kaç odalı (16)",
        "hedef": "/deneyimler, ana",
    },
    {
        "kume": "B Ticari",
        "ornek": "Foça butik otel fiyatları / müsaitlik",
        "hedef": "/odalar",
    },
    {
        "kume": "C Karşılaştırma",
        "ornek": "Foça mı Alaçatı mı? / butik mi tatil köyü mü?",
        "hedef": "yeni sayfa",
    },
    {
        "kume": "D Konum/yerel",
        "ornek": "İzmir Havalimanı'na uzaklık (~82 km) / nasıl gidilir",
        "hedef": "/lokasyon, yeni",
    },
    {
        "kume": "E Güven",
        "ornek": "Aile uygun mu? Evcil? Ödeme güvenli mi?",
        "hedef": "/sss",
    },
    {
        "kume": "F Deneyimsel",
        "ornek": "Kahvaltı dahil mi? Havuz var mı? (resort yok)",
        "hedef": "/gastronomi, /sss",
    },
    {
        "kume": "G Mevsimsel",
        "ornek": "Ne zaman gidilir (May–Eki)? Kışın açık mı?",
        "hedef": "yeni sayfa",
    },
    {
        "kume": "H Etkinlik",
        "ornek": "Foça kır düğünü mekanı / paket fiyatı?",
        "hedef": "/organizasyonlar",
    },
]
AEO_SCHEMA_CHECKLIST = [
    {
        "sema": "Hotel/LodgingBusiness",
        "sayfa": "Ana sayfa",
        "dosya": "aeo/schema/hotel.jsonld",
    },
    {
        "sema": "HotelRoom (+Offer)",
        "sayfa": "Oda detay (7)",
        "dosya": "aeo/schema/hotelroom-ornek.jsonld",
    },
    {
        "sema": "Restaurant",
        "sayfa": "/gastronomi",
        "dosya": "aeo/schema/restaurant.jsonld",
    },
    {"sema": "FAQPage", "sayfa": "/sss", "dosya": "aeo/schema/faqpage.jsonld"},
    {
        "sema": "BreadcrumbList",
        "sayfa": "tüm iç sayfalar",
        "dosya": "aeo/schema/breadcrumb-ornek.jsonld",
    },
]


# ---- Sezon kampanya planlari -----------------------------------------------
SEASONS = [
    {
        "sezon": "Yüksek (Haz–Eyl)",
        "tema": "manzara / kahvaltı / aile",
        "kanal": "Marka koru + Meta prospecting + retargeting",
        "butce": "tam; DOLU tarihte kıs",
        "teklif": "min indirim; deneyim öne",
        "kpi": "doluluk + blended ROAS",
    },
    {
        "sezon": "Düşük (Kas–Mar)",
        "tema": "hafta içi sakin kaçış + WhatsApp",
        "kanal": "dar non-brand kıs; WhatsApp + retargeting + içerik/SEO",
        "butce": "kıs; WhatsApp ağırlık",
        "teklif": "hafta içi / erken rez. avantajı",
        "kpi": "lead + direkt rezervasyon",
    },
    {
        "sezon": "Geçiş (Nis–May, Eki)",
        "tema": "balayı/çift, evcil, köy kahvaltısı",
        "kanal": "prospecting + içerik + email",
        "butce": "orta",
        "teklif": "2 gece + kahvaltı paketi",
        "kpi": "yeni kitle + CVR",
    },
]

# ---- Dönüşüm hunisi (funnel) -----------------------------------------------
FUNNEL_STAGES = [
    {
        "asama": "1 Farkındalık",
        "kanal": "Meta prospecting, TikTok/Reels, içerik/SEO, AEO",
        "kpi": "erişim, CTR, ziyaret",
        "kayip": "zayıf hook",
        "fix": "creatives/ + aeo/",
    },
    {
        "asama": "2 İlgi/Değerlendirme",
        "kanal": "site /odalar /gastronomi, Instagram, yorumlar",
        "kpi": "oda görüntüleme, süre",
        "kayip": "şema/yorum yok",
        "fix": "aeo/ + profiles/",
    },
    {
        "asama": "3 Niyet",
        "kanal": "Marka Search, retargeting, WhatsApp",
        "kpi": "begin_checkout, WhatsApp lead",
        "kayip": "OTA savunmasız",
        "fix": "campaigns/ + whatsapp/",
    },
    {
        "asama": "4 Rezervasyon",
        "kanal": "HMS motoru, WhatsApp",
        "kpi": "purchase, CVR",
        "kayip": "cross-domain ölçüm yok",
        "fix": "tracking/implementation + fixes/",
    },
    {
        "asama": "5 Sadakat/Tekrar",
        "kanal": "email, WhatsApp takip, yorum",
        "kpi": "tekrar rez., yorum, NPS",
        "kayip": "takip yok",
        "fix": "email/ + whatsapp/ + fixes/06",
    },
]

# ---- Teklif / paket şablonları ---------------------------------------------
OFFERS = [
    {
        "teklif": "Hafta içi sakin kaçış",
        "kosul": "Pzt–Per, min 2 gece",
        "mesaj": "sessizlik + manzara",
        "kanal": "Meta / WhatsApp / email",
    },
    {
        "teklif": "Erken rezervasyon",
        "kosul": "≥30 gün önce",
        "mesaj": "yer garanti + avantaj",
        "kanal": "Marka Search / email",
    },
    {
        "teklif": "Balayı / çift paketi",
        "kosul": "2 gece + kahvaltı + karşılama",
        "mesaj": "romantik köy kaçışı",
        "kanal": "Meta / Instagram",
    },
    {
        "teklif": "Evcil dostu",
        "kosul": "ücretsiz + mama kabı",
        "mesaj": "patiler davetli",
        "kanal": "Meta / sosyal",
    },
    {
        "teklif": "Köy kahvaltısı (günübirlik)",
        "kosul": "rezervasyonla",
        "mesaj": "organik sofra",
        "kanal": "GBP / Instagram / yerel",
    },
]


# ---- web (frontend) kontrol listesi ----------------------------------------
WEB_CHECKLIST = [
    {
        "alan": "Performans",
        "hedef": "Lighthouse ≥90 mobil; LCP<2.5s INP<200ms CLS<0.1",
        "kaynak": "web/performance",
    },
    {
        "alan": "Erişilebilirlik (WCAG AA)",
        "hedef": "a11y ≥95; klavye + kontrast 4.5:1 + alt + focus",
        "kaynak": "web/accessibility",
    },
    {
        "alan": "Meta / OpenGraph",
        "hedef": "OG/Twitter/canonical/hreflang + OG görsel",
        "kaynak": "web/meta",
    },
    {
        "alan": "PWA",
        "hedef": "geçerli manifest + SW + ikon (installable)",
        "kaynak": "web/pwa",
    },
    {
        "alan": "Responsive / mobil",
        "hedef": "viewport (zoom açık), 44px hedef, yatay scroll yok",
        "kaynak": "web/responsive",
    },
    {
        "alan": "Animasyon",
        "hedef": "reduced-motion saygı; sadece transform/opacity",
        "kaynak": "web/animations",
    },
]


# ---- B2B kurumsal (Aliağa sanayi) -------------------------------------------
B2B_TARGETS = [
    {
        "sektor": "Rafineri / Petrokimya",
        "cap_firma": "STAR Rafineri, Petkim, SOCAR, Tüpraş",
        "kullanim": "yönetici konaklama + etkinlik + müşteri ağırlama",
        "oncelik": "Yüksek",
    },
    {
        "sektor": "Demir-çelik / metal",
        "cap_firma": "İzmir Demir Çelik, Habaş, Ege Çelik, Kocaer",
        "kullanim": "yüklenici barınma (bakım-duruş) + toplantı",
        "oncelik": "Yüksek",
    },
    {
        "sektor": "Gemi söküm / liman",
        "cap_firma": "MKE + özel yatlar, Nemrut limanları",
        "kullanim": "armatör/sörveyör ağırlama + premium konaklama",
        "oncelik": "Orta",
    },
    {
        "sektor": "OSB / serbest bölge",
        "cap_firma": "Aliağa OSB (72 firma), Menemen OSB",
        "kullanim": "proje ekibi konaklama + toplantı + yemek",
        "oncelik": "Orta",
    },
]
B2B_PACKAGES = [
    {
        "paket": "Toplantı / Eğitim offsite",
        "icerik": "salon + ekipman + 2 kahve arası + öğle",
        "hedef": "departman/proje",
    },
    {
        "paket": "24 saat (konaklamalı)",
        "icerik": "DDR + akşam yemeği + 1 gece + kahvaltı",
        "hedef": "toplantı + konaklama",
    },
    {
        "paket": "Kurumsal yemek / gala",
        "icerik": "200 kişi + kişi başı menü",
        "hedef": "yıl sonu / gala / iftar",
    },
    {
        "paket": "Yönetici / müşteri ağırlama",
        "icerik": "premium + gizli + az kişi + transfer",
        "hedef": "armatör/alıcı/denetçi",
    },
    {
        "paket": "Yüklenici kampı",
        "icerik": "uzun toplu konaklama + tam pansiyon + servis",
        "hedef": "bakım-duruş ekibi",
    },
]
B2B_LOCATION = "Aliağa sanayi kalbine ~25–30 km (30–40 dk). Foça/Kozbeyli."

# ---- ÖLÇÜM DURUMU (tarayıcıda canlı doğrulandı, Haz 2026) -------------------
# Kaynak: www.kozbeylikonagi.com canlı beacon + Google Ads hesabı okuması.
# `kads tracking` bunu raporlar. CANLI=çalışıyor, EKSİK=kurulmalı, KAPALI=ayar kapalı.
TRACKING_STATE = [
    {
        "bilesen": "GTM container (GTM-KCG6B4MJ)",
        "durum": "CANLI",
        "detay": "Sitede yüklü + çalışıyor",
        "aksiyon": "Erişimi DOĞRULA (eski ajansta olabilir)",
    },
    {
        "bilesen": "GA4 Config (G-V3R66C3MEF)",
        "durum": "EKSİK",
        "detay": "GTM içinde GA4 Config etiketi yok",
        "aksiyon": "GTM'e GA4 Config (All Pages) ekle",
    },
    {
        "bilesen": "Google Ads dönüşüm (AW-800024713)",
        "durum": "EKSİK",
        "detay": "GTM'de Conversion Linker/Conversion yok → Ads 0 dönüşüm",
        "aksiyon": "Linker (All Pages) + Conversion (begin_checkout)",
    },
    {
        "bilesen": "Meta Pixel (1781546559309505)",
        "durum": "CANLI",
        "detay": "Tek pixel; PageView + InitiateCheckout ateşliyor",
        "aksiyon": "-",
    },
    {
        "bilesen": "Meta Purchase (tamamlanan rezervasyon)",
        "durum": "EKSİK",
        "detay": "Rezervasyon hmshotel.net'te biter, pixel orada yok",
        "aksiyon": "HMS onay sayfasına Purchase (value+currency)",
    },
    {
        "bilesen": "Meta Advanced Matching",
        "durum": "KAPALI",
        "detay": "Beacon'da kullanıcı-verisi yok",
        "aksiyon": "Events Manager → Automatic Advanced Matching AÇ (1 tık)",
    },
    {
        "bilesen": "Site event'leri (begin_checkout / InitiateCheckout)",
        "durum": "ATIYOR",
        "detay": "Tetikleyiciler sitede hazır",
        "aksiyon": "-",
    },
    {
        "bilesen": "Conversions API (CAPI)",
        "durum": "YOK",
        "detay": "Sadece tarayıcı-pixel",
        "aksiyon": "Opsiyonel: sunucu-taraflı CAPI + event dedup",
    },
]


# ---- Reklam teslim paketi (#2-#10) durum özeti ------------------------------
# Tam metin: docs/REKLAM-TESLIM-PAKETI.md · Skill: skills/ads-delivery/SKILL.md
# durum: HAZIR (repoda uygulanabilir) | ÖLÇÜM BEKLİYOR (canlı tag şart) | AKSİYON (elle iş)
DELIVERY_STATUS = [
    {"no": "#2", "baslik": "Strateji (kanal rolleri + bütçe)", "durum": "HAZIR",
     "konum": "docs/REKLAM-TESLIM-PAKETI.md · kads allocate", "aksiyon": "-"},
    {"no": "#3", "baslik": "12 kreatif (R/K/T/M/D) + takvim", "durum": "HAZIR",
     "konum": "creatives/ · docs/REKLAM-TESLIM-PAKETI.md", "aksiyon": "üret + A/B test"},
    {"no": "#4", "baslik": "Keyword dosyası + negatifler", "durum": "HAZIR",
     "konum": "campaigns/google-editor/03_keywords.csv · kads keywords", "aksiyon": "-"},
    {"no": "#5", "baslik": "Tracking QA (18 madde, skor 80+)", "durum": "ÖLÇÜM BEKLİYOR",
     "konum": "kads tracking · golive/GTM-KURULUM.html", "aksiyon": "GTM GA4/Ads etiketi + test rezervasyon"},
    {"no": "#6", "baslik": "Landing page QA + eşleme", "durum": "HAZIR",
     "konum": "docs/26-site-onpage-seo-denetimi.md", "aksiyon": "taze yorum hızı"},
    {"no": "#7", "baslik": "WhatsApp satış (şablon+offline conv)", "durum": "HAZIR",
     "konum": "docs/REKLAM-TESLIM-PAKETI.md · kads conversions", "aksiyon": "şablonları kur"},
    {"no": "#8", "baslik": "Haftalık optimizasyon (8 kural)", "durum": "HAZIR",
     "konum": "kads monitor · kads rules", "aksiyon": "-"},
    {"no": "#9", "baslik": "Risk listesi (10)", "durum": "HAZIR",
     "konum": "docs/REKLAM-TESLIM-PAKETI.md", "aksiyon": "-"},
    {"no": "#10", "baslik": "30 gün planı", "durum": "ÖLÇÜM KAPISI",
     "konum": "docs/REKLAM-TESLIM-PAKETI.md", "aksiyon": "Gün 1-3 ölçüm önce"},
]


# ---- AEO/GEO: AI görünürlük test sorguları + skor -------------------------
# Haftalık 4 platformda (ChatGPT/Perplexity/Gemini/Claude) test edilir.
# Değerleme: 2=önerildi/kaynak, 1=bahsedildi, 0=yok. Bkz. docs/aeo-strategy.md
AEO_TEST_QUERIES = [
    {"sorgu": "Foça'da tarihi taş konak otel", "kategori": "butik", "dil": "tr"},
    {"sorgu": "Kozbeyli Konağı nedir nerede", "kategori": "marka", "dil": "tr"},
    {"sorgu": "Foça butik otel önerisi", "kategori": "butik", "dil": "tr"},
    {"sorgu": "İzmir'de köy düğünü mekanı", "kategori": "organizasyon", "dil": "tr"},
    {"sorgu": "Foça'da kahvaltısı güzel otel", "kategori": "kahvaltı", "dil": "tr"},
    {"sorgu": "Foça'ya yakın sakin otel", "kategori": "butik", "dil": "tr"},
    {"sorgu": "Foça mı Alaçatı mı nerede kalınır", "kategori": "karşılaştırma", "dil": "tr"},
    {"sorgu": "Foça'da çiftler için romantik otel", "kategori": "romantik", "dil": "tr"},
    {"sorgu": "evcil hayvan kabul eden Foça oteli", "kategori": "evcil", "dil": "tr"},
    {"sorgu": "Foça'da Ege mutfağı restoran", "kategori": "restoran", "dil": "tr"},
    {"sorgu": "İzmir taş konak otel öner", "kategori": "butik", "dil": "tr"},
    {"sorgu": "Yeni Foça'da butik konaklama", "kategori": "bölge", "dil": "tr"},
    {"sorgu": "Foça'da köy kahvaltısı nerede yapılır", "kategori": "kahvaltı", "dil": "tr"},
    {"sorgu": "Foça'da canlı müzikli restoran", "kategori": "restoran", "dil": "tr"},
    {"sorgu": "Foça'da nişan kına mekanı", "kategori": "organizasyon", "dil": "tr"},
    {"sorgu": "best boutique hotel near Foça Turkey", "kategori": "butik", "dil": "en"},
    {"sorgu": "historic stone house hotel Izmir Turkey", "kategori": "butik", "dil": "en"},
    {"sorgu": "where to stay in Foça village Turkey", "kategori": "bölge", "dil": "en"},
    {"sorgu": "pet friendly boutique hotel Aegean Turkey", "kategori": "evcil", "dil": "en"},
    {"sorgu": "Foça vs Alacati where to stay", "kategori": "karşılaştırma", "dil": "en"},
]

# Haftalık ölçümde Kozbeyli ile karşılaştırılacak rakipler (share of voice).
AEO_COMPETITORS_TRACK = ["Bülbül Yuvası Hotel", "Huri Nuri Hotel", "Foça Ensar Otel"]

AEO_PLATFORMS = ["ChatGPT", "Perplexity", "Gemini", "Claude"]


def aeo_visibility_score(rows: list) -> dict:
    """Doldurulmuş alıntı-testi satırlarından AI görünürlük skorunu hesaplar.

    rows: her biri en az {ChatGPT,Perplexity,Gemini,Claude} anahtarlı dict
    (değerler 0/1/2 veya boş). Döndürür: {overall_pct, per_platform, filled, total_cells}.
    Boş hücre ölçülmemiş sayılır (paydaya girmez) — dürüst kısmi skor.
    """
    per = {p: {"sum": 0, "max": 0} for p in AEO_PLATFORMS}
    filled = 0
    for r in rows:
        for p in AEO_PLATFORMS:
            v = str(r.get(p, "")).strip()
            if v == "":
                continue
            try:
                val = int(float(v.replace(",", ".")))
            except (TypeError, ValueError):
                continue
            val = max(0, min(2, val))
            per[p]["sum"] += val
            per[p]["max"] += 2
            filled += 1
    total_sum = sum(p["sum"] for p in per.values())
    total_max = sum(p["max"] for p in per.values())
    overall = round(total_sum / total_max * 100, 1) if total_max else 0.0
    per_platform = {
        p: (round(d["sum"] / d["max"] * 100, 1) if d["max"] else None)
        for p, d in per.items()
    }
    return {
        "overall_pct": overall,
        "per_platform": per_platform,
        "filled": filled,
        "total_cells": len(rows) * len(AEO_PLATFORMS),
    }
