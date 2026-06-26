# aeo/ — AEO & GEO uygulama paketi (kozbeylikonagi.com)

AI motorlarında (ChatGPT/Perplexity/Gemini/Google AI Overviews) görünürlük + alıntı. Denetim:
site **SSR, robots.txt + 57 URL sitemap + llms.txt var**; **en kritik eksik: hiçbir sayfada
JSON-LD yok**. Bu paket onu drop-in koda çevirir.

**Dürüst çerçeve:** Hiçbir AEO/GEO işi alıntı/sıralama GARANTİ etmez; olasılığı artırır. Şema
sayfadaki görünür içerikle eşleşmeli. **Sahte yorum/puan/ödül/fiyat YOK.** Temel SEO
(indekslenebilirlik, iç bağlantı, varlık güveni, ölçüm) zorunlu kalır.

## İçerik
- `schema/` — Hotel, HotelRoom, Restaurant, FAQPage, Breadcrumb (.jsonld) + `HotelSchema.tsx` (@graph, Next.js).
- `robots.txt` — AI botlarını açıkça davet eden sürüm (OAI-SearchBot/PerplexityBot Allow).
- `llms.txt` — doğrulanmış gerçeklerle refine (16 oda, 7/24 değil, havuz yok, ~82 km).
- `hreflang-nextjs.md` · `soru-kumeleri.md` · `icerik-mimarisi.md` · `olcum.md` · `7-30-gun-plan.md`
- `alinti-testi.csv` — haftalık AI alıntı testi takip şablonu.

## Öncelik (en yüksek getiri → düşük)
1. JSON-LD şema katmanı (5 şablon, Rich Results Test'ten geçmeli).
2. hreflang/alternates (TR↔EN, self-referencing).
3. Yanıt-öncelikli içerik + soru kümeleri (3 yeni sayfa).
4. GBP + NAP + sameAs (profiles/ ile birleşir).
5. Ölçüm (GA4 AI kanalı + sunucu log + alıntı testi).

Komut: `kads aeo` (soru kümeleri + şema kontrol listesi). Doğrula: Google Rich Results Test + Schema Markup Validator.
