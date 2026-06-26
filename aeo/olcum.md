# AEO Ölçüm Planı

## GA4 — AI yönlendirme (özel kanal grubu)
Admin > Data Display > Channel Groups > yeni kanal; **Referral'ın ÜSTÜNE** taşı. Source matches regex:
```
chatgpt\.com|chat\.openai\.com|perplexity\.ai|claude\.ai|gemini\.google\.com|copilot\.microsoft\.com|deepseek\.com|grok\.com
```
(GA4 yerel "AI Assistant" kanalı Perplexity'yi kapsamıyor + geriye dönük değil → özel kanal şart. Regex çeyrekte bir güncelle.)

## Sunucu log / Cloudflare
AI botları (GPTBot, OAI-SearchBot, ClaudeBot, Claude-SearchBot, PerplexityBot) GA4'te GÖRÜNMEZ
(JS çalıştırmaz). Sunucu logu / Cloudflare AI Audit ile tarama sıklığını izle. **WAF'ın bu botlara
429/403 dönmediğini düzenli kontrol et** (en sık "görünmezlik" sebebi).

## GSC
AI Overviews/AI Mode trafiği "Web" tipine dahil. Performance + Enhancements (yapısal veri) raporu izle.

## Haftalık alıntı testi
`alinti-testi.csv` — 10 sorgu × ChatGPT/Perplexity/Gemini/Claude → Kozbeyli alıntılanıyor mu?
