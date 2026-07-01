---
name: ads-delivery
description: >-
  Kozbeyli Konağı reklam teslim paketini (#2-#10) referans alarak kampanya
  kurulumu, kreatif üretimi, keyword/negatif seçimi, tracking QA, WhatsApp satış
  akışı ve haftalık optimizasyon rehberliği yapar. Kullan: "reklam kur", "kampanya
  aç", "teslim durumu", "kreatif üret", "keyword ekle", "optimizasyon", "WhatsApp
  şablonu", "bütçe dağıt", "30 gün planı" veya Kozbeyli reklam/Google Ads/Meta Ads
  işleri geçtiğinde. Kaynak: docs/REKLAM-TESLIM-PAKETI.md · CLI: kads deliver.
---

# Kozbeyli Konağı — Reklam Teslim Paketi Rehberi

Bu skill, `docs/REKLAM-TESLIM-PAKETI.md` teslim paketini (#2–#10) uygulamaya çevirir.
Durum özeti için önce **`kads deliver`** çalıştır, ölçüm için **`kads tracking`**.

## 0) ÖNCE OKU — değişmez sabitler
- GA4 `G-V3R66C3MEF` · Google Ads `AW-800024713` · Meta Pixel `1781546559309505` · GTM `GTM-KCG6B4MJ`
- Rezervasyon: HMS Otel · Kanal/parite: HoterRunner · Site: `www.kozbeylikonagi.com` (**`.com.tr` KULLANMA**)
- Bütçe: 30.000 TL/ay (Meta 15.000 · Google 15.000)
- Marka renkleri: Zeytin `#505D4B` · Altın `#C4A265` · Fildişi `#F8F5F0`
- Konum dili: **"Yeni Foça'ya yakın"** — sabit/yanlış km ("13 km" vb.) YAZMA (doğrulanmadı).

## 1) ALTIN KURAL — ölçüm kapısı
**Ölçüm canlı değilse (GTM içi GA4/Ads etiketi yoksa) HİÇBİR kampanyayı ölçekleme.**
Sıra: GTM'e GA4 Config + Ads Conversion Linker/Conversion → Publish → **test rezervasyonuyla doğrula** →
`kads tracking` skoru 80+ → ancak o zaman ölçekle. Bu yapılmadan sadece küçük bütçeyle marka + prospecting aç.
Düşük bütçede Meta öğrenme fazı için **WhatsAppClick / Lead** optimize et (Purchase değil).

## 2) Strateji rolleri (#2)
Meta = talep yaratma · Google = talep yakalama · FBL/PMax = direkt rezervasyon · WhatsApp = satış kapatma · Site = güven.
- **Google 15k:** Marka %25 · NonBrand %25 · FBL+PMax %30 · Remarketing %10 · Test %10 → `kads allocate`
- **Meta 15k:** Prospecting %55 · Kahvaltı/Restoran %20 · Retargeting %15 · Düğün %10
- Google kur-sırası: GBP → FBL → Marka Search → NonBrand → PMax → Remarketing → (allowlist) Hotel Ads.

## 3) Kreatif üretimi (#3)
12 konsept: Romantik (R1–R3), Kahvaltı (K1–K3), Taş konak (T1–T2), Canlı müzik (M1–M2), Düğün (D1–D2).
Her kreatif için üret: **hook (0–2sn) · reels senaryosu · feed metni · story · CTA · retargeting mesajı · landing eşlemesi**.
Tam hook/senaryo metinleri paketin #3 bölümünde. Renk paletine ve sakin/mirasa-saygılı tona sadık kal.
30 günlük içerik/test takvimini uygula (Hafta 1 açılış → Hafta 4 kazananı ölçekle).

## 4) Keyword + negatif (#4)
- Marka: `[tam]` + `"öbek"` · NonBrand: `"öbek"` · Broad YALNIZCA smart bidding + veri sonrası.
- Kaynak: `campaigns/google-editor/03_keywords.csv` · `kads keywords`. Negatif listesi paket #4'te (iş/emlak/OTA/coğrafi).
- NonBrand 3 grubu ayrı RSA alır (Butik / Genel / Niche) — birini diğerine kopyalama.

## 5) Tracking QA (#5) — 18 madde, kapı 80+
`kads tracking` ile kontrol et. EKSİK olanlar (GA4 Config, Ads Conversion, Purchase, Advanced Matching, CAPI) reklam öncesi şart.
`purchase.event_id = transactionId` dedup kod hazır (Pixel+CAPI+GA4 aynı id). UTM standardını her linke uygula:
`utm_source={google|meta}&utm_medium={cpc|paid_social}&utm_campaign={...}&utm_content={kreatif_id}`.

## 6) Landing QA (#6)
Reklam mesajı = sayfa başlığı. Eşleme matrisi paket #6'da (kahvaltı→/gastronomi, düğün→/organizasyonlar, oda→/odalar).
Sosyal kanıt: yıldız ortalaması (~4.2) yerine **taze olumlu yorum akışı** öne çıkar; yorum hızını artır (ücretsiz kaldıraç).

## 7) WhatsApp satış (#7)
Şablonlar paket #7'de (ilk yanıt → fiyat → 24s/72s/7g takip). Rezerve olanı `kads conversions` ile **offline conversion**
olarak Google/Meta'ya geri besle → algoritma gerçek satışı öğrenir. Haftalık kayıt tablosunu tut.

## 8) Haftalık optimizasyon (#8) — 8 karar kuralı
1. CTR düşük → hook değiştir · 2. Tıklama var mesaj yok → landing/teklif · 3. Mesaj var rezerve yok → WhatsApp takip ·
4. Frekans >3 → kreatif yenile · 5. Marka CVR yüksek + bütçe kısıtlı → önce markayı doyur · 6. Keyword CPA 3x → duraklat/negatif ·
7. Retargeting CPA en düşük → payı artır · 8. **Ölçüm skoru 80 altı → TÜM ölçeklemeyi durdur, önce ölç.**
Rutin: `kads monitor` + `kads rules`.

## 9) Risk (#9) & 30 gün (#10)
10 risk paketin #9'unda (en kritik: ölçüm canlı değil, yanlış event optimizasyonu, consent mode, OTA parite).
30 gün: Gün 1–3 ölçüm kapısı → 4–7 kreatif/açılış → 8–14 test → 15–21 temizlik → 22–30 ölçekleme.

## Güvenlik (bu repo kuralları)
- Reklam/finans hesapları **salt-okunur** referans: para taşıma / trade / canlı bütçe değişimini SEN yapma; kullanıcıya bırak.
- Token/secret'i sohbete/GitHub'a yazma; `.env` gitignore'lu. Yazma işlemleri guardrail'li ve varsayılan kapalı.
- Doğrulanmamış iddia (km, ödül, "en iyi") kullanma. `.com.tr` gündem yapma.

## Hızlı komutlar
`kads deliver` (durum) · `kads tracking` (ölçüm) · `kads keywords` · `kads allocate` (bütçe) · `kads monitor` · `kads rules` · `kads conversions` (offline).
Referanslar: `docs/REKLAM-TESLIM-PAKETI.md` · `golive/GTM-KURULUM.html` · `audit/MCKINSEY-EXECUTIVE-SUMMARY.html`.
