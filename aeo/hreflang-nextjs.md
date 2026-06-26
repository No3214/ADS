# hreflang + Next.js 15 (TR/EN)

Site iki dilli ama makine-okunur hreflang tespit edilemedi. Her sayfaya ekle.

## generateMetadata (sayfa bazlı)
```ts
export async function generateMetadata({ params }) {
  return {
    alternates: {
      canonical: "https://www.kozbeylikonagi.com/odalar",
      languages: {
        "tr": "https://www.kozbeylikonagi.com/odalar",
        "en": "https://www.kozbeylikonagi.com/en/rooms",
        "x-default": "https://www.kozbeylikonagi.com/odalar"
      }
    }
  };
}
```

## sitemap.ts — her URL'ye alternates
```ts
{ url: "https://www.kozbeylikonagi.com/odalar", lastModified: new Date(),
  alternates: { languages: {
    tr: "https://www.kozbeylikonagi.com/odalar",
    en: "https://www.kozbeylikonagi.com/en/rooms" } } }
```

## Kurallar
- ISO kodları tire ile (`tr`, `en`), alt çizgi değil. `x-default` = TR.
- **Self-referencing zorunlu:** her dil sürümü kendisi dahil tüm dilleri listelesin (en sık hata).
- JSON-LD'yi server component'te `<script type="application/ld+json">` ile enjekte et (aeo/schema/HotelSchema.tsx).
- Public sayfaları SSG/ISR (`export const revalidate = 3600`); oda sayfalarında `generateStaticParams`.
