// .com (Next.js App Router) — schema.jsonld'yi sayfaya gömer.
// app/layout.tsx veya ana sayfada <JsonLd /> olarak kullan. Rich Results Test ile doğrula.
import schema from "./schema.jsonld";   // veya aşağıdaki nesneyi inline yapıştır

export default function JsonLd() {
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}
// NOT: 'url' ve 'image' alanları kanonik domaine (.com) göre güncel olmalı.
// Restoran için ayrı Restaurant şeması + SSS için FAQPage şeması da eklenebilir (docs/09 #5).
