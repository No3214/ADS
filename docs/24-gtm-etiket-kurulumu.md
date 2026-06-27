# 24 — GTM Etiket Kurulumu (GA4 + Google Ads dönüşüm)

Tarayıcıda canlı doğrulandı (Haz 2026): **GTM-KCG6B4MJ sitede CANLI**, Meta Pixel canlı, `begin_checkout`
(GA4 tarzı) + `InitiateCheckout` (Meta) event'leri **atıyor**. Eksik tek şey: GTM container'ın **içinde**
GA4 + Google Ads etiketleri yok → Google Ads **0 dönüşüm** gösteriyor. Bu doküman o boşluğu kapatır.
Özet durum: `kads tracking`.

## 0. ÖN KOŞUL — container erişimi (önce bunu doğrula)
`tagmanager.google.com` → **GTM-KCG6B4MJ** container'ını görüyor + açıp **Tags** ekleyebiliyor musun?
- **Evet** → Bölüm 1'e geç.
- **Hayır (eski/başka bir hesabında)** → iki seçenek:
  1. Ajanstan container'a kullanıcı erişimi / transfer iste, veya
  2. **Kendi container'ını oluştur** → sitedeki GTM ID'sini onunla değiştir (Next.js'te GTM snippet/`ConsentAndGtm.tsx`)
     → bu dokümandaki etiketleri temiz kur. (Site sizde olduğu için ID değişimi sizde.)

## 1. GA4 Configuration (Google Tag)
- Tür: **Google Tag** / GA4 Configuration · Measurement ID: **G-V3R66C3MEF**
- Tetikleyici: **All Pages (Initialization - All Pages)**
- Amaç: GA4'e sayfa görüntüleme + temel event akışı.

## 2. Google Ads Conversion Linker
- Tür: **Conversion Linker** · Tetikleyici: **All Pages**
- Amaç: tıklama bilgisini (gclid) çereze yaz; dönüşüm atfı için **şart**.

## 3. Google Ads Conversion Tracking (asıl dönüşüm)
- Tür: **Google Ads Conversion Tracking** · Conversion ID: **AW-800024713** · Conversion Label: (Google Ads'te oluştur, aşağıda)
- Tetikleyici: **Custom Event = `begin_checkout`** (rezervasyon başlangıcı; site bunu zaten atıyor)
- İdeal ikinci aşama: HMS onay/teşekkür sayfasında `purchase` event'i ile **tamamlanan** rezervasyon (gerçek dönüşüm).

## 4. (Önerilir) GA4 Event — begin_checkout
- Tür: GA4 Event · Event name: `begin_checkout` · Tetikleyici: Custom Event `begin_checkout`
- Amaç: GA4 huni analizi (başlangıç→tamamlanma).

## 5. Google Ads tarafı — Conversion action
`ads.google.com` → Araçlar → **Dönüşümler** → Yeni:
- Tür: Website (veya Import). Ad: "Rezervasyon başlangıcı" (ve ayrı: "Rezervasyon tamamlandı").
- Oluşan **Conversion Label**'ı Bölüm 3'teki GTM etiketine yapıştır.
- Değer: rezervasyon başı ortalama (veya HMS'ten gerçek) — ROAS için.
- Mikro-dönüşüm (opsiyonel): WhatsApp/telefon/harita tıklaması.

## 6. HMS Purchase (tamamlanan rezervasyon — en kritik)
Rezervasyon `hmshotel.net`'te (ayrı domain) tamamlanıyor; ana sitedeki pixel/etiket orayı görmüyor.
- HMS onay/teşekkür sayfasına: GA4 `purchase` + Google Ads conversion + **Meta `Purchase`** (value+currency=TRY).
- Hazır şablon: `tracking/hms-confirmation-snippet.html`. Cross-domain: GA4 allowLinker `.com` ↔ `hmshotel.net` + referral exclusion.

## 7. Yayın + doğrulama (reklam öncesi ŞART)
1. GTM **Submit → Publish** (yayınlamadan canlı olmaz).
2. GTM **Preview** + Tag Assistant → GA4 Config + Conversion Linker All Pages'te ateşliyor mu?
3. **Test rezervasyon** → GA4 **DebugView**'da `begin_checkout`/`purchase`; Google Ads → Dönüşümler "kaydediliyor"a geçti mi?
4. Yeşilse: yeni temiz kampanya paketi (`campaigns/google-editor/`) Editor'dan import → enable; eski 8 kampanya kapalı kalsın.

## Sıra (özet)
container erişimi → GA4 Config + Conversion Linker + Conversion (begin_checkout) → Ads conversion action →
HMS Purchase → Publish → test rezervasyonla doğrula → ancak sonra reklam enable. Durum takibi: `kads tracking`.
Sahip-dostu tek sayfa: `golive/GTM-KURULUM.html`.
