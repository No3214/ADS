# 09 — Dijital Varlık & SEO Denetimi (kanıt temelli)

Tarih: 26 Haziran 2026. Yöntem: her iki resmi domain + EN sürümü + alt sayfalar
web_fetch ile çekildi; sosyal/OTA/Google taraması yapıldı. Erişilemeyen / client-render
olan yerler açıkça belirtilmiştir. Bu denetim `kads presence` ve kontrol-merkezi
panosunu besler.

## Özet (en kritik 5 bulgu)

1. **ÜÇ ayrı domain aynı markayı taşıyor — en büyük risk.** Bilinen iki domaine
   (`.com.tr` ve `.com`) ek olarak **üçüncü ve aktif** bir domain çıktı:
   **`kozbeylikonagiotel.com`** ("Rezervasyon 0 232 218 21 09" — farklı, sabit hatlı
   telefon). Üç domain + HMS booking subdomaini marka otoritesini böler, duplicate
   content / canonical karmaşası yaratır ve müşteriye **çelişkili telefon numarası**
   gösterir (cep `+90 532 234 2686` ↔ sabit `0232 218 2109`). Tek başına en acil konu.

2. **`.com.tr` ("resmi" sanılan domain) SEO açısından ölü bir kabuk.** Sayfa body'si
   **tek bir base64 gömülü PNG**; taranabilir metin yok. `/odalar`, `/iletisim` gibi
   alt yollar **ana sayfaya düşüyor** (gerçek route yok). Title/description iyi olsa da
   indekslenecek metin gövdesi olmadığı için kelime sıralaması üretemez.

3. **`.com` açık ara en güçlü ve gerçek site** (Next.js, server-render metin, TR+EN,
   zengin içerik, SSS, doğru NAP, WhatsApp CTA, HMS'e UTM'li temiz geçiş). Karar net:
   **`.com` ana/canonical domain olmalı; diğerleri 301 ile buraya yönlenmeli.**

4. **Marka araması OTA + eski/parazit listelerle dolu; otel kendi adına bile zayıf.**
   "Kozbeyli Konağı" aramasında trivago, obilet, Booking, Hotels.com, otelz, wheree,
   bookeder, kesfetsek ve **eski `kozbeylikonagiotel.com`** öne çıkıyor. Google Otel/Maps
   paneli mevcut ama resmi site bu rekabette öne çıkamıyor.

5. **İnceleme puanları tutarsız + NAP'ta köy/şehir karışıklığı.** Booking ~8.8,
   Otelpuan ~8.3 iyi; **TripAdvisor 3/5** marka algısını düşürüyor. Booking oteli
   **"Yenifoça"**, bazı kaynaklar "~50 km İzmir / 15 km Foça", site "Foça'ya ~13 km"
   diyor → şehir etiketi ve mesafe ifadeleri oturmamış.

## Mülk bazında denetim

### 1) www.kozbeylikonagi.com.tr — "resmi" domain (ama kabuk)
- **Durum:** HTTP 200, HTTPS, TR. Title/description çok iyi; OG var. Ama body'nin tamamı
  base64 gömülü görsel; H1/H2, metin, link yok. `/odalar`, `/iletisim` ana sayfaya düşüyor
  (canonical hep ana sayfa).
- **Hatalar/eksikler:** image-only metinsiz sayfa (indekslenemez); çoklu domain çakışması;
  schema yok; OG image bir logo; NAP gövdede taranamaz.
- **Düzeltme:** **Kritik** — `.com.tr` → `301` `.com`. Marka için domaini tut ama tek
  sayfalık kabuk olarak yayında bırakma. (Tutulacaksa: gerçek HTML metin + schema.)

### 2) www.kozbeylikonagi.com — gerçek ana site (en güçlü varlık)
- **Durum:** Next.js, server-render gerçek metin. Tam mimari: ana sayfa, `/odalar`
  (+ oda detay URL'leri), `/hikayemiz`, `/gastronomi`, `/organizasyonlar`, `/deneyimler`
  (Kozbeyli/Foça rehberleri = gerçek SEO içeriği), `/iletisim` (form + harita + WhatsApp),
  `/galeri`, `/sss`, hukuki sayfalar. TR+EN. Güçlü meta (title/description, OG, Twitter,
  robots index/follow, self-canonical). NAP doğru: No:188, Foça/İzmir, +90 532 234 26 86,
  info@kozbeylikonagi.com, harita 38.713943,26.896018. Rezervasyon HMS'e UTM'li geçiş.
- **Hatalar/eksikler:** görünür schema/JSON-LD yok; hreflang doğrulanamadı; EN'de
  placeholder ("yorumlar yakında", "experience cue"); HMS cross-domain ölçüm kanıtlanamadı;
  çalışma saati/geç giriş ifade çelişkisi; bazı footer sayfaları (menü/teklifler) derinliği
  belirsiz; Booking/TripAdvisor rozetleri siteye yansımamış.
- **Düzeltme:** **Kritik** — tek resmi/canonical domain ilan et. **Yüksek** — JSON-LD
  şema (`campaigns/seo/schema-lodgingbusiness.jsonld`, url'i `.com`'a göre güncelle) +
  gerçek yorum + cross-domain GA4. **Orta** — hreflang; EN placeholder'ları değiştir.

### 3) kozbeylikonagiotel.com — ESKİ/PARAZİT üçüncü domain
- **Durum:** Aktif, indeksli: "…Rezervasyon **0 232 218 21 09**", `http://`.
- **Hatalar/eksikler:** marka kanibalizasyonu; **çelişkili NAP / yanlış telefon**;
  HTTPS yok; sahiplik belirsiz (otel mi, eski ajans/aracı mı?).
- **Düzeltme:** **Kritik** — sahipliği teyit et. Otele aitse içeriği kaldır + 301 `.com`.
  Değilse kaldırılması için iletişime geç; Google'da yanlış numara için düzeltme talep et.

### 4) HMS rezervasyon motoru (kozbeyli-konagi.hmshotel.net)
- **Durum:** `.com`'dan UTM'li, "yeni sekme + kart bilgisi burada saklanmaz" notuyla doğru
  çağrılıyor. Oda tipleri site ile uyumlu.
- **Hatalar/eksikler:** ayrı domain → cross-domain tracking zorunlu; GA4 linker/referral
  exclusion kanıtlanamadı → dönüşüm yanlış atfediliyor olabilir.
- **Düzeltme:** **Yüksek** — GA4/GTM allowLinker + referral exclusion `hmshotel.net` +
  begin_checkout event (docs/01).

### 5) Instagram — @kozbeylikonagi
- **Durum:** Aktif, ~11K takipçi, bio "Aile İşletmesi Taş Otel & Restoran", düzenli paylaşım.
- **Hatalar/eksikler:** bio link hedefi doğrulanamadı (login duvarı) — eski domaine
  gidiyorsa trafik yanlış siteye akar; marka adı varyasyonu ("Konağı" vs "Konağı Otel").
- **Düzeltme:** **Yüksek** — bio link = `.com`/WhatsApp. **Orta** — marka adını sabitle;
  öne çıkan hikâyeler (Odalar/Menü/Rezervasyon).

### 6) Facebook — /kozbeylikonagi
- **Durum:** Sayfa var, konum "Kozbeyli, İzmir", foto/video/gönderi geçmişi var.
- **Hatalar/eksikler:** güncellik IG'den düşük görünüyor; "About" NAP'ı tek resmi domaine
  işaret ediyor mu doğrulanamadı.
- **Düzeltme:** **Orta** — About'ta website=`.com`, telefon=+90 532 234 2686, standart adres.

### 7) OTA & inceleme listeleri
- **Durum:** trivago, Booking, Hotels.com, obilet, etstur, Agoda, otelz, Otelpuan, trip.com,
  easemytrip, wheree, bookeder, kesfetsek, TripAdvisor'da listeli. Booking ~8.8, Otelpuan
  ~8.3, TripAdvisor 3/5. Google Otel/Maps paneli mevcut.
- **Hatalar/eksikler:** marka SERP'i OTA-dominant; NAP/şehir tutarsızlığı (Yenifoça vs Foça);
  TripAdvisor düşük puan + düşük hacim; listeler arası ad/koordinat farkları.
- **Düzeltme:** **Kritik** — Google Business Profile sahiplen + NAP'ı tek standarda çek.
  **Yüksek** — marka kelimesinde organik/ücretli savunma; OTA profillerini `.com`+NAP ile
  eşitle; TripAdvisor yorum kampanyası. **Orta** — mesafe/konum metnini tutarlı hale getir.

## İki (üç) domain kararı — net öneri

| Domain | Render | İçerik | Telefon | Karar |
|---|---|---|---|---|
| **kozbeylikonagi.com** | Server-render, gerçek metin | Tam (TR+EN) | +90 532 234 2686 | **ANA / CANONICAL** |
| **kozbeylikonagi.com.tr** | Image-only kabuk | Yok | görselde | **301 → .com** (marka için tut) |
| **kozbeylikonagiotel.com** | Eski/parazit, http:// | Belirsiz | **0232 218 2109 (yanlış)** | **Kaldır/301; sahiplik teyidi** |
| kozbeyli-konagi.hmshotel.net | Booking motoru | Booking | 905322342686 | Koru; GA4 linker |

> **Tek cümle öneri:** `kozbeylikonagi.com` tek resmi domain ilan edilmeli; `.com.tr` ve
> `kozbeylikonagiotel.com` 301 ile buraya yönlenmeli (`.com.tr` marka koruması için tutulur),
> tüm sosyal/OTA/Google profilleri yalnızca `.com`'a ve tek numaraya (+90 532 234 2686)
> işaret etmeli. Denetimdeki en yüksek getirili tek hamle budur.
>
> NOT: Başlangıç paketi config'i (`config/ads-assets.yaml`, `kads/seo.py`) şu an site
> domaini olarak `.com.tr` kullanıyor. Canonical kararını verince schema `url`'i + Ads
> final URL'leri seçilen domaine göre güncellenmeli.

## Önceliklendirilmiş düzeltme listesi

| # | Bulgu | Mülk | Öncelik | Aksiyon |
|---|---|---|---|---|
| 1 | Üç marka domaini + çelişkili telefon | Tüm domainler | Kritik | `.com` canonical; diğerleri 301; tek numara |
| 2 | `kozbeylikonagiotel.com` yanlış numara yayında | otel.com | Kritik | Sahiplik teyit; kaldır/301; Google'da numara düzelt |
| 3 | `.com.tr` image-only kabuk | .com.tr | Kritik | 301 ile çöz; tutulacaksa metin + schema |
| 4 | Google Business Profile sahiplik + NAP standardı | Google/OTA | Kritik | GBP sahiplen; NAP tek standart (Foça vs Yenifoça) |
| 5 | schema.org JSON-LD yok | .com | Yüksek | Hotel + Restaurant + FAQPage JSON-LD ekle |
| 6 | HMS cross-domain ölçüm yok | .com + hms | Yüksek | GA4 allowLinker + referral exclusion + begin_checkout |
| 7 | Marka SERP OTA-dominant | OTA + .com | Yüksek | Marka organik/ücretli savunma; OTA profil eşitle |
| 8 | TripAdvisor 3/5 + düşük hacim | TripAdvisor | Yüksek | Yorum toplama kampanyası; profil güncelle |
| 9 | IG/FB bio link + NAP doğrulanamadı | IG + FB | Yüksek | Bio link=.com/WhatsApp; FB About NAP |
| 10 | EN placeholder metinler | .com/en | Orta | Gerçek yorum/içerik |
| 11 | hreflang TR↔EN doğrulanamadı | .com | Orta | rel=alternate hreflang çiftleri |
| 12 | Mesafe/şehir tutarsız | Site + OTA | Orta | Tek metin: "Foça merkeze ~13 km" |
| 13 | Çalışma saati çelişkisi; boş sayfalar | .com | Düşük | SSS ile hizala; menü/teklifler doldur |
| 14 | Marka adı varyasyonu | Tüm kanallar | Düşük | "Kozbeyli Konağı" sabit |

## Kaynaklar
web_fetch: kozbeylikonagi.com.tr (+ /odalar, /iletisim), kozbeylikonagi.com (+ /odalar,
/iletisim, /hikayemiz, /en). WebSearch/görülen: kozbeylikonagiotel.com, TripAdvisor,
trivago, Booking (Yenifoça), obilet, Hotels.com, Agoda, otelz, Otelpuan, kesfetsek, wheree,
trip.com, easemytrip, instagram.com/kozbeylikonagi, facebook.com/kozbeylikonagi, Google
Otel/Maps paneli, kozbeyli-konagi.hmshotel.net.
Erişilemeyen: IG/FB iç sayfalar (login); .com JSON-LD/hreflang (fetch'te görünmedi —
tarayıcı denetimiyle teyit); .com.tr body (base64 görsel).

---

## Güncel web-reach doğrulaması (27 Haz 2026)

Denetim bulguları canlı çekimle (web-reach `fetch.py`) tazelendi. **Sinyaller** — kesinleştirmek
için Google Rich Results Test + GBP + tarayıcıyla teyit edilmeli:

- **`kozbeylikonagi.com` (gerçek site):** HTTP 200. **JSON-LD VAR** — `@type`: PostalAddress,
  GeoCoordinates, LocationFeatureSpecification (amenity). Yani "schema yok" bulgusu **artık
  geçerli değil**; aksiyon "ekle"den **"denetle/tamamla"ya** döndü (Hotel/Restaurant/FAQPage/
  HotelRoom tam mı?). Telefon **+90 532 234 2686 (doğru)**.
- **`kozbeylikonagiotel.com` (parazit):** Jina reader "Domain could not be resolved" (DNS) →
  **muhtemelen ölü/kaldırılmış.** Yanlış telefon (0232 218 2109) sayfadan gelmedi. Risk Kritik'ten
  Orta'ya düştü; iş artık **Google'da kalan listing + GBP'deki yanlış numarayı** temizlemek.
- **`kozbeylikonagi.com.tr` (kabuk):** HTTP 200, ~7.3K metin + 11 "kozbeyli" geçişi → eskisi gibi
  tamamen image-only olmayabilir; yine de canonical `.com`, diğerleri 301 önerisi geçerli.

Kaynak: web-reach fetch.py (jina_reader/direct), 27 Haz 2026. Her sezon yeniden doğrula.
