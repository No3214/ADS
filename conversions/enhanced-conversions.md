# Enhanced Conversions + Advanced Matching

`kads conversions enhanced`. Çerez sonrası dünyada eşleşmeyi güçlendirir.

## Google Enhanced Conversions
- `purchase` anında hash'li **e-posta/telefon** gönder (gtag/GTM Enhanced Conversions).
- **Consent Mode v2 şart** (tracking/implementation/01). Rıza yoksa modelleme devreye girer.
- Etkisi: kaybolan dönüşümlerin bir kısmını geri kazanır; daha doğru ROAS.

## Meta Advanced Matching + CAPI
- Pixel + CAPI birlikte; hash'li `em/ph/fn/ln`. Aynı `event_id` ile dedup.
- EMQ skorunu izle (>6 hedefle).

## Consent Mode v2 (her ikisi)
- TR/AB rıza durumunu sinyalle; rızasız trafikte modelli dönüşüm.
- Kurulum: `tracking/implementation/01-consent-mode-v2.html` + `tracking/ConsentAndGtm.tsx`.
