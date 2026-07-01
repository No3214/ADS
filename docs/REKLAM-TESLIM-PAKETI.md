# KOZBEYLİ KONAĞI — REKLAM TESLİM PAKETİ (#2 → #10)

> Master promptun 20. bölümündeki teslim listesinin **#2–#10** arasını uygulanabilir tek parça olarak içerir.
> CLI özeti: `kads deliver` · Skill: `skills/ads-delivery/SKILL.md`

## Sabitler
| Alan | Değer |
|---|---|
| GA4 | `G-V3R66C3MEF` |
| Google Ads | `AW-800024713` (Customer 648-937-2864) |
| Meta Pixel | `1781546559309505` (Ad Account `act_2115950531494`) |
| GTM | `GTM-KCG6B4MJ` |
| Rezervasyon motoru | HMS Otel (`kozbeyli-konagi.hmshotel.net`) |
| Kanal yönetimi | HotelRunner (OTA parite) |
| Site | `www.kozbeylikonagi.com` (Vercel) — **`.com.tr` KAPSAM DIŞI** |
| Marka renkleri | Zeytin Yeşili `#505D4B` · Antik Altın `#C4A265` · Fildişi `#F8F5F0` |
| Bütçe | **30.000 TL/ay** — Meta 15.000 · Google 15.000 |
| Telefon/WhatsApp | +90 532 234 2686 |
| Konum | Kozbeyli Köyü No:188, Foça/İzmir — **Yeni Foça'ya yakın** (kesin km doğrulanmadı) |

> **⚠️ ÖN KOŞUL — ÖLÇÜM CANLI DEĞİL:** GTM içinde GA4/Ads dönüşüm etiketi yok → Google Ads 0 dönüşüm gösteriyor.
> **Bu paketteki her ölçekleme adımı, ölçüm doğrulanana kadar bekler.** Bkz. `golive/GTM-KURULUM.html`, `kads tracking`.

---

## DOĞRULAMA ÖZETİ — 6 düzeltme
1. **Free Booking Links (FBL)** feed'siz kurulabiliyor — GBP üzerinden (Hotel Center şart değil).
2. **PMax for Travel Goals**, Hotel Center hesabı gerektirmiyor.
3. **Klasik Hotel Ads** allowlist'e bağlı (davetle açılır).
4. **Enhanced Conversions** web + leads tek ayar (Nisan 2026 birleşti).
5. **Consent Mode v2 + sertifikalı CMP** zorunlu (AEA/AB trafiği).
6. **Meta öğrenme fazı** ~50 dönüşüm/ad set → düşük bütçede ucuz event optimize et: **WhatsAppClick / Lead** (Purchase değil).

---

## TESLİM #2 — STRATEJİ

**Formül:** Meta = talep yaratma · Google = talep yakalama · FBL/PMax = direkt rezervasyon · WhatsApp = satış kapatma · Site = güven · Tracking = bütçe koruma.

### Google öncelik sırası (kur-ve-aç)
GBP optimizasyonu → **FBL** → **Marka Search** → **NonBrand Search** → **PMax (Travel Goals)** → **Remarketing/RLSA** → (allowlist gelirse) Hotel Ads.

### Google bütçe dağılımı (15.000 TL/ay)
| Blok | Pay | TL/ay | Not |
|---|---|---|---|
| Marka Search | %25 | 3.750 | En düşük CPC, en yüksek CVR, OTA savunması (marka adı poz-1 pin) |
| NonBrand Search | %25 | 3.750 | 3 grup: Butik / Genel / Niche (farklı RSA) |
| FBL + PMax | %30 | 4.500 | Direkt rezervasyon, komisyonsuz |
| Remarketing/RLSA | %10 | 1.500 | Site + `begin_checkout` terk havuzu |
| Test | %10 | 1.500 | Yeni kelime/kreatif denemesi |

### Meta bütçe dağılımı (15.000 TL/ay)
| Kampanya | Pay | TL/ay | Optimizasyon |
|---|---|---|---|
| Prospecting (talep yaratma) | %55 | 8.250 | WhatsAppClick / Lead (öğrenme fazı için ucuz event) |
| Kahvaltı/Restoran | %20 | 3.000 | Yerel + ilgi hedefleme |
| Retargeting | %15 | 2.250 | Site + IG/FB etkileşim + video izleyen |
| Düğün/Organizasyon | %10 | 1.500 | Lead form / WhatsApp |

> **Not (tutarlılık):** Bu dağılım #2 teslim **rafinasyonudur** (FBL/PMax + Remarketing + Düğün ayrı satır). `kads plan`
> (data.PLAN) ise ilk **fazlı taban** plandır (Marka 4500 · NonBrand 9000 · Test 1500 / Meta Prospecting 10500 · WhatsApp
> 4500 · Retargeting 3000). İkisi de 15k+15k'ye toplanır; küçük satır farkları normaldir. Canlı veri gelince tek doğru
> kaynak **`kads allocate`** ile güncellenir — iki tabloyu elle senkron tutmayın.

### Düşük bütçe kuralı
Az ad set (havuzu bölme) · ucuz event optimizasyonu (WhatsApp/Lead) · **marka search önce** (garanti dönüşüm) · geniş eşleme YALNIZCA smart bidding + veri sonrası.

---

## TESLİM #3 — 12 KREATİF

Her kreatif: **hook · reels senaryosu · feed metni · story · CTA · retargeting mesajı · landing page**.
Renk paleti: Zeytin `#505D4B` / Altın `#C4A265` / Fildişi `#F8F5F0`. Ton: sakin, mirasa saygılı, abartısız.

### Romantik (R1–R3)
- **R1 — "Çatı terasında gün batımı"**
  - Hook (0–2sn): "Ege'nin en sessiz gün batımı burada." · Reels: teras → şarap → manzara pan, trend akustik ses.
  - Feed: "600 yıllık taş konakta iki kişilik kaçış. Çatı terasında Ege manzarası, mum ışığı, sessizlik." · Story: "Kaçışını ayır →" swipe.
  - CTA: WhatsApp'tan tarih sor. · Retargeting: "Baktığın oda hâlâ müsait — bu hafta sonu?" · Landing: `/odalar`
- **R2 — "İki kişilik köy sabahı"**
  - Hook: "Telefonsuz bir sabah nasıl olurdu?" · Reels: taş avlu, kuş sesi, kahvaltı serpme.
  - Feed: "Yeni Foça'ya yakın, kalabalıktan uzak. Sadece siz, taş duvarlar ve organik kahvaltı." · CTA: Rezerve et. · Landing: `/rezervasyon`
- **R3 — "Balayı / yıldönümü"**
  - Hook: "Yıldönümünüzü hatırlanacak bir yere taşıyın." · Retargeting: "Özel gününüz için oda + sürpriz kurulum." · Landing: `/odalar`

### Kahvaltı (K1–K3)
- **K1 — "Organik köy kahvaltısı"** · Hook: "Bu sofra 40 çeşit." · Reels: serpme kahvaltı üstten çekim, dibek kahvesi. · Feed: "Köyün organik kahvaltısı — reçeller, peynirler, sıcak pişi." · CTA: Masa ayırt (WhatsApp). · Landing: `/gastronomi`
- **K2 — "Pişi + dibek kahvesi"** · Hook: "Dibekte dövülmüş kahve kokusu." · Story anketi: "Pişi mi, gözleme mi?"
- **K3 — "Hafta sonu brunch"** · Hook: "Cumartesi sabahını köyde geçir." · Retargeting: "Bu hafta sonu kahvaltı için yerini ayır."

### Taş konak (T1–T2)
- **T1 — "600 yıllık miras"** · Hook: "Bu duvarlar 600 yıldır ayakta." · Reels: taş doku makro → oda → avlu. · Feed: "Osmanlı taş mimarisiyle restore, 16 özel oda." · Landing: `/`
- **T2 — "16 özel tasarım oda"** · Hook: "Hiçbir oda diğerine benzemiyor." · Landing: `/odalar`

### Canlı müzik (M1–M2)
- **M1 — "Akşam canlı müzik"** · Hook: "Akşam, taş avluda canlı müzik." · Reels: alaca karanlık, enstrüman, kalabalık siluet. · CTA: Rezervasyon + etkinlik takvimi. · Landing: `/gastronomi`
- **M2 — "Restoran akşamı"** · Hook: "Ege–Antakya sofrası + müzik." · Retargeting: "Bu cuma masan hazır olsun mu?"

### Düğün / nişan (D1–D2)
- **D1 — "Taş avluda düğün"** · Hook: "Hikâyeniz 600 yıllık bir avluda başlasın." · Feed: "Köy dokusunda butik düğün/nişan — 200 kişiye kadar." · CTA: Teklif al (Lead form / WhatsApp). · Landing: `/organizasyonlar`
- **D2 — "Nişan / kına"** · Hook: "Küçük, samimi, unutulmaz." · Retargeting: "Tarih müsaitliği için mesaj atın."

### 30 günlük içerik/test takvimi (özet)
| Hafta | Odak | Yayın |
|---|---|---|
| 1 | Ölçüm kapısı + marka/prospecting açılış | R1, K1, T1 (3 kreatif A/B) |
| 2 | Kahvaltı + taş konak test | K2, K3, T2 + en iyi hook'u ölçekle |
| 3 | Canlı müzik + retargeting | M1, M2 + retargeting havuzları |
| 4 | Düğün/organizasyon + kazananları ölçekle | D1, D2 + kazanan kreatifleri 2x bütçe |

---

## TESLİM #4 — KEYWORD DOSYASI

> Kaynak: `kads keywords` · `campaigns/google-editor/03_keywords.csv`. Eşleme: marka **[tam]+"öbeği"**, nonbrand **"öbeği"**, broad YALNIZCA smart bidding + veri sonrası.

### Marka (Marka grubu — [tam] + "öbek")
`kozbeyli konağı`, `kozbeyli konak`, `kozbeyli otel`, `kozbeyli konağı foça`, `kozbeyli konağı rezervasyon`

### NonBrand — Butik/Taş ("öbek")
`foça butik otel`, `foça taş ev otel`, `foça konak otel`, `foça köy oteli`, `foça otantik otel`, `kozbeyli köyü otel`, `yeni foça butik otel`, `yeni foça taş otel`

### NonBrand — Genel ("öbek")
`foça otel`, `foça otelleri`, `foça konaklama`, `foça deniz manzaralı otel`, `foça balayı oteli`, `foça evcil hayvan kabul eden otel`, `foça hafta sonu kaçamağı otel`, `yeni foça otel`, `yeni foça konaklama`

### NonBrand — Organizasyon / Restoran / Kahvaltı
`foça düğün mekanı`, `foça kır düğünü`, `foça nişan mekanı`, `foça organizasyon`, `foça köy kahvaltısı`, `foça kahvaltı mekanları`, `foça restoran`, `izmir taş konak otel`, `izmir butik köy oteli`

### Negatif keyword listesi (paylaşımlı)
`iş ilanı`, `iş`, `kariyer`, `personel`, `eleman`, `maaş`, `kiralık`, `satılık`, `arsa`, `emlak`, `fiyat düşük`, `ucuz`, `bedava`, `hostel`, `pansiyon`, `kamp`, `camping`, `glamping`, `devremülk`, `apart`, `booking`, `otelz`, `etstur`, `tatilsepeti`, `yandex`, `tripadvisor` (OTA/aggregator → direkt rezervasyona yönlendir), coğrafi alakasızlar (`bodrum`, `çeşme`, `alaçatı`, `kuşadası`).

---

## TESLİM #5 — TRACKING QA (18 madde)

> Durum: `kads tracking`. **Ölçüm güven skoru KAPI = 80+.** Altındaysa reklam ölçekleme YOK.

1. GTM container canlı (`GTM-KCG6B4MJ`) ✓
2. GA4 Config etiketi GTM içinde (`G-V3R66C3MEF`) — **EKSİK**
3. Google Ads Conversion Linker — **EKSİK**
4. Google Ads Conversion (`AW-800024713`) + Label — **EKSİK**
5. `begin_checkout` dataLayer event atıyor ✓
6. HMS onay sayfasında `purchase` event — **EKSİK** (rezervasyon hmshotel.net'te tamamlanıyor)
7. Meta Pixel PageView her sayfa ✓
8. Meta InitiateCheckout `/rezervasyon`'da ✓
9. Meta Purchase (onay sayfası) — **EKSİK**
10. Meta Advanced Matching — **KAPALI** (Events Manager 1 tık bedava)
11. Meta CAPI — **YOK**
12. Enhanced Conversions (web+leads) — kur
13. Consent Mode v2 + CMP — doğrula
14. `purchase.event_id = transactionId` (Pixel+CAPI+GA4 dedup) ✓ (kod hazır)
15. UTM standardı tüm reklam linklerinde ✓
16. Offline/call conversion import hazır (`kads conversions`) ✓
17. GSC + Bing doğrulama + sitemap — bekliyor
18. Test rezervasyonuyla uçtan uca doğrulama — **EKSİK** (kritik kapı)

### Event listesi
- **Meta:** PageView, ViewContent (oda), InitiateCheckout, Lead, Contact/WhatsAppClick, Purchase
- **GA4:** page_view, view_item, begin_checkout, generate_lead, purchase

### UTM standardı
`?utm_source={google|meta}&utm_medium={cpc|paid_social}&utm_campaign={marka|nonbrand|prospecting|retargeting|dugun}&utm_content={kreatif_id}`
Örnek: `...utm_source=meta&utm_medium=paid_social&utm_campaign=prospecting&utm_content=R1`

---

## TESLİM #6 — LANDING PAGE QA

### Reklam → sayfa eşleme matrisi
| Kreatif/Grup | Landing |
|---|---|
| Marka Search | `/rezervasyon` |
| NonBrand Butik/Genel | `/odalar` |
| Kahvaltı (K1–K3) | `/gastronomi` |
| Canlı müzik (M1–M2) | `/gastronomi` |
| Düğün (D1–D2) | `/organizasyonlar` |
| Romantik (R1–R3) | `/odalar` → `/rezervasyon` |

### 11 maddelik sayfa kontrolü
1. Reklam mesajı = sayfa başlığı (message match) · 2. Tek net CTA (Rezerve/WhatsApp) · 3. Mobil hız < 3sn · 4. Fiyat/müsaitlik görünür · 5. Telefon/WhatsApp tıklanır · 6. Foto galeri güncel · 7. Sosyal kanıt (yorum/puan) · 8. Konum + "Yeni Foça'ya yakın" (sabit yanlış km YOK) · 9. Evcil/kahvaltı/teras rozetleri · 10. Güven işaretleri (HMS güvenli ödeme) · 11. `begin_checkout` tetikleniyor.

### Sosyal kanıt düzeltmesi
Google puanı ~4.2 (rakipler 4.7–4.8). Sitede **son ve olumlu yorumları** öne çıkar; yıldız ortalamasını değil, taze yorum akışını göster. Yorum hızını artır (en yüksek getirili ÜCRETSİZ kaldıraç).

---

## TESLİM #7 — WHATSAPP SATIŞ

### Etiketler (HotelRunner/CRM veya manuel)
`sıcak-lead`, `fiyat-verildi`, `takip-1`, `takip-2`, `rezerve`, `kayıp`, `düğün-lead`, `grup`

### Şablonlar
- **İlk yanıt:** "Merhaba! Kozbeyli Konağı'na ilginiz için teşekkürler 🌿 Hangi tarihler ve kaç kişi için bakalım?"
- **Fiyat sonrası:** "{tarih} için {oda} müsait. Gecelik {fiyat} TL, organik köy kahvaltısı dahil. Doğrudan bizden rezerve ederseniz komisyon yok. Ayıralım mı?"
- **Takip-1 (24 saat):** "Merhaba, {tarih} için oda hâlâ müsait ama hızlı doluyor. Sizin için tutayım mı?"
- **Takip-2 (72 saat):** "Planınız netleşti mi? Esnek tarihlerde alternatif de önerebilirim."
- **Düğün lead:** "Organizasyonunuz için taş avlu + {kapasite} kişi uygun. Tarih ve kişi sayısını paylaşırsanız teklif hazırlayayım."

### Fiyat sonrası takip ritmi
0. saat fiyat → 24s takip-1 → 72s takip-2 → 7. gün son teklif → kapanmadıysa `kayıp` etiketi.

### Offline conversion geri besleme
Rezerve olan WhatsApp lead'i → `kads conversions` ile Google/Meta'ya **offline conversion** olarak yükle (GCLID/telefon eşleme) → algoritma gerçek satışı öğrenir.

### Haftalık kayıt tablosu (kolonlar)
`tarih · kaynak(utm) · isim · tarih_talebi · kişi · fiyat_verildi · durum · rezerve_tutar · not`

---

## TESLİM #8 — HAFTALIK OPTİMİZASYON

> Rutin: `kads monitor` + `kads rules`. Haftada 1, sabit gün.

### 13 maddelik kontrol
1. Ölçüm skoru hâlâ 80+ mı · 2. Harcama/bütçe pacing · 3. Marka vs NonBrand CVR · 4. En pahalı 5 keyword · 5. Negatif eklenecek arama terimi · 6. Meta frekans (>3 → yorgunluk) · 7. En iyi/en kötü kreatif · 8. Retargeting havuz büyüklüğü · 9. WhatsApp yanıt süresi · 10. Landing CVR · 11. OTA parite (HotelRunner) · 12. FBL/PMax rezervasyon · 13. Bütçe yeniden dağıtımı.

### 8 karar kuralı
1. **CTR düşük** (<%2 nonbrand) → hook değiştir (kreatif).
2. **Tıklama var, mesaj yok** → landing/teklif sorunu; sayfa + fiyatı gözden geçir.
3. **Mesaj var, rezerve yok** → WhatsApp takip ritmi + teklif cazibesi.
4. **Frekans > 3** → kreatif yenile veya kitle genişlet.
5. **Marka CVR yüksek + bütçe sınırlı** → önce markayı doyur.
6. **Bir keyword CPA hedefin 3x'i** → duraklat/negatif.
7. **Retargeting CPA en düşük** → payı artır (havuz yeterse).
8. **Ölçüm skoru 80 altına düştü** → TÜM ölçeklemeyi durdur, önce ölç.

---

## TESLİM #9 — RİSK LİSTESİ (10)
| # | Risk | Etki | Önlem |
|---|---|---|---|
| 1 | Ölçüm canlı değil | Kör harcama, 0 dönüşüm | GTM etiket + test rezervasyon (KAPI) |
| 2 | Yanlış event optimizasyonu | Algoritma boş event'e koşar | Düşük bütçede WhatsApp/Lead, veri sonra Purchase |
| 3 | Consent Mode v2 eksik | AB/AEA trafiği ölçülmez + uyum | Sertifikalı CMP + Consent Mode v2 |
| 4 | OTA parite bozulması | Booking/OTA cezası, güven kaybı | HotelRunner ile fiyat/müsaitlik senkron |
| 5 | Zayıf sosyal kanıt (4.2) | CTR/CVR düşer | Taze yorum kampanyası + yanıt |
| 6 | Bütçe parçalanması | Öğrenme fazına ulaşılamaz | Az ad set, ucuz event, marka önce |
| 7 | Marka teriminde OTA rekabeti | Komisyonlu tıklama | Marka Search + poz-1 pin savunma |
| 8 | Doğrulanmamış iddia (km, ödül) | Uyum/itibar riski | "Yeni Foça'ya yakın"; sabit yanlış sayı yok |
| 9 | Kreatif yorgunluğu | Frekans↑, CPM↑ | Haftalık kreatif rotasyonu |
| 10 | Landing hız/mobil | Tıklama israfı | < 3sn, tek CTA, message match |

---

## TESLİM #10 — 30 GÜN PLANI
| Gün | Faz | İş |
|---|---|---|
| 1–3 | **ÖLÇÜM KAPISI** | GTM GA4/Ads etiketi + Pixel Purchase + Consent Mode → test rezervasyonuyla doğrula. Skor 80+ olmadan reklam ölçekleme YOK. |
| 4–7 | Kreatif + açılış | Marka Search + Prospecting aç (düşük bütçe). R1/K1/T1 A/B. WhatsApp akışı hazır. |
| 8–14 | Test | 12 kreatifi rotasyonla test; en iyi hook/kitle belirle. NonBrand grupları izle. |
| 15–21 | Temizlik | Negatif ekle, kötü kreatif/keyword duraklat, landing düzelt, retargeting havuzu büyüsün. |
| 22–30 | Ölçekleme | Kazanan kreatif/kelimeleri 2x; FBL/PMax + remarketing payını artır; offline conversion besle. |

---

**Formül (özet):** Meta = talep yaratma · Google = talep yakalama · FBL/PMax = direkt rezervasyon · WhatsApp = satış kapatma · Site = güven · Tracking = bütçe koruma.

> İlgili: `kads deliver` (durum) · `kads tracking` (ölçüm) · `golive/GTM-KURULUM.html` · `audit/MCKINSEY-EXECUTIVE-SUMMARY.html` · `skills/ads-delivery/SKILL.md`.
