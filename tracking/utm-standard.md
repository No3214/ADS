# UTM Standardı — Kozbeyli Konağı

Tutarlı UTM = temiz attribution. Tutarsız etiket (Meta vs meta, boşluk vs tire) GA4'te
trafiği böler ve raporu bozar. Her ücretli/paylaşılan linki bu standarda göre etiketle.

## Üretici (önerilen)
```
kads utm build --url https://www.kozbeylikonagi.com/odalar --channel google-pmax
kads utm build --url https://www.kozbeylikonagi.com/odalar --source meta --medium paid_social --campaign retargeting --content reel-01
```
`kads utm` tüm kanal matrisini, `kads utm rules` kuralları gösterir.

## Kurallar
- **Küçük harf** (GA4 büyük/küçük ayırır): `utm_source=meta`.
- **Boşluk yok**, tire kullan: `utm_campaign=yaz-2026`.
- `utm_source` = platform (google/meta/instagram/email), `utm_medium` = tür
  (cpc/paid_social/email/organic/display), `utm_campaign` = amaç (brand/pmax/retargeting).
- `utm_term` = paid search kelimesi, `utm_content` = A/B reklam/kreatif varyantı.
- **Marka Search'i elle etiketleme**: Google auto-tagging (gclid) zaten bağlar; UTM gclid'i ezmesin.

## Matris
Kanal → source/medium/campaign eşlemesi: `tracking/utm-matris.csv` (kads ile üretildi).
