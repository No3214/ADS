# GA4 Çapraz Alan (cross-domain) — ZORUNLU

Site `kozbeylikonagi.com`, rezervasyon `kozbeyli-konagi.hmshotel.net` → AYRI alan adı.

## GA4 Admin
1. Admin > Data Streams > web stream (`G-V3R66C3MEF`) > Configure tag settings >
   **Configure your domains** → ekle: `kozbeylikonagi.com` VE `hmshotel.net`.
2. **List unwanted referrals** → ekle: `hmshotel.net` (self-referral'ı engelle).
3. Linker otomatik `_gl` parametresini `<a>` tıklamasında taşır. JS yönlendirmesi varsa
   `_gl`'yi elle ekle (HMS tam sayfa yönlendirme → genelde otomatik çalışır).

## Doğrulama
- Siteden HMS'e geçişte hedef URL'de `_gl=` var mı? (DevTools / Tag Assistant)
- Her iki alanda `_ga` çerezi aynı değeri taşıyor mu? → tek kullanıcı/oturum.
- Onay sayfasında purchase aynı oturuma bağlanıyor mu?

## Onay sayfasına erişemiyorsan (yedek)
Offline Conversion Import (GCLID/WBRAID eşleme) + Enhanced Conversions for Leads + Meta CAPI
(sunucu tarafı). Bkz docs/01 + fixes/05 (HMS destek talebi).
