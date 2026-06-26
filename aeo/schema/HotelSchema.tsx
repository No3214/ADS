// Next.js server component — ana sayfaya/layout'a koy. Tek @graph ile Hotel+Restaurant+Website.
// Şema sayfadaki GÖRÜNÜR içerikle eşleşmeli. Sahte puan/yorum/ödül/fiyat YOK.
import hotel from "./hotel.jsonld";
import restaurant from "./restaurant.jsonld";

export default function HotelSchema() {
  const graph = {
    "@context": "https://schema.org",
    "@graph": [
      { ...hotel, "@id": "https://www.kozbeylikonagi.com/#hotel" },
      { ...restaurant, "@id": "https://www.kozbeylikonagi.com/#restaurant" },
      { "@type": "WebSite", "@id": "https://www.kozbeylikonagi.com/#website",
        "url": "https://www.kozbeylikonagi.com", "name": "Kozbeyli Konağı",
        "inLanguage": "tr-TR" }
    ]
  };
  return (
    <script type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(graph) }} />
  );
}
// Oda detay / SSS / gastronomi sayfalarında hotelroom/faqpage/restaurant şemalarını ayrı <script> ile ekle.
