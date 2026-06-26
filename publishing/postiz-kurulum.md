# Postiz Kurulum + Kanal Bağlama

## Seçenek A — Cowork Postiz eklentisi (en hızlı)
Cowork'te Postiz eklentisi kurulu (`postiz` skill). Postiz hesabınla kanalları bağla,
sonra içerik takvimini (kads publish) Postiz'e aktar/zamanla.

## Seçenek B — Self-host (ücretsiz, Docker)
```bash
# Basit docker (detay: github.com/gitroomhq/postiz-app, postiz.com/docs)
# Railway/Docker compose ile tek tık deploy seçenekleri de var (railway.com/deploy/postiz).
```
- Kur, hesap aç, Settings > Channels'tan ekle: **Instagram, Facebook Page, TikTok, LinkedIn, X**.
  (Her kanal kendi OAuth'u ile bağlanır; token Postiz'de kalır, sohbete/koda yazma.)

## İçerik takvimini yükleme
- `kads publish --out content/takvim` → `postiz-takvim.csv`.
- Postiz'de elle gönderi oluştur + zamanla, **veya** otomasyon:
  - **n8n/Make:** CSV satırlarını oku → Postiz node/REST API ile zamanla.
  - **REST API / @postiz/node:** her satırı `POST /posts` benzeri uçla zamanla (Postiz API docs).

## Kanal notları (otel)
- **Instagram/TikTok:** 9:16 Reels/video (creatives 01) — en yüksek erişim.
- **Facebook:** 4:5 Feed + link.
- **X:** kısa metin + kozbeylikonagi.com linki.
- **LinkedIn:** kurumsal/etkinlik açısı (taş konak, 200 kişilik organizasyon) — düşük frekans.
- **Google İşletme:** haftalık Post (profiles/google-isletme-profili.md).

## Güvenlik
Postiz token'ları Postiz'de/`.env`'de; URL'ye/sohbete yazma (docs/04). Self-host'ta erişimi kısıtla.
