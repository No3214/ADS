# 30.000 TL/Ay Google + Meta Direkt Rezervasyon Planı

## Kanal rolleri

- **Google Search:** Var olan yüksek niyetli rezervasyon talebini yakalar.
- **Meta/Instagram:** Talep yaratır, hikâyeyi görselleştirir, yeniden pazarlama ve WhatsApp rezervasyonlarını taşır.
- Başarı, yalnız platform raporlarıyla değil toplam direkt rezervasyon geliri, blended CPA ve blended ROAS ile değerlendirilir.

## Google Ads — 15.000 TL/ay

Google ortalama günlük bütçeleri 30,4 gün üzerinden hesaplanmıştır.

| Kampanya | Aylık | Ortalama günlük | İşlev |
|---|---:|---:|---|
| Marka Search | 4.500 TL | 148 TL | Marka/OTA savunması |
| Dar non-brand Search | 9.000 TL | 296 TL | Yüksek niyetli yeni talep |
| Kontrollü test rezervi | 1.500 TL | 49 TL | Arama terimi ve sezon testi |

İlk 30–45 gün Google Display remarketing açılmaz. Yeniden pazarlama Meta tarafından karşılanır; Google bütçesi Search'te tutulur.

### Teklif stratejisi

- Ölçüm doğru ancak hesap yeni ise: Maximize Clicks + CPC üst sınırı.
- Maximize Conversions için 15 dönüşüm/30 gün zorunluluk değil, güçlü tavsiyedir.
- Target CPA geçmiş olmadan teknik olarak kullanılabilir; fakat ekonomik hedef bilinmeden keyfi tCPA girilmez.
- Tüm yeni kampanyalar `PAUSED` oluşturulur.

## Meta/Instagram — 15.000 TL/ay

### İlk 30 gün

| Kampanya | Aylık | Günlük | İşlev |
|---|---:|---:|---|
| Website Sales Prospecting | 10.500 TL | 350 TL | Yeni kitle ve direkt rezervasyon |
| WhatsApp/Mesaj | 4.500 TL | 150 TL | Nitelikli rezervasyon talebi |

Ayrı retargeting, site ve Instagram kitlesi oluşmadan açılmaz.

### 2. aydan sonra

| Kampanya | Aylık | Günlük | İşlev |
|---|---:|---:|---|
| Prospecting | 9.000 TL | 300 TL | Yeni talep |
| Retargeting | 3.000 TL | 100 TL | Site/IG/checkout terk |
| WhatsApp/Mesaj | 3.000 TL | 100 TL | Rezervasyon görüşmesi |

### Meta yapı kuralları

- İlk ay en fazla 2 kampanya; ikinci ay en fazla 3 kampanya.
- Bütçeyi çok sayıda küçük ad sete bölme.
- Reels/Stories için 9:16, Feed için 4:5 kreatif üret.
- Purchase güvenilir değilse Website Sales'i açma; önce tracking ve WhatsApp akışını çalıştır.
- En derin güvenilir olaya optimize et: `purchase`; geçici alternatif `begin_checkout`.

## Kreatif konseptleri

1. 600 yıllık Kozbeyli köyü ve taş konak
2. Oda, çatı terası ve Ege manzarası
3. Organik köy kahvaltısı ve Antakya–Ege mutfağı
4. Evcil hayvan dostu konaklama
5. Hafta içi sakin kaçış ve müsaitlik

## Ölçüm ön koşulları

1. Doğru GTM container seçilir.
2. Rezervasyon motorunun gerçek domaini ve iframe/yönlendirme yapısı doğrulanır.
3. Google purchase: `transaction_id`, `value`, `currency=TRY`.
4. Meta Pixel + CAPI: aynı `event_id` ile tekilleştirme.
5. Meta `Purchase`, `InitiateCheckout`, `Lead` olayları Test Events'te doğrulanır.
6. Google Ads purchase dönüşümü test rezervasyonunda doğrulanır.
7. UTM standardı uygulanır.

## Ticari hedef

| Hedef | Gerekli izlenen rezervasyon geliri |
|---|---:|
| 3x medya ROAS | 90.000 TL |
| 4x medya ROAS | 120.000 TL |

| Ortalama rezervasyon geliri | 3x için rezervasyon | 4x için rezervasyon |
|---:|---:|---:|
| 7.500 TL | 12 | 16 |
| 10.000 TL | 9 | 12 |

WhatsApp için:

`Maksimum CPL = kabul edilen rezervasyon CPA × lead→rezervasyon oranı`

Örnek: rezervasyon CPA sınırı 2.000 TL, kapanış oranı %15 ise maksimum nitelikli WhatsApp lead maliyeti 300 TL.
