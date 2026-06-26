# web/ — Frontend uygulama paketi (kozbeylikonagi.com, Next.js 15)

Sitenin (ayrı Next.js + Payload CMS kod tabanı) performans, erişilebilirlik, PWA, meta/OG,
responsive ve animasyon işlerini **drop-in kod/config** olarak verir. aeo/ + fixes/ ile birleşir.

| Alan | Klasör | Öne çıkan |
|---|---|---|
| Performans | `performance/` | next.config (AVIF/WebP, cache), next/image lazy, dynamic import, next/font, web-vitals→GA4, bundle analiz |
| Erişilebilirlik (WCAG AA) | `accessibility/` | kontrol listesi, skip link + focus + form snippet, kontrast, reduced-motion CSS |
| Meta / OpenGraph | `meta/` | tam generateMetadata (OG/Twitter/canonical/hreflang) + dinamik opengraph-image |
| PWA | `pwa/` | geçerli manifest.webmanifest + Serwist SW kurulumu + ikon notu |
| Mobil / responsive | `responsive/` | kontrol listesi + viewport (zoom engelleme yok) |
| Animasyon | `animations/` | reduced-motion saygılı, transform/opacity-only zarif reveal |

## Hedefler (Lighthouse, mobil)
Performance ≥ 90 · Accessibility ≥ 95 · Best Practices ≥ 95 · SEO ≥ 95 · PWA installable.
CWV (saha): **LCP < 2.5s · INP < 200ms · CLS < 0.1**.

## Doğrulama
Lighthouse (mobil) + axe DevTools + WAVE + klavye-only tur + gerçek cihaz + `web-vitals` saha verisi.
Şema/SEO için aeo/ (Rich Results Test). Güvenlik başlıkları fixes/02 ile birleştir.

> Drop-in kod örnektir; sitenin gerçek bileşen/yollarına uyarlanır. Komut: `kads web` (kontrol listesi).
