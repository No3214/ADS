# 06 — Türkiye Otel Reklam Benchmark'ları + Foça Rekabet Taraması

Tarih: Haziran 2026. Tüm rakamlar **piyasa referansıdır, garanti değildir**; gerçek
maliyet teklif, kalite, sezon, konum ve rekabete göre değişir. Anahtar Kelime
Planlayıcı ile kendi hesabının verisini doğrula.

## 1. Google Ads (Türkiye)
- **Ortalama CPC (genel, TR):** ~10,5 TL (2026). Otel/turizm rekabetçi bir dikeydir;
  marka terimleri çok daha ucuz, jenerik "foça otel" daha pahalıdır.
- **Bizim CPC limitimiz:** ~6 TL (marka çoğunlukla altında; non-brand'i dar tutarak
  kontrol ediyoruz). Kaynak: kampanya `Max CPC Bid Limit`.
- **Dönüşüm pik saatleri:** 08–11 ve 19–22. Bütçe darsa bu saatlere ağırlık ver
  (reklam takvimi).
- **Google Hotel Ads:** komisyon-hedefli teklif yeni kampanyalar için kaldırıldı;
  alternatifler (tROAS, Performance Max for travel) HMS'in canlı fiyat/müsaitlik
  feed'ini gerektirir → şimdilik Search'e odak (docs/03).

## 2. Meta (Instagram/Facebook, Türkiye)
- **Instagram CPC:** ~1,50–8,00 TL (≈ $0,25–2,50) aralığı; hedefleme ve kreatife bağlı.
- **Minimum anlamlı bütçe:** günlük tabanın (50 TL) çok üstünde; bizim ad set'ler
  100–350 TL/gün ile öğrenmeyi besler.
- **ROAS referansı:** e-ticaret için tipik hedef 3–5x. Otelde **blended** ROAS hedefi
  3x (90.000 TL izlenen gelir) – 4x (120.000 TL) — bkz. plan.
- Meta'nın rolü: görsel hikâye ile **talep yaratma** + retargeting + WhatsApp; doğrudan
  rezervasyon geliri OTA bağımlılığını azaltır.

## 3. Bizim otelin ekonomisi (web ile doğrulandı)
- **Ortalama gece:** ~1.900–2.000 TL. Çok geceli konaklamada ortalama rezervasyon
  geliri ~7.500–10.000 TL bandına oturur (planın varsayımı tutarlı).
- **16 oda** kısıtı: reklamın işi boş geceleri doldurmak; doluluk-duyarlı harcama şart
  (docs/05 §3).
- **Rezervasyon hedefi (30.000 TL medya):**
  | Hedef | Ort. rezervasyon 7.500 TL | Ort. 10.000 TL |
  |---|---:|---:|
  | 3x ROAS (90.000 TL) | 12 | 9 |
  | 4x ROAS (120.000 TL) | 16 | 12 |
  (`kads kpi` ile hesaplanır.)

## 4. Foça / Eski Foça rekabet taraması
- **Pazar dokusu:** Foça konaklaması büyük tatil köyleri değil, **küçük aile işletmesi
  butik oteller**; özellikle Eski Foça'da restore Rum evleri / taş konaklar yoğun.
  Konumlanma genelde liman/merkez yürüme mesafesi.
- **Bizim ayrışma:** Kozbeyli **köyü** (merkeze değil, 600 yıllık köye konumlu), taş konak
  mirası, organik köy kahvaltısı, çatı terası deniz manzarası, **evcil dostu (ücretsiz)**,
  TripAdvisor "Top 10 Aile Oteli" tanınırlığı, 200 kişilik etkinlik alanı.
- **Adı geçen rakip/komşu işletmeler (örnek):** Bülbül Yuvası Hotel, Huri Nuri Hotel,
  Foça Ensar Otel. (Konumlanma: merkez/liman; bizim hikâye: köy + miras + mutfak + evcil.)
- **OTA/aggregatörler (marka savunması gerekli):** trivago, Booking, Hotels.com,
  neredekal, obilet, etstur, tatilsepeti, Jolly. Bunlar marka terimine girer →
  Marka Search + GBP ile doğrudan rezervasyonu savun (komisyonsuz avantaj).

## 5. Sonuç (kampanyaya yansıması)
- Non-brand'i **dar + niyetli** tut (foça butik/taş ev/köy oteli), genel "foça otel"i
  yüksek CPC nedeniyle test bütçesinde dene.
- Negatif liste agresif (ucuz/kamp/emlak/iş + alakasız lokasyonlar) — küçük bütçede en
  büyük kaldıraç (`campaigns/google-editor/05_negative_keywords.csv`).
- Meta'da deneyim/hikâye kreatifleri (köy, manzara, kahvaltı, evcil) ayrışmayı taşır.
- Doluluk + sezon harcamayı yönlendirir (docs/05).

## Kaynaklar (Haziran 2026 web araması)
- TR Google Ads CPC ~10,5 TL: 212medya, Avangard Reklam (TR dijital istatistikleri 2026).
- Otel/turizm pik saat + öneriler: pazarlamaturkiye.com, kreativty.com, blimp.com.tr.
- Google Hotel Ads komisyon teklifi kaldırma: zenitdijital.com.
- Instagram CPC + ROAS: prismindmedia.com, onuroztr.com, zbtmedia.com; otel direkt
  rezervasyon: adroket.com.
- Otel verisi/fiyat/rakip: trivago, neredekal, kucukoteller.com.tr, enuygun, izgazete,
  Kozbeyli Konağı resmî site + Instagram.
> Not: Rakamlar referans amaçlıdır; hesabının gerçek verisiyle güncelle.
