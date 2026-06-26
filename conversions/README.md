# conversions/ — Dönüşüm ölçüm döngüsü (online + offline)

`kads conversions` · `offline` · `enhanced` · `calls`.

16 odalı butik otelde rezervasyonun bir kısmı **telefon/WhatsApp**'tan kapanır. Bunları
Google/Meta'ya geri yüklemezsen algoritma sadece online `purchase`'i görür ve offline
kapanan müşteriye benzer kişileri **hedeflemez** → para boşa gider. Bu paket döngüyü kapatır.

- `gclid-capture.html` — reklamdan gelen ziyaretçinin GCLID/fbclid'ini yakala (forma + localStorage).
- `offline-import-template.csv` — Google Offline Conversion Import yükleme şablonu.
- `google-offline-import.md` — telefon/WhatsApp rezervasyonunu Google'a geri yükleme (OCI).
- `meta-offline-capi.md` — Meta offline/CAPI ile aynı (lead_id veya hash'li eşleşme).
- `enhanced-conversions.md` — Google Enhanced Conversions + Meta Advanced Matching + Consent Mode v2.
- Altyapı (event'ler, CAPI route, cross-domain): `tracking/`.
