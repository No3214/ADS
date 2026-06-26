# hreflang (TR/EN) — .com

Her sayfanın TR ve EN sürümü birbirine işaret etmeli (uluslararası hedefleme).

## Next.js App Router (metadata)
```ts
// app/[locale]/page.tsx
export const metadata = {
  alternates: {
    canonical: "https://www.kozbeylikonagi.com/",
    languages: {
      "tr-TR": "https://www.kozbeylikonagi.com/",
      "en":    "https://www.kozbeylikonagi.com/en",
      "x-default": "https://www.kozbeylikonagi.com/"
    }
  }
};
```

## Ham HTML (<head>)
```html
<link rel="alternate" hreflang="tr-TR" href="https://www.kozbeylikonagi.com/" />
<link rel="alternate" hreflang="en" href="https://www.kozbeylikonagi.com/en" />
<link rel="alternate" hreflang="x-default" href="https://www.kozbeylikonagi.com/" />
```
Her sayfa çiftinde karşılıklı (reciprocal) olmalı; aksi halde Google yok sayar.
