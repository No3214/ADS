# Google Ads Editor — Import Rehberi (Kozbeyli Konağı)

Bu klasördeki CSV'ler **import-hazırdır** ve tüm kampanyaları **PAUSED** oluşturur.

## Adımlar
1. Google Ads Editor'ü aç, doğru hesabı (10 haneli müşteri ID) indir.
2. **Account > Import > From file** ile sırasıyla CSV'leri içeri al:
   `01_campaigns` → `02_ad_groups` → `03_keywords` → `04_responsive_search_ads`
   → `05_negative_keywords` → `06_sitelinks` → `07_callouts` → `08_structured_snippets`.
3. Her import sonrası "Check changes" ile önizle. **Post etmeden** her şeyi review et.
4. Bütçeler **günlük TRY**; bid stratejisi **Maximize Clicks + CPC limiti**.
5. Post et → kampanyalar **PAUSED** hesapta oluşur.
6. ENABLE etme; ölçüm test rezervasyonuyla doğrulanana kadar bekle (docs/03).
   ENABLE gerektiğinde `/kozbeyli-ads-change` + `kads guard` ile ikinci onay.

## Notlar
- Negatifler paylaşılan liste olarak gelir; non-brand + test kampanyalarına bağla.
- RSA başlıkları ≤30, açıklamalar ≤90 karakter (kads validate ile doğrulandı).
- Uzantılar (sitelink/callout/snippet) Editor'de ilgili sekmelere paste edilebilir.
- Konum: şehir hedefi (radius değil). Dil: Türkçe.
