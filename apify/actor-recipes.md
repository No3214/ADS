# Apify Actor Reçeteleri (call-actor input JSON)

> Google Maps URL'sini Google İşletme Profili'nden al (pin → "Paylaş" linki). TripAdvisor
> URL'si doğrulandı (aşağıda). Her reçetede maxItems/maxReviews ile maliyeti sınırla.

## 1) Kendi Google yorumları (haftalık izle)
actor: `compass/Google-Maps-Reviews-Scraper`
```json
{ "startUrls": [{ "url": "<KOZBEYLI_GOOGLE_MAPS_URL>" }],
  "maxReviews": 20, "reviewsSort": "newest", "language": "tr", "personalData": false }
```

## 2) Rakip Google yorumları
actor: `compass/Google-Maps-Reviews-Scraper`
```json
{ "startUrls": [
    { "url": "<BULBUL_YUVASI_MAPS_URL>" },
    { "url": "<HURI_NURI_MAPS_URL>" },
    { "url": "<FOCA_ENSAR_MAPS_URL>" } ],
  "maxReviews": 10, "reviewsSort": "newest", "language": "tr" }
```

## 3) TripAdvisor yorumları (kendi — URL DOĞRULANDI)
actor: `maxcopell/tripadvisor-reviews`
```json
{ "startUrls": [{ "url": "https://www.tripadvisor.com.tr/Hotel_Review-g10920533-d4298328-Reviews-Kozbeyli_KonagI-Kozbeyli_Foca_Izmir_Province_Turkish_Aegean_Coast.html" }],
  "maxItemsPerQuery": 20, "reviewsLanguages": ["tr","all"] }
```

## 4) Booking rakip fiyat (Foça)
actor: `santamaria-automations/booking-com-scraper`
```json
{ "destination": "Foca", "checkin": "2026-07-15", "checkout": "2026-07-18",
  "adults": 2, "rooms": 1, "currency": "TRY", "maxResults": 15 }
```

## 5) Marka SERP sıralama ("kozbeyli")
actor: `scraperlink/google-search-results-serp-scraper` (en ucuz, $0.0005/SERP)
```json
{ "keyword": "kozbeyli konağı", "country": "tr", "hl": "tr" }
```
(Ayrıca: "foça butik otel", "kozbeyli konaklama" — kendi sıranı + OTA hâkimiyetini izle.)

## 6) Genel web okuma (ajan) — DOĞRULANDI
dedicated tool: `apify--rag-web-browser`
```json
{ "query": "Kozbeyli Konağı Foça otel yorum", "maxResults": 3, "outputFormats": ["markdown"] }
```

## Maliyet kontrolü
call-actor `callOptions.maxItems` (pay-per-result) veya `maxTotalChargeUsd` (pay-per-event) ile
tavan koy. Önce maxItems=5 test → sonra artır. Sonuçları `get-dataset-items` ile çek.
