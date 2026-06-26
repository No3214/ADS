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
