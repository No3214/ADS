# attribution/ — Ölçüm ve atıf modeli

Hangi temasın dönüşümü aldığı + Google/Meta çift sayımının nasıl çözüldüğü.
CLI: `kads attribution`. Kurulum: `tracking/`.

- `model.md` — katman katman model (GA4 DDA, Google Ads DDA, Meta 7-1, dedup, blended).
- Cross-domain ZORUNLU (purchase HMS'te olur): `tracking/implementation/03-ga4-cross-domain.md`.
- purchase tekilliği: `transaction_id` (HMS rez. no). Meta CAPI: `event_id` dedup (tracking/05).
