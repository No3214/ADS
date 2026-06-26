# 08 — Yerel SEO + Google İşletme Profili ("kozbeyli" aramasında öne çık)

## Dürüst çerçeve (önce bunu oku)
- **"Kozbeyli Konağı" (markalı) aramada #1 olmak çok ulaşılabilir** — kendi markandır;
  doğru kurulumla organikte üst sıra + Maps + paid savunma ile SERP'i kaplarsın.
- **Jenerik organik #1'i hiç kimse GARANTİ edemez** (Google'a aykırı, sıralama
  algoritması + rekabet + niyet belirler). "İlk sırada çıkarırız" diyen bir araç/ajans
  gerçeği eğip büküyordur. Bizim yaptığımız: **şansı maksimize eden eksiksiz sistem**.
- **Bare "kozbeyli"** köy adıdır; o sorguda bilgi niyeti baskın (Vikipedi/gezi siteleri).
  Orada hedef: GBP + Haritalar + marka içeriğiyle **yan yana ve görünür** olmak, ve
  "kozbeyli **konağı/otel/konaklama**" sorgularını tam sahiplenmek.

Bu üç katman birlikte "kozbeyli" yazınca seni görünür kılar:
1. **Organik SEO** (site) · 2. **Google İşletme Profili + Haritalar** · 3. **Paid marka savunması** (Marka Search kampanyası — `campaigns/google-editor`).

## A. Google İşletme Profili (GBP) — yerel sinyalin kalbi
Tam liste: `campaigns/seo/gbp-kontrol-listesi.csv` (veya `kads seo gbp`). Kritik olanlar:
- **Sahiplik doğrulama** (kart/telefon/video). Doğrulanmamış profil zayıftır.
- **İsim:** tam olarak "Kozbeyli Konağı". Anahtar kelime doldurma (örn. "Kozbeyli Konağı
  Foça En İyi Otel") yasak ve askıya alma riski.
- **Birincil kategori: Otel.** Ek: Restoran, Düğün/etkinlik mekânı, Kahvaltı yeri.
- **NAP tutarlılığı:** Ad-Adres-Telefon site ve TÜM dizinlerde **birebir aynı**
  (No:188, 35680 Foça/İzmir · +90 532 234 2686).
- **Pin doğruluğu:** harita iğnesi gerçek konuma otursun (`kads seo schema` koordinatları
  38.7145, 26.8942 — GBP'deki gerçek pinle DOĞRULA).
- **Fotoğraf:** min 25 (cephe, odalar, kahvaltı, teras, restoran, logo, kapak) + kısa video.
- **Açıklama:** ~750 karakter, USP + Foça/Kozbeyli + doğal anahtar kelime.
- **Rezervasyon linki:** doğrudan `hmshotel.net` (UTM ile izlenebilir).
- **Google Posts:** haftalık (teklif/etkinlik/sezon).
- **Soru-Cevap:** sık sorulanları kendin sor + yanıtla (evcil, otopark, kahvaltı, ulaşım).
- **Yorumlar:** her misafirden iste; **TÜMÜNE 48 saat içinde yanıt ver.** Yorum
  hacmi + tazeliği + yanıt oranı yerel sıralamanın en güçlü kaldıraçlarındandır.
  (TripAdvisor "Dünyanın En İyi 10 Aile Oteli" tanınırlığını profil + sitede vurgula.)

## B. Site SEO (organik)
- **Ana sayfa `<title>`:** `Kozbeyli Konağı | Foça Butik Taş Otel & Restoran`.
  **H1:** "Kozbeyli Konağı". Marka terimini net sahiplen.
- **Sayfa mimarisi:** /odalar, /restoran, /galeri, /rezervasyon, /iletisim, /etkinlik,
  /hikayemiz (her biri tek niyet + iç link).
- **Şema (JSON-LD):** `campaigns/seo/schema-lodgingbusiness.jsonld` dosyasını sitenin
  `<head>`'ine `<script type="application/ld+json">…</script>` olarak göm. Geçerli
  schema.org `Hotel` tipidir (sahte puan İÇERMEZ; gerçek yorum verisi GBP'den gelir).
  Doğrula: Google Rich Results Test.
- **Teknik:** hız (Core Web Vitals), mobil, HTTPS, XML sitemap, robots.txt, kırık link yok.
  Site Next.js (istemci render) — etiket/şema render sonrası enjekte oluyorsa SSR/SSG ile
  ham HTML'de görünür olduğundan emin ol (docs/02 ile aynı sebep).
- **Çapraz alan:** rezervasyon `hmshotel.net`'te; ölçüm için cross-domain (docs/01).
- **İçerik/otorite:** "Kozbeyli köyü rehberi", "Foça'da ne yapılır", "köy kahvaltısı"
  blog yazıları — uzun kuyruk + marka otoritesi (jenerik "kozbeyli" görünürlüğüne yardım).

## C. Haritalar / yerel paket
- GBP eksiksizliği + yorum + foto + doğru pin = Maps sıralaması.
- **Yerel atıflar (NAP):** `campaigns/seo/nap-atif-listesi.csv` — Google, Apple Maps,
  Yandex Haritalar (TR'de önemli), Bing Places, Foursquare, TripAdvisor, trivago, Facebook,
  Instagram. Hepsinde NAP birebir aynı.
- **Maps temizliği:** yinelenen/sahte listeleme veya yanlış pin varsa kaldırt.

## D. Paid marka savunması (anında üst sıra)
- "Kozbeyli Konağı", "Kozbeyli otel", "Kozbeyli konaklama" sorgularında **Marka Search
  kampanyası** (zaten hazır: `kads build google`) paid'de en üstte gösterir ve OTA'ların
  marka terimine girmesine karşı savunur. Düşük CPC, yüksek CVR.
- Bu, organik #1 olsan bile değerlidir (SERP'te organik + GBP + paid = alanı kaplama).

## E. 30 günlük yerel SEO sırası
1. GBP sahiplik + doğrulama + NAP + kategori + pin (Hafta 1).
2. Fotoğraf yükleme + açıklama + rezervasyon linki + öznitelikler (Hafta 1).
3. Site `<title>`/H1 + JSON-LD şema gömme + Rich Results testi (Hafta 1-2).
4. NAP atıfları (Apple/Yandex/Bing/Foursquare/TripAdvisor) (Hafta 2).
5. Yorum toplama akışı (check-out sonrası kibar istek) + tüm yorumlara yanıt (Sürekli).
6. Haftalık Google Posts + Soru-Cevap besleme (Sürekli).
7. Marka Search kampanyasını yayına al (ölçüm doğrulandıktan sonra) (Hafta 3+).

> Komutlar: `kads seo` (özet) · `kads seo gbp` · `kads seo schema` · `kads seo local`
> · `kads seo brand` · `kads build seo` (dosyaları üret).
