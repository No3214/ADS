# publishing/ — Otomatik Sosyal Medya Yayını (Postiz)

Otelin kanalları: **Instagram · Facebook · TikTok · LinkedIn · X**. Hepsini tek yerden
zamanlamak için **Postiz** (açık kaynak, AGPL-3.0, **self-host ücretsiz**).

- Repo: https://github.com/gitroomhq/postiz-app (~30k★) · Site: https://postiz.com
- Kanallar: IG, FB, TikTok, X, LinkedIn (+ Page), Threads, YouTube, Pinterest, Google İşletme... (20+).
- API + n8n/Make/Zapier + NodeJS SDK (`@postiz/node`) + yerleşik AI ajan.
- Cowork: **Postiz eklentisi** zaten kurulu (skill: `postiz`). Self-host istersen `postiz-kurulum.md`.

## Akış (kreatif → takvim → yayın)
1. `kads calendar --out content/takvim` → 30 günlük çok kanallı takvim.
2. `kads publish --out content/takvim` → **postiz-takvim.csv** (date,time,channel,content,media,concept).
3. Postiz'de kanalları bağla (IG/FB/TikTok/LinkedIn/X) → CSV'yi içe al **veya** n8n/API ile otomatik zamanla.
4. Görseller: `creatives/` storyboard + şot listesi → çek/kurgula (Palmier/DaVinci/CapCut).

> Reklam (paid) ≠ organik yayın. Postiz organik sosyal yayını otomatikleştirir; reklam tarafı
> kads + Meta/Google connector ile guardrail'li yürür. İkisi farklı, birbirini besler.
