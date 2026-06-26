# apify/ — Web veri toplama (Apify MCP) entegrasyonu

Apify MCP **doğrulandı ve çalışıyor** (free-tier). Test çalıştırması: `apify/rag-web-browser`
runId `8gcfVqcbEKpj8nw7y` → SUCCEEDED (21s); otelin canlı listelemeleri keşfedildi (TripAdvisor
`d4298328`, obilet, Hotels.com). Tüm seçilen actor'lar **pay-per-event** ve free-tier uyumlu
(free plan ~$5/ay kredi → binlerce sonuç).

## Ne işimize yarar (agentic workflow)
- **Yorum izleme** (kendi + rakip): Google Maps + TripAdvisor → itibar + TripAdvisor 3/5 düzeltme takibi.
- **Rakip fiyat** (Booking, Foça): fiyat paritesi + konumlanma.
- **Marka SERP sıralama** ("kozbeyli", "foça butik otel"): yerel/organik görünürlük takibi.
- **Ajan web okuma** (RAG browser): genel araştırma/doğrulama.

Bunlar `competitors/`, `profiles/` (yorum), ve docs/08 (SERP) ile birleşir. Komut: `kads apify`.

## MCP doğru kullanım akışı (Claude)
1. **search-actors** (keyword) → actor bul (free, kredi yakmaz).
2. **fetch-actor-details** (actor, output={inputSchema,pricing}) → girdi şeması + fiyat.
3. **call-actor** (actor, input, callOptions.maxItems) → çalıştır (maxItems ile sonucu sınırla = maliyet kontrolü).
4. **get-actor-run** / **get-dataset-items** (datasetId) → sonucu oku.
- Dedicated araç varsa (apify--rag-web-browser) onu kullan.

## Free-tier güvenlik
- Her zaman `maxReviews`/`maxResults`/`maxItems` ile sonucu sınırla (maliyet = sonuç sayısı × birim).
- Token Apify'de; sohbete/URL'ye yazma. Önce küçük test (maxItems=5), sonra ölçekle.
- Reçeteler: `actor-recipes.md`. Kadans + bütçe: `monitoring-plan.md`.
