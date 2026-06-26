# Bundle Boyutu Analizi + Hedefler

## Kurulum
```bash
npm i -D @next/bundle-analyzer
```
```js
// next.config.js'i sarmala
const withAnalyzer = require('@next/bundle-analyzer')({ enabled: process.env.ANALYZE === 'true' });
module.exports = withAnalyzer(nextConfig);
```
```bash
ANALYZE=true npm run build   # tarayıcıda treemap açılır
```

## Hedefler / kontrol
- İlk yük JS (route) **< ~150–170 KB gzip**. Büyük bağımlılıkları `next/dynamic` ile ertele.
- `optimizePackageImports` ile ikon/util paketlerini tree-shake et.
- Kullanılmayan CSS/JS, çift kütüphane, ağır moment/lodash → hafif alternatif.
- Görseller AVIF/WebP + doğru `sizes`. Üçüncü taraf script'leri `next/script` strategy="lazyOnload".
- Lighthouse Performance ≥ 90 (mobil) hedefle; saha (CrUX) için CWV "Good".
