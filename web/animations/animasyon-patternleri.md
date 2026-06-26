# Animasyon (zarif + erişilebilir)

Butik otel = sakin, zarif, abartısız. Animasyon dikkat dağıtmamalı, performansı düşürmemeli,
**`prefers-reduced-motion`'a saygı** göstermeli.

## İlkeler
- Sadece `transform` + `opacity` anime et (GPU; reflow yok). `top/left/width` animasyonundan kaçın.
- Süre 150–400ms, yumuşak easing (ease-out giriş). Aşırı paralaks/otomatik kaydırma yok.
- Scroll-reveal hafif (fade/slide 8–16px). Hero'da içeriği geciktirme (LCP'yi bozma).
- Hover: masaüstünde ince; mobilde hover yok → tıkla durumuna güven.
- `prefers-reduced-motion: reduce` → animasyonları kapat (odak-stilleri.css zaten yapıyor).

## CSS (hafif reveal)
```css
@media (prefers-reduced-motion: no-preference) {
  .reveal { opacity: 0; transform: translateY(12px); transition: opacity .4s ease, transform .4s ease; }
  .reveal.in { opacity: 1; transform: none; }
}
```
IntersectionObserver ile `.in` ekle. Framer Motion kullanıyorsan `motion-ornek.tsx`.
