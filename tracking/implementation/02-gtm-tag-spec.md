# GTM Tag Spesifikasyonu (canlı container'da kur)

> Önce docs/02 ile canlı container'ı belirle (`GTM-KCG6B4MJ` / `GTM-MSL2FLF5`). Çift container varsa birini arşivle.

## Değişkenler (Variables)
- DLV - `transaction_id`  (Data Layer Variable)
- DLV - `value`
- DLV - `currency`  (varsayılan TRY)
- DLV - `items` (opsiyonel, GA4 e-ticaret)

## Tetikleyiciler (Triggers)
- `purchase` — Custom Event = `purchase`
- `begin_checkout` — Custom Event = `begin_checkout`
- `view_item` — Custom Event = `view_item`
- Consent Initialization - All Pages

## Tag'ler
1. **GA4 Configuration** — Measurement ID `G-V3R66C3MEF`; Fields: `send_page_view=true`.
   Consent: analytics_storage gerektirir. (Cross-domain GA4 admin'de, bkz 03.)
2. **GA4 Event - purchase** — Event name `purchase`; params: transaction_id, value, currency, items.
   Trigger: `purchase`.
3. **GA4 Event - begin_checkout** — Trigger: `begin_checkout`.
4. **Google Ads Conversion** — Conversion ID `AW-800024713`, Label `<DÖNÜŞÜM_ETIKETI>` (Ads'te oluştur);
   value `{{DLV - value}}`, currency `{{DLV - currency}}`, transaction_id `{{DLV - transaction_id}}`.
   Trigger: `purchase`. **Enhanced Conversions: AÇIK** (e-posta/telefon hash).
5. **Google Ads Remarketing** — `AW-800024713` (liste için; Google Display ertelense de listeyi besle).
6. **Meta Pixel - Base** — Custom HTML (Pixel `1781546559309505`) tüm sayfalar, Consent: ad_storage.
7. **Meta Pixel - Purchase** — `fbq('track','Purchase',{value,currency,...},{eventID:'{{DLV - transaction_id}}'})`.
   `eventID` = transaction_id → CAPI ile dedup. Trigger: `purchase`.

## Notlar
- Tüm pazarlama tag'leri Consent v2'ye saygılı (GTM consent ayarları).
- Onay (HMS) sayfası ayrı domain → 04'teki dataLayer + 03'teki cross-domain şart.
