# Mobil & Responsive Kontrol

Trafik ağırlıklı mobil → mobil öncelik. Tailwind breakpoint'leri: sm 640 / md 768 / lg 1024 / xl 1280.

## Kontrol listesi
- [ ] `<meta name="viewport" content="width=device-width, initial-scale=1">` (Next.js viewport export).
- [ ] Yatay kaydırma YOK (taşan görsel/tablo). `max-w-full`, `overflow-x` kontrol.
- [ ] Dokunma hedefleri ≥ 44×44px; CTA'lar parmak dostu; yakın linkler arası boşluk.
- [ ] Görseller responsive (`sizes`, next/image); mobilde hero tek kare, hafif.
- [ ] Yazı ≥ 16px gövde (zoom engelleme yok). Satır uzunluğu okunur.
- [ ] Sticky/sabit CTA mobilde içeriği kapatmasın; "rezervasyon" kolay erişilir.
- [ ] Menü: erişilebilir hamburger (aria-expanded, focus tuzağı yok), dil değiştirici çalışır.
- [ ] Form alanları mobilde tam genişlik; doğru `inputmode`/`autocomplete` (tel/email/date).
- [ ] Tablolar mobilde stack/scroll; harita/galeri mobilde performanslı (lazy).

## Test
Chrome DevTools cihaz emülasyonu (iPhone/Android), gerçek cihaz, Lighthouse mobil, 360px genişlik
ekstrem testi. Kırık nokta: en dar ekranda da düzgün.
