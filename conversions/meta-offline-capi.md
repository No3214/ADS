# Meta Offline / Conversions API — offline rezervasyon

`kads conversions offline`. Meta'da GCLID yok; eşleşme **lead_id** veya **hash'li** kişi
verisiyle (em=e-posta, ph=telefon) yapılır.

## Akış
1. Kaynak: Meta Lead Form ise `lead_id`; değilse hash'li `em`/`ph` (SHA-256, küçük harf, trim).
2. Rezervasyon kapanınca **Conversions API** ile `Purchase` (offline) event'i gönder:
   `value` + `currency=TRY` + `event_id` + (varsa) `lead_id` / hash'li kullanıcı verisi.
3. **Dedup**: online Pixel `purchase` ile **aynı event_id** → çift sayma (tracking/implementation/05).
4. **Eşleşme kalitesi (EMQ)**: hedef >6. Ne kadar çok hash'li alan, o kadar iyi atıf.

## Not
- CAPI route hazır: `tracking/implementation/05-meta-capi-route.ts` (event_id dedup içeriyor).
- Consent Mode v2 / rıza: `tracking/implementation/01-consent-mode-v2.html`.
