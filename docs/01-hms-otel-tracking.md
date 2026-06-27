# 01 — HMS Otel Dönüşüm Takibi (Doğrulanmış Bulgu + Doğrulama)

## Bulgu (doğrulandı)

Rezervasyon motoru sağlayıcınız **HMS Otel (hmsotel.com)**. HMS'in kendi dokümanındaki
("Online Rezervasyon Takibi Nasıl Yapılır") örnek bağlantı:

```
https://hms-otel.hmshotel.net/?utm_source=instagram&utm_medium=page
```

Yani rezervasyon motoru **`hmshotel.net`** üzerinde çalışır, biçim:
`https://{otel-slug}.hmshotel.net/`. Bu, sitenizden (`kozbeylikonagi.com`) **AYRI bir
kayıtlı alan adıdır**.

### Bunun üç sonucu

1. **Çapraz alan (cross-domain) ölçümü ZORUNLU.** Alt alan adı değil, farklı kayıtlı alan
   söz konusu. Aynı GA4 ID her iki tarafta olmalı; linker'a `hmshotel.net` eklenmeli;
   `hmshotel.net` "istenmeyen yönlendirmeler"e konmalı. (Kod: `../tracking/ConsentAndGtm.tsx`)
2. **Akış tam sayfa yönlendirmedir** (iframe değil), çünkü kullanıcı `{slug}.hmshotel.net`
   adresine gider. Bu, çapraz alan linker'ın `<a>` tıklamasıyla çalışmasını gerektirir;
   JavaScript yönlendirmesi varsa ek yapılandırma gerekir.
3. **Onay sayfası davranışı kamuya açık DEĞİL.** HMS'in onay (teşekkür) sayfasında kendi
   GA4 `purchase` / `transaction_id` / `value` / `currency` değerlerinizi üretip
   üretemeyeceğiniz dokümante edilmemiştir. **Test rezervasyonu + HMS desteği** ile
   doğrulanmalıdır.

> HMS ayrıca kendi panelinde UTM tabanlı kanal takibi sunar ("Rezervasyon > Kanal
> Rezervasyon", "Kanal Kod" sütunu). Bu, GA4/Ads/Pixel dönüşümünüzün YERİNE geçmez;
> yalnızca HMS'in kendi içindeki kaynak takibidir.

## Doğrulanması gerekenler (HMS desteğine sorun)

1. Bizim otelin gerçek alt alanı nedir? (`kozbeyli-konagi.hmshotel.net` gibi)
2. Onay sayfası URL deseni nedir? (dönüşüm tetikleyicisi buna bağlanır)
3. Panelde **GA4 / GTM / Meta Pixel ID** girilebilecek bir alan var mı?
4. Onay sayfasına **kendi GTM container** veya **gtag/fbq snippet'i** ekleyebilir miyiz?
   (`../tracking/hms-confirmation-snippet.html`)
5. Onay sayfası `dataLayer` ile `transaction_id`, `value`, `currency` veriyor mu?
6. Ödeme akışı tam yönlendirme mi? (beklenen: evet)

## Test rezervasyonu kontrol listesi (reklam açmadan ÖNCE)

1. Ana sitede `view_item` ve `begin_checkout` GA4 DebugView'da görünüyor mu?
2. Gerçek bir test rezervasyonu yapın. `{slug}.hmshotel.net` onay sayfasında DevTools >
   Console: `window.dataLayer` içinde `purchase` + `transaction_id` + `value` +
   `currency: 'TRY'` var mı?
3. Alanlar arası geçişte hedef URL'de `_gl=` parametresi var mı? Her iki alanda `_ga`
   çerezi aynı değeri taşıyor mu? (Tag Assistant / DevTools)
4. Meta Events Manager > Test Events: `Purchase` (ve `InitiateCheckout`) düşüyor mu?
5. Google Ads dönüşümü "kaydedildi" mi?

## Eğer onay sayfasına tag konulamıyorsa (yedek plan)

- **Offline Conversion Import (çevrimdışı dönüşüm yükleme):** HMS rezervasyon no'sunu
  GCLID/WBRAID ile eşleyip Google Ads'e periyodik yükleyin. Rezervasyon değeri ve tarihi
  ile gerçek dönüşümü sonradan içeri aktarır.
- **Enhanced Conversions for Leads:** Form/telefon lead'lerini hash'li e-posta/telefon ile
  eşleyip kapanan rezervasyonu offline raporlayın.
- **Meta CAPI (sunucu tarafı):** Pixel onay sayfasına konamıyorsa, rezervasyon
  tamamlandığında sunucudan Conversions API ile `Purchase` gönderin (aynı `event_id`).

Bu yedekler, "onay sayfasına dokunamıyoruz" durumunda bile ölçümü kurtarır; ancak ilk
tercih her zaman onay sayfasında doğrudan `purchase` olayıdır.
