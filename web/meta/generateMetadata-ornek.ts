// Tam meta + OpenGraph + Twitter + canonical + hreflang (Next.js App Router).
import type { Metadata } from "next";
export async function generateMetadata({ params }: { params: { locale?: string } }): Promise<Metadata> {
  const url = "https://www.kozbeylikonagi.com/odalar";
  return {
    metadataBase: new URL("https://www.kozbeylikonagi.com"),
    title: "Odalar | Kozbeyli Konağı — Foça Butik Taş Otel",
    description: "Foça'da 600 yıllık köyde 16 odalı butik taş konak. Manzaralı odalar, organik köy kahvaltısı, doğrudan rezervasyon.",
    alternates: {
      canonical: url,
      languages: { tr: url, en: "https://www.kozbeylikonagi.com/en/rooms", "x-default": url },
    },
    openGraph: {
      type: "website", url, siteName: "Kozbeyli Konağı", locale: "tr_TR",
      title: "Kozbeyli Konağı — Foça Butik Taş Otel",
      description: "600 yıllık Kozbeyli köyünde tarihi taş konak. Ege manzarası, köy kahvaltısı.",
      images: [{ url: "/opengraph-image", width: 1200, height: 630, alt: "Kozbeyli Konağı" }],
    },
    twitter: { card: "summary_large_image", title: "Kozbeyli Konağı", description: "Foça'da 600 yıllık taş konak otel.", images: ["/opengraph-image"] },
    robots: { index: true, follow: true, "max-image-preview": "large" },
  };
}
