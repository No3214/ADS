# Apify İzleme Planı (kadans + bütçe + akış)

## Haftalık (Pazartesi, ~$0.05-0.20)
- Kendi Google + TripAdvisor yorumları (reçete 1,3, maxReviews=20) → yeni yorum + puan trendi
  → `competitors/izleme-sablonu.csv` ve yorum yanıtı (profiles/google + whatsapp/takip).
- Marka SERP (reçete 5: "kozbeyli konağı", "foça butik otel") → sıralama + OTA hâkimiyeti (docs/08).

## İki haftada bir
- Rakip Google yorumları (reçete 2) + Booking rakip fiyat (reçete 4) → parite + konumlanma
  → `competitors/rakipler.md` güncelle.

## Bütçe matematiği (free plan ~$5/ay)
- 20 yorum (Google) ≈ $0.012 · 20 yorum (TA) ≈ $0.10 · 3 SERP ≈ $0.0015 · 15 otel (Booking) ≈ $0.045.
- Haftalık tipik < $0.20 → aylık < $1. Free kredi fazlasıyla yeter. maxItems ile her zaman sınırla.

## Akış (dataset -> sistem)
1. call-actor → get-dataset-items (datasetId).
2. Yorum verisi → itibar takibi + yanıt (48 saat kuralı, fixes/06).
3. Fiyat verisi → `competitors/izleme-sablonu.csv`.
4. SERP verisi → `kads presence` / docs/08 sıralama notu.
5. Otomasyon: Apify Schedules (haftalık) veya n8n ile dataset → CSV/rapor.

## Güvenlik
Önce küçük test (maxItems=5). Token Apify'de. Free-tier'da kal; maxItems/maxResults zorunlu.
