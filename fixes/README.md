# fixes/ — Dijital denetim düzeltmeleri (docs/09 → kopyala-yapıştır)

`docs/09` / `kads presence fixes` bulgularını uygulanabilir çözümlere çevirir. **Kanonik
domain kararı: `kozbeylikonagi.com`** (tek aktif domain; gerçek metin sitesi orada). `.com.tr` TERK EDİLDİ —
seçersen kaynak/hedefi ters çevir.

| # | Düzeltme | Dosya |
|---|---|---|
| 1,2,3 | Domain birleştirme (301) | `01-domain-birlestirme/` |
| (güvenlik) | Güvenlik başlıkları (HSTS/CSP...) | `02-guvenlik-basliklari/` |
| 5 | schema.org JSON-LD gömme | `03-schema/` |
| 4 | Tek NAP standardı (GBP+OTA+sosyal) | `04-nap-standart.md` |
| 6 | HMS cross-domain — destek talebi | `05-hms-destek-talebi.md` |
| 8 | TripAdvisor/Google yorum toplama | `06-yorum-toplama-sablonlari.md` |
| 11 | hreflang TR/EN | `07-hreflang.md` |

> Her dosya **şablondur**; gerçek host/altyapına göre uyarla. Production'a almadan önce
> staging'de dene (docs/12).
