# Dönüşüm Takibi Kurulumu (Next.js 15 + GTM + GA4 + Meta) — Kozbeyli Konağı

Bu klasör, "önce ölçüm, sonra trafik" ilkesinin kod tarafıdır. Reklam açmadan
önce bu kurulum bir test rezervasyonuyla doğrulanmalıdır.

## Doğrulanmış kritik gerçek

Rezervasyon motoru **ayrı bir kayıtlı alan adındadır**: `{slug}.hmshotel.net`
(siteniz `kozbeylikonagi.com.tr` değil). HMS'in kendi dokümanındaki örnek:
`https://hms-otel.hmshotel.net/`. Bu yüzden **çapraz alan (cross-domain) ölçümü
zorunludur**. Aynı GA4 ID her iki alanda bulunmalı ve linker'a `hmshotel.net`
eklenmelidir. Detay ve doğrulama: `../docs/01-hms-otel-tracking.md`.

## Dosyalar

| Dosya | Görev |
|---|---|
| `ConsentAndGtm.tsx` | Consent Mode v2 (varsayılan denied) + GTM yükleyici + çapraz alan linker. `app/layout.tsx` içine konur. |
| `events.ts` | `purchase`, `begin_checkout`, `generate_lead`, `view_item`, `search` için tip güvenli yardımcılar. Aynı `event_id` ile Meta CAPI tekilleştirme. |
| `hms-confirmation-snippet.html` | HMS onay sayfasına (kendi HTML/etiket eklenebiliyorsa) konacak saf snippet. |

## Kurulum sırası

1. **GTM container'ı seçin.** İki aday var (`GTM-KCG6B4MJ`, `GTM-MSL2FLF5`).
   Canlı olanı `../docs/02-gtm-resolution.md` ile belirleyin. `NEXT_PUBLIC_GTM_ID`
   değişkenine yazın.
2. **Bileşeni yerleştirin.** `app/layout.tsx`:
   ```tsx
   import ConsentAndGtm from './_analytics/ConsentAndGtm';

   export default function RootLayout({ children }: { children: React.ReactNode }) {
     return (
       <html lang="tr">
         <body>
           <ConsentAndGtm />
           {children}
         </body>
       </html>
     );
   }
   ```
3. **Etiketleri GTM içinde kurun** (koda gömmeyin): GA4 Configuration (`G-V3R66C3MEF`),
   Google Ads Conversion (`AW-800024713`, "Satın alma" kategorisi), Meta Pixel
   (`1781546559309505`). Tetikleyiciler: `purchase`, `begin_checkout`, `generate_lead`.
4. **Çapraz alanı açın.** GA4 > Yönetici > Veri Akışları > Web > Etiket ayarları >
   Alanlarınızı yapılandırın: `kozbeylikonagi.com.tr` **ve** `hmshotel.net`. Ardından
   `hmshotel.net`'i "istenmeyen yönlendirmeler" listesine ekleyin.
5. **HMS onay sayfası.** HMS panelinde GA4/GTM/Pixel ID alanı varsa aynı ID'leri
   girin. Yoksa `hms-confirmation-snippet.html` içeriğini onay sayfasına eklemeyi
   HMS desteğinden isteyin. Hiçbiri mümkün değilse **offline conversion import**
   (docs/01) kullanın.
6. **CMP onayını bağlayın.** Çerez izni "Kabul Et" butonu `grantConsent()` çağırmalı
   (sayfa geçişinden önce).

## Çift platform olay eşlemesi

| Funnel adımı | GA4 olayı | Google Ads | Meta Pixel/CAPI | Değer |
|---|---|---|---|---|
| Oda görüntüleme | `view_item` | — | `ViewContent` | — |
| Tarih araması | `search` | — | `Search` | — |
| Rezervasyona giriş | `begin_checkout` | (ops.) | `InitiateCheckout` | `value` + TRY |
| Rezervasyon tamam | `purchase` | **Satın alma** (transaction_id) | `Purchase` (event_id) | `value` + TRY |
| Telefon/WhatsApp/form | `generate_lead` | (ops. dönüşüm) | `Lead` / `Contact` | — |

`transaction_id` (Google) ve `event_id` (Meta) her dönüşümün **bir kez** sayılmasını
sağlar. Depozito + bakiye gibi çift ateşlemelere karşı kritiktir.

## Gelişmiş Dönüşümler (Enhanced Conversions)

Onay sayfasında SHA-256 ile hash'lenmiş e-posta/telefon Google'a gönderilir; çerez
kaybı ve consent reddinde doğruluğu artırır, Consent Mode ile birlikte çalışır ve
Smart Bidding'i besler. Meta tarafında karşılığı CAPI'dir (sunucu tarafı olay).

## Doğrulama (reklam açmadan ÖNCE)

1. GA4 DebugView'da `view_item` → `begin_checkout` görülmeli.
2. Bir **test rezervasyonu** yapın; `hmshotel.net` onay sayfasında `purchase`,
   `transaction_id`, `value`, `currency=TRY` üretiliyor mu kontrol edin (DevTools >
   `window.dataLayer`).
3. Alanlar arası geçişte hedef URL'de `_gl=` parametresi, her iki alanda aynı `_ga`
   çerezi olmalı (Tag Assistant / DevTools).
4. Meta Events Manager > Test Events'te `Purchase`/`InitiateCheckout`/`Lead` görülmeli.
5. Google Ads dönüşümü test rezervasyonunda "kaydedildi" olmalı.

Bu beş madde geçmeden hiçbir kampanya `ENABLED` yapılmaz.
