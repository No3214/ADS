#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kads.data_growth — büyüme katmanı verisi (tek kaynak, data.py/data_ext.py'yi tamamlar).

Kapsam: Performance Max + Demand Gen (yeni Google formatları), Google remarketing
+ RLSA akışları, UTM standardı + matris, attribution modeli, bütçe dağıtım matrisi,
sezon strateji detayı. CLI bunları salt-okunur gösterir; yazma/harcama guardrail'li.
Tüm sözlük listeleri core.emit ile birebir uyumlu (düz alan adları).
"""
from __future__ import annotations

# =============================================================================
# 1) PERFORMANCE MAX (PMax) — tek kampanya, tüm Google envanteri
#    (Search + Display + YouTube + Discover + Gmail + Maps). Asset-group temelli.
# =============================================================================
PMAX_ASSET_GROUPS = [
    {"grup": "Butik Konaklama / Manzara", "tema": "taş konak, huzur, doğa, çift/aile",
     "final_url": "https://www.kozbeylikonagi.com/odalar", "tema_kitle_sinyali": "Lüks gezgin + Foça/İzmir tatil arayanlar + site ziyaretçileri",
     "oncelik": "Yüksek"},
    {"grup": "Köy Kahvaltısı / Gastronomi", "tema": "organik sofra, yöresel, günübirlik",
     "final_url": "https://www.kozbeylikonagi.com/gastronomi", "tema_kitle_sinyali": "Yeme-içme ilgisi + yerel (İzmir 60km) + restoran arayanlar",
     "oncelik": "Orta"},
    {"grup": "Düğün / Etkinlik (200 kişi)", "tema": "kır düğünü, kına, davet, bahçe",
     "final_url": "https://www.kozbeylikonagi.com/organizasyonlar", "tema_kitle_sinyali": "Nişanlı/düğün planlayan + etkinlik mekanı arayanlar",
     "oncelik": "Yüksek"},
    {"grup": "Kurumsal / B2B (Aliağa)", "tema": "toplantı, offsite, yönetici konaklama, gala",
     "final_url": "https://www.kozbeylikonagi.com/organizasyonlar", "tema_kitle_sinyali": "Aliağa/İzmir sanayi + İK/Satınalma profilleri + LinkedIn benzeri ilgi",
     "oncelik": "Orta"},
]

# PMax varlık limitleri (Google zorunlulukları). count = önerilen adet.
PMAX_ASSET_SPECS = [
    {"varlik": "Başlık (headline)", "adet": "8-15", "limit": "≤30 karakter", "not": "en az 3 zorunlu; çoğu güçlü"},
    {"varlik": "Uzun başlık (long headline)", "adet": "3-5", "limit": "≤90 karakter", "not": "en az 1 zorunlu"},
    {"varlik": "Açıklama (description)", "adet": "4-5", "limit": "≤90 (1 adet ≤60)", "not": "en az 2 zorunlu"},
    {"varlik": "İşletme adı", "adet": "1", "limit": "≤25 karakter", "not": "Kozbeyli Konağı"},
    {"varlik": "Görsel yatay 1.91:1", "adet": "≥3", "limit": "≥600x314 (1200x628 ideal)", "not": "yüksek kaliteli"},
    {"varlik": "Görsel kare 1:1", "adet": "≥3", "limit": "≥300x300 (1200x1200 ideal)", "not": "zorunlu"},
    {"varlik": "Görsel dikey 4:5", "adet": "≥1", "limit": "≥480x600", "not": "mobil/Discover için"},
    {"varlik": "Logo kare 1:1", "adet": "1", "limit": "≥128x128", "not": "yatay 4:1 logo da ekle"},
    {"varlik": "Video", "adet": "≥1", "limit": "≥10 sn (YouTube)", "not": "yoksa Google otomatik üretir; kendi videon daha iyi"},
]

PMAX_SETUP = [
    {"adim": "1", "is": "Dönüşüm hazır olsun", "detay": "purchase + generate_lead Google Ads'e akmalı (tracking/). PMax dönüşüme göre öğrenir."},
    {"adim": "2", "is": "Kampanya tipi: Performance Max", "detay": "Hedef: Satışlar/Potansiyel müşteri. tICKET: rezervasyon + WhatsApp lead."},
    {"adim": "3", "is": "Asset group başına 1 tema", "detay": "Yukarıdaki 4 grup; her grup kendi URL + görsel + kitle sinyali."},
    {"adim": "4", "is": "Kitle sinyali ver (audience signal)", "detay": "Kendi listelerin (site ziyaretçi, CRM) + ilgi alanları. Sinyal = hızlandırıcı, kısıt değil."},
    {"adim": "5", "is": "URL genişletme KAPALI test et", "detay": "Marka trafiğini Search'ten çalmasın diye başta Final URL expansion kapat."},
    {"adim": "6", "is": "Marka hariç tut", "detay": "Brand exclusions ekle; PMax marka aramalarını ucuza yazıp raporu şişirmesin."},
    {"adim": "7", "is": "Bütçe + 2-4 hafta öğrenme", "detay": "Günlük bütçeyi guardrail tavanına göre koy; erken kapatma, öğrenmeyi bekle."},
]
PMAX_NOTE = ("PMax kara kutudur: marka aramasını yutabilir ve raporu şişirir. KORUMA: marka "
             "hariç tutma (brand exclusions) + URL genişletme kapalı + ayrı Marka Search kampanyası. "
             "Düşük bütçede önce Search+Meta otur, PMax'i ay 2-3'te aç (docs/05).")

# =============================================================================
# 2) DEMAND GEN — görsel/keşif kampanyası (YouTube + Discover + Gmail)
#    Talep yaratma; otelin güçlü görselleriyle üst-orta huni.
# =============================================================================
DEMAND_GEN_FORMATS = [
    {"format": "Tekli görsel", "oran": "1.91:1 + 1:1 + 4:5", "yerlesim": "Discover, Gmail, YouTube feed", "kullanim": "manzara/oda/sofra tek kare"},
    {"format": "Karusel", "oran": "1.91:1 veya 1:1 (2-10 kart)", "yerlesim": "Discover, Gmail", "kullanim": "oda turu / paket / etkinlik adımları"},
    {"format": "Video", "oran": "yatay/kare/dikey", "yerlesim": "YouTube (in-feed, Shorts)", "kullanim": "reels/shotlist videoları (creatives/)"},
]
DEMAND_GEN_SPECS = [
    {"varlik": "Görsel yatay 1.91:1", "limit": "1200x628 (≥600x314)", "not": "ana kare"},
    {"varlik": "Görsel kare 1:1", "limit": "1200x1200 (≥300x300)", "not": "feed"},
    {"varlik": "Görsel dikey 4:5", "limit": "960x1200", "not": "mobil"},
    {"varlik": "Başlık", "limit": "≤40 karakter", "adet": "≥1 (5'e kadar)"},
    {"varlik": "Açıklama", "limit": "≤90 karakter", "adet": "≥1 (5'e kadar)"},
    {"varlik": "İşletme adı", "limit": "≤25", "adet": "1"},
    {"varlik": "CTA", "limit": "menüden", "adet": "Rezervasyon yap / Daha fazla bilgi"},
]
DEMAND_GEN_AUDIENCES = [
    {"kitle": "Benzer kitle (lookalike)", "kaynak": "Site dönüşenler / CRM", "huni": "Üst", "not": "en güçlü prospecting sinyali"},
    {"kitle": "Özel niyet (custom intent)", "kaynak": "Aratılan kelimeler + rakip siteler", "huni": "Orta", "not": "Foça otel/düğün arayanlar"},
    {"kitle": "İlgi alanları", "kaynak": "Seyahat, gurme, düğün", "huni": "Üst", "not": "geniş farkındalık"},
    {"kitle": "Remarketing", "kaynak": "Site/YouTube/etkileşim", "huni": "Alt", "not": "geri kazanım — ayrı düşük bütçe"},
]
DEMAND_GEN_NOTE = ("Demand Gen = sosyalin Google karşılığı; görsel/video ile talep yaratır. "
                   "Otelin en iyi kareleri (creatives/) burada çalışır. Üst-orta huni; alt huniyi "
                   "Marka Search + retargeting kapatır. Meta prospecting ile çakışmayı izleyip dengele.")

# =============================================================================
# 3) GOOGLE REMARKETING + RLSA — geri kazanım (Meta retargeting'i tamamlar)
# =============================================================================
GOOGLE_REMARKETING = [
    {"liste": "Tüm site ziyaretçileri", "uyelik_gun": 540, "min_boyut": "Display 100 / Search 1000",
     "kullanim": "Display + Demand Gen geniş geri kazanım", "oncelik": "Orta"},
    {"liste": "Oda/fiyat görüntüleyenler", "uyelik_gun": 90, "min_boyut": "1000 (Search)",
     "kullanim": "RLSA + PMax sinyali + Display", "oncelik": "Yüksek"},
    {"liste": "Rezervasyonu yarıda bırakanlar (begin_checkout, no purchase)", "uyelik_gun": 30, "min_boyut": "100 (Display)",
     "kullanim": "agresif retargeting — en sıcak", "oncelik": "Yüksek"},
    {"liste": "Geçmiş misafirler (purchase)", "uyelik_gun": 540, "min_boyut": "CRM/Customer Match",
     "kullanim": "tekrar rez. + sezon teklifi + benzer kitle tohumu", "oncelik": "Yüksek"},
    {"liste": "Etkinlik/düğün sayfası", "uyelik_gun": 180, "min_boyut": "100 (Display)",
     "kullanim": "uzun karar süreci — nazik hatırlatma", "oncelik": "Orta"},
    {"liste": "B2B/organizasyon sayfası", "uyelik_gun": 180, "min_boyut": "100 (Display)",
     "kullanim": "kurumsal karar süreci + LinkedIn outreach ile birlikte", "oncelik": "Orta"},
    {"liste": "YouTube/video izleyenler", "uyelik_gun": 180, "min_boyut": "kanal bağlı",
     "kullanim": "Demand Gen + Display geri kazanım", "oncelik": "Düşük"},
]
RLSA_RULES = [
    {"senaryo": "Marka Search + 'oda görüntüleyen' listesi", "aksiyon": "Teklif +%20–40", "neden": "sıcak; dönüşür"},
    {"senaryo": "Non-brand Search + 'tüm ziyaretçi'", "aksiyon": "Teklif +%10–20 / geniş kelimeye izin", "neden": "bilen kullanıcı daha güvenli"},
    {"senaryo": "'Rezervasyonu bırakan' tüm Search", "aksiyon": "Teklif +%30–50", "neden": "en yüksek niyet"},
    {"senaryo": "Geçmiş misafir + jenerik kelime", "aksiyon": "Özel reklam metni (tekrar gel)", "neden": "sadakat mesajı"},
]
GOOGLE_REMARKETING_NOTE = ("Remarketing yalnız ay 2+ ve liste min boyuta ulaşınca açılır (docs/03). "
                           "Etiket: Google Ads tag + GA4 kitleleri (tracking/). Customer Match için "
                           "rıza/KVKK uyumlu liste şart. Meta retargeting ile mesajı bölme: Google=arama "
                           "niyeti yakala, Meta=görsel geri kazanım. Frekans sınırı koy (bunaltma).")

# Kanal arası remarketing akışı (kullanıcı yolculuğu)
REMARKETING_FLOW = [
    {"tetik": "Siteye girdi, çıktı", "1_kanal": "Meta retargeting (görsel)", "2_kanal": "Google Display", "mesaj": "manzara + 'seni bekliyoruz'"},
    {"tetik": "Oda/fiyat gördü", "1_kanal": "RLSA (Search teklif +)", "2_kanal": "Meta dinamik", "mesaj": "oda + müsaitlik + sosyal kanıt"},
    {"tetik": "Rezervasyonu bıraktı", "1_kanal": "Meta retargeting agresif", "2_kanal": "RLSA +%40", "mesaj": "aciliyet + WhatsApp + (varsa) avantaj"},
    {"tetik": "Rezervasyon yaptı", "1_kanal": "Hariç tut (suppression)", "2_kanal": "email/WhatsApp upsell", "mesaj": "teşekkür + ek hizmet + tekrar"},
    {"tetik": "Misafir oldu, ayrıldı", "1_kanal": "email sıra akışı", "2_kanal": "sezon Meta/Customer Match", "mesaj": "yorum iste + tekrar gel teklifi"},
]


# =============================================================================
# 4) UTM STANDARDI + matris — her kanalda tutarli etiketleme = temiz attribution
#    Kural: kucuk harf, bosluk yok (tire), tutarli. utm_term=kelime, utm_content=varyant.
# =============================================================================
UTM_RULES = [
    {"kural": "Kucuk harf", "ornek": "utm_source=meta (Meta degil)", "neden": "GA4 buyuk/kucuk ayrir"},
    {"kural": "Bosluk yok", "ornek": "utm_campaign=yaz-kampanya", "neden": "tire kullan, bosluk/altcizgi karisir"},
    {"kural": "source=platform", "ornek": "google / meta / instagram / email", "neden": "trafigin geldigi yer"},
    {"kural": "medium=tur", "ornek": "cpc / paid_social / email / organic", "neden": "kanal tipi"},
    {"kural": "campaign=amac", "ornek": "brand / pmax / retargeting / yaz-2026", "neden": "kampanya kimligi"},
    {"kural": "term=kelime (Search)", "ornek": "utm_term=foca+otel", "neden": "paid search anahtar kelime"},
    {"kural": "content=varyant", "ornek": "utm_content=rsa-a / reel-01", "neden": "A/B reklam/kreatif ayrimi"},
    {"kural": "Marka Search'i etiketleme", "ornek": "auto-tagging (gclid) yeterli", "neden": "Google Ads zaten gclid ile baglar; UTM gclid'i ezmesin"},
]

# anahtar = kads utm build --channel <anahtar>
UTM_MATRIX = [
    {"anahtar": "google-brand", "kanal": "Google Marka Search", "utm_source": "google", "utm_medium": "cpc", "utm_campaign": "brand", "not": "auto-tag varsa UTM opsiyonel"},
    {"anahtar": "google-nonbrand", "kanal": "Google Non-brand Search", "utm_source": "google", "utm_medium": "cpc", "utm_campaign": "nonbrand", "not": "utm_term=kelime ekle"},
    {"anahtar": "google-pmax", "kanal": "Google Performance Max", "utm_source": "google", "utm_medium": "cpc", "utm_campaign": "pmax", "not": "final URL expansion kapaliyken"},
    {"anahtar": "google-demandgen", "kanal": "Google Demand Gen", "utm_source": "google", "utm_medium": "demandgen", "utm_campaign": "demandgen", "not": "gorsel/video"},
    {"anahtar": "google-display", "kanal": "Google Display/Remarketing", "utm_source": "google", "utm_medium": "display", "utm_campaign": "remarketing", "not": "geri kazanim"},
    {"anahtar": "meta-prospecting", "kanal": "Meta Prospecting", "utm_source": "meta", "utm_medium": "paid_social", "utm_campaign": "prospecting", "not": "utm_content=reel-01 vb."},
    {"anahtar": "meta-retargeting", "kanal": "Meta Retargeting", "utm_source": "meta", "utm_medium": "paid_social", "utm_campaign": "retargeting", "not": "site/checkout terk"},
    {"anahtar": "meta-whatsapp", "kanal": "Meta WhatsApp/Mesaj", "utm_source": "meta", "utm_medium": "paid_social", "utm_campaign": "whatsapp", "not": "lead amac"},
    {"anahtar": "instagram-organic", "kanal": "Instagram (organik/bio)", "utm_source": "instagram", "utm_medium": "social", "utm_campaign": "bio-link", "not": "Linktree/bio"},
    {"anahtar": "email", "kanal": "E-posta", "utm_source": "email", "utm_medium": "email", "utm_campaign": "yaz-2026", "not": "kampanyaya gore degis"},
    {"anahtar": "whatsapp-organic", "kanal": "WhatsApp (organik)", "utm_source": "whatsapp", "utm_medium": "referral", "utm_campaign": "destek", "not": "link paylasiminda"},
    {"anahtar": "gbp", "kanal": "Google Isletme Profili", "utm_source": "gbp", "utm_medium": "organic", "utm_campaign": "profil", "not": "Maps/isletme link"},
    {"anahtar": "tiktok-organic", "kanal": "TikTok (organik)", "utm_source": "tiktok", "utm_medium": "social", "utm_campaign": "bio-link", "not": "bio"},
    {"anahtar": "linkedin-b2b", "kanal": "LinkedIn (B2B outreach)", "utm_source": "linkedin", "utm_medium": "social", "utm_campaign": "b2b-aliaga", "not": "kurumsal"},
]

# =============================================================================
# 5) ATTRIBUTION MODELI — hangi temas donusumu alir; kanal arasi cift sayim cozumu
# =============================================================================
ATTRIBUTION = [
    {"katman": "GA4 raporlama", "model": "Data-driven (DDA)", "pencere": "30 gun tikla / 1 gun gor", "not": "turizmde karar uzun; DDA varsayilan"},
    {"katman": "Google Ads donusum", "model": "Data-driven (DDA)", "pencere": "30 gun", "not": "son-tik degil; tum yolu degerlendir"},
    {"katman": "Meta Ads", "model": "7 gun tikla / 1 gun gor", "pencere": "7-1", "not": "view-through'a supheli yaklas"},
    {"katman": "Kaynak otorite (dedup)", "model": "GA4 = tek gercek", "pencere": "-", "not": "Google+Meta ayni rezervasyonu sayar; GA4'te birlestir"},
    {"katman": "purchase tekillik", "model": "transaction_id (HMS rez. no)", "pencere": "-", "not": "ayni rez. iki kez sayilmaz (tracking/)"},
    {"katman": "Meta CAPI dedup", "model": "event_id eslesme", "pencere": "-", "not": "Pixel+CAPI ayni event_id (tracking/05)"},
    {"katman": "Karar (yonetim)", "model": "Blended CPA/ROAS", "pencere": "aylik", "not": "tek platform metrigine takilma (docs)"},
]
ATTRIBUTION_NOTES = [
    "Cross-domain ZORUNLU: purchase HMS'te ({slug}.hmshotel.net) olur; GA4 cross-domain yoksa yol kopar (tracking/03).",
    "Google ve Meta ayni rezervasyonu kendine yazar -> toplam sisirilir. GA4'u hakem al, blended bak.",
    "View-through (goruntuleme) donusumunu ayri raporla; karari click-through agirlikli ver.",
    "Lookback turizmde uzun: 30 gun tikla mantikli. Kisa pencere yeni talebi olduren gosterir.",
    "UTM tutarsizligi attribution'u bozar -> kads utm ile her linki standart etiketle.",
]


# =============================================================================
# 6) BUTCE DAGITIM MATRISI — 30.000 TL/ay; kanal x huni x ay (PLAN ile tutarli)
#    ay1 = lansman (retargeting kapali), ay2 = oturmus (retargeting acik).
#    Iki ayin da toplami = 30.000 TL (test dogrular).
# =============================================================================
BUDGET_MATRIX = [
    {"kanal": "Meta Prospecting", "huni": "TOF/MOF", "ay1_try": 10500, "ay1_pct": "35%", "ay2_try": 9000, "ay2_pct": "30%", "gerekce": "yeni talep; ay2'de retargeting'e yer ac"},
    {"kanal": "Meta Retargeting", "huni": "BOF/Retention", "ay1_try": 0, "ay1_pct": "0%", "ay2_try": 3000, "ay2_pct": "10%", "gerekce": "liste min boyuta gelince acilir (ay2+)"},
    {"kanal": "Meta WhatsApp/Mesaj", "huni": "BOF", "ay1_try": 4500, "ay1_pct": "15%", "ay2_try": 3000, "ay2_pct": "10%", "gerekce": "nitelikli rezervasyon gorusmesi"},
    {"kanal": "Google Non-brand Search", "huni": "MOF/BOF", "ay1_try": 9000, "ay1_pct": "30%", "ay2_try": 9000, "ay2_pct": "30%", "gerekce": "yuksek niyetli yeni talep"},
    {"kanal": "Google Marka Search", "huni": "BOF", "ay1_try": 4500, "ay1_pct": "15%", "ay2_try": 4500, "ay2_pct": "15%", "gerekce": "marka + OTA savunmasi"},
    {"kanal": "Google Test -> Demand Gen", "huni": "TOF/test", "ay1_try": 1500, "ay1_pct": "5%", "ay2_try": 1500, "ay2_pct": "5%", "gerekce": "ay1 terim testi; ay2 Demand Gen/remarketing"},
]
BUDGET_TOTAL_TRY = 30000  # ay1 ve ay2 ayri ayri bu toplama esit olmali

BUDGET_BY_FUNNEL = [
    {"asama": "TOF Farkindalik", "kanallar": "Meta Prospecting + Demand Gen", "ay2_try": 10500, "pct": "35%", "amac": "yeni kitleye eris"},
    {"asama": "MOF Degerlendirme", "kanallar": "Google Non-brand Search", "ay2_try": 9000, "pct": "30%", "amac": "niyetli aramayi yakala"},
    {"asama": "BOF Donusum", "kanallar": "Marka Search + WhatsApp", "ay2_try": 7500, "pct": "25%", "amac": "rezervasyonu kapat"},
    {"asama": "Retention/Geri kazanim", "kanallar": "Meta + Google remarketing", "ay2_try": 3000, "pct": "10%", "amac": "terk edeni geri getir"},
]

BUDGET_REALLOCATION_RULES = [
    {"tetik": "Kanal ROAS > hedef (2 hafta)", "esik": ">3x blended", "aksiyon": "+%20 butce (test/zayiftan al)", "kaynak": "OPT_RULES + rules.py"},
    {"tetik": "Kanal CPA > hedef (2 hafta)", "esik": ">1.5x hedef CPA", "aksiyon": "-%30 veya duraklat", "kaynak": "rules.py"},
    {"tetik": "Retargeting listesi dolu", "esik": "min boyut + ay2", "aksiyon": "retargeting'e %10 ayir", "kaynak": "campaigns/remarketing"},
    {"tetik": "Yuksek sezon (Haz-Eyl)", "esik": "doluluk yuksek", "aksiyon": "marka koru; indirimi kis; deneyim one", "kaynak": "SEASON_DETAIL"},
    {"tetik": "Dusuk sezon (Kas-Mar)", "esik": "talep dusuk", "aksiyon": "WhatsApp + retargeting + icerik/SEO'ya kaydir", "kaynak": "SEASON_DETAIL"},
    {"tetik": "Gunluk tavan", "esik": "Google 493 / Meta 500 TL/gun", "aksiyon": "asma (guardrail)", "kaynak": "scripts/guardrails.py"},
]

# =============================================================================
# 7) SEZON STRATEJI DETAYI — SEASONS'i derinlestirir (butce kaydirma + mix + aci)
# =============================================================================
SEASON_DETAIL = [
    {"sezon": "Yuksek (Haz-Eyl)", "aylar": "Haziran-Eylul", "butce_vurgu": "tam; marka koru, indirimi kis",
     "kanal_mix": "Marka Search + Meta prospecting + retargeting", "kreatif_aci": "manzara/kahvalti/aile, deneyim one",
     "kelime_vurgu": "foca otel, foca konaklama, butik otel", "teklif": "min indirim; 2 gece deneyim", "kpi": "doluluk + blended ROAS",
     "b2b": "dusuk (sanayi yazin yavas); etkinlik/dugun pik"},
    {"sezon": "Dusuk (Kas-Mar)", "aylar": "Kasim-Mart", "butce_vurgu": "kis; WhatsApp + retargeting + icerik agirlik",
     "kanal_mix": "dar non-brand + WhatsApp + retargeting + SEO/AEO", "kreatif_aci": "hafta ici sakin kacis, somine, huzur",
     "kelime_vurgu": "hafta sonu kacamagi, sakin tatil, romantik", "teklif": "hafta ici / erken rezervasyon avantaji", "kpi": "lead + direkt rezervasyon",
     "b2b": "YUKSEK: bakim-durus + yuklenici barinma + toplanti (Aliaga yogun)"},
    {"sezon": "Gecis (Nis-May, Eki)", "aylar": "Nisan-Mayis, Ekim", "butce_vurgu": "orta; prospecting + icerik + email",
     "kanal_mix": "Meta prospecting + Demand Gen + email + SEO", "kreatif_aci": "balayi/cift, evcil, koy kahvaltisi",
     "kelime_vurgu": "balayi oteli, evcil dostu otel, koy kahvaltisi", "teklif": "2 gece + kahvalti paketi", "kpi": "yeni kitle + CVR",
     "b2b": "orta: yil sonu gala/iftar planlama (Ekim-Kasim teklif zamani)"},
]
