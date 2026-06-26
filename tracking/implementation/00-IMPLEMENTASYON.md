# Ölçüm İmplementasyonu — `.com` + `hmshotel.net` (master rehber)

Amaç: doğru, dedup'lı dönüşüm ölçümü. Sıra: Consent v2 → GTM tag'leri → GA4 cross-domain
→ dataLayer olayları → Meta CAPI. Bunlar kurulmadan kampanya ENABLE EDİLMEZ (docs/03, golive).

Bilinen ID'ler: GA4 `G-V3R66C3MEF` · Google Ads `AW-800024713` · Meta Pixel `1781546559309505`
· GTM `GTM-KCG6B4MJ` veya `GTM-MSL2FLF5` (docs/02 ile canlı olanı seç) · Motor `kozbeyli-konagi.hmshotel.net`.

Dosyalar:
- `01-consent-mode-v2.html` — Consent Mode v2 default (denied) + güncelleme (KVKK-güvenli).
- `02-gtm-tag-spec.md` — GTM'de kurulacak değişken/tetikleyici/tag listesi.
- `03-ga4-cross-domain.md` — GA4 admin çapraz alan + referral exclusion.
- `04-datalayer-events.md` — site + HMS onay sayfası dataLayer olay şeması.
- `05-meta-capi-route.ts` — sunucu tarafı Meta CAPI (event_id dedup) Next.js route.

Doğrulama (golive Faz 2): test rezervasyonu → GA4 DebugView + Meta Test Events'te
**aynı event_id ile tek Purchase** ("2 kaynaktan 1 olay"). Geçmeden trafik açma.
