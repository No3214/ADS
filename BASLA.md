# BAŞLA — Kozbeyli Konağı reklam & dijital sistem (kod bilmeden)

Bu repo otelin **reklamlarını, yerel SEO'sunu, sosyal yayınını ve dijital varlığını** tek
yerden yönetir. Aşağıdaki sırayı izle; her adımda hangi dosya/komut lazım yazıyor.

## 0) Kur (bir kez)
- Python varsa: klasörde `pip install -e .` → `kads` komutu hazır. (Yoksa `python -m kads ...`)
- `kads setup` → `.env` ve `.mcp.json` oluşur. `kads doctor` → eksikleri gösterir.

## 1) Kimlikleri doldur (`.env`)
Meta `act_...` · Google 10 hane müşteri ID · GTM container (docs/02) · Google Dev Token + OAuth.
`kads doctor` ve `kads golive` neyin eksik olduğunu söyler.

## 2) Ölç (reklamdan ÖNCE — en önemli adım)
`tracking/implementation/` + `golive/YAYINA-ALMA.md`: Consent v2, GTM tag'leri, GA4 cross-domain,
`kads godtier-audit` ile durum gör. Meta CAPI. HMS desteğine 6 soru (`fixes/05`). **Test rezervasyonu** ile doğrula.

## 3) Reklamları üret + yayına al (guardrail'li)
`kads build all` → Google Ads Editor CSV (PAUSED) + Meta kurulum + SEO. Editor'e import et.
Yayına alma: `kads guard` + açık onay. Plan: `kads plan` · bütçe: `kads budget`.

## 4) Dijitali düzelt
`kads presence fixes` (14 madde) → `fixes/` (domain birleştir, güvenlik, schema, NAP) +
`profiles/` (Google İşletme + OTA + sosyal metinleri yapıştır).

## 5) Sosyal yayını otomatikleştir
`kads calendar --out content/takvim` (30 günlük plan) → `kads publish` (Postiz-hazır CSV) →
Postiz'e kanalları (IG/FB/TikTok/LinkedIn/X) bağla (`publishing/`). Kreatif: `creatives/storyboard.html`.

## 6) İzle + optimize et (haftalık)
`kads report --metrics metrics.csv` (KPI) · `kads rules` (öneri) · `kads godtier-audit` (CAPI/OCT denetimi) · `kads inject-audiences` (CRM kitleleri) · `dashboard/rapor.html` ·
`kads competitors` (rakip) · yorum topla (`fixes/06` + `whatsapp/takip-mesajlari.md`).

## Yardım
`kads help` (43 komut) · `kads status` (sistem özeti) · docs/00-26 · README.md (teknik).
WhatsApp rezervasyon: `whatsapp/`. GitHub'a yükle: `push.bat`.
