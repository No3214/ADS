# PWA Kurulumu (Next.js 15 + Serwist)

PWA = yüklenebilir + hızlı tekrar ziyaret + (opsiyonel) offline. Otel için: ana sayfa/odalar
cache → tekrar ziyaret hızı; rezervasyon (HMS) her zaman ağdan.

## 1) Manifest
`web/pwa/manifest.webmanifest` → `public/manifest.webmanifest`. layout metadata:
```ts
export const metadata = { manifest: "/manifest.webmanifest", themeColor: "#3f6b4f" };
```
İkonlar: 192 / 512 / maskable-512 (public/icons/). Apple için `apple-touch-icon` (180x180).

## 2) Service worker (Serwist — next-pwa'nın güncel halefi)
```bash
npm i @serwist/next && npm i -D serwist
```
```ts
// next.config.js'i withSerwist ile sarmala; app/sw.ts service worker.
// Stratejiler: statik varlık + sayfalar = StaleWhileRevalidate; /api ve hmshotel.net = NetworkOnly.
```
- Rezervasyon/ödeme akışını ASLA cache'leme (NetworkOnly). Sürüm atlamada cache temizliği (skipWaiting).
- Offline fallback sayfası opsiyonel (örn. /offline).

## 3) Doğrulama
Lighthouse PWA denetimi (yüklenebilir, manifest geçerli, SW kayıtlı), Chrome > Application > Manifest.
> Not: PWA "şart" değil; tekrar ziyaret hızı + "ana ekrana ekle" deneyimi için artı. Karmaşıklığı
> ölçülü tut; rezervasyon güvenilirliği > offline.
