# Yayına Alma Runbook'u — bugünden ilk canlı kampanyaya

Tek sayfa: ne, hangi sırayla, hangi dosya. Kural: **ölçüm doğrulanmadan ENABLE yok.**
Durum denetimi: `kads golive`. Eksik kimlikler: `kads doctor`.

## 0) Karar: kanonik domain
- Tek odak `www.kozbeylikonagi.com`. `.com.tr` kapsam dışı (sahip ayrı yönetiyor). Tüm reklam/SEO `.com`. Yanlış telefonu kaldır.

## 1) Hesap + bağlantı (Faz 1 — okuma)
- [ ] `.env` doldur: GA4, Ads, Pixel (bilinen) + Meta `act_...` + Google 10 hane + Dev Token + OAuth.
- [ ] Google read MCP: `.mcp.json` hazır → `/mcp` bağlı mı? (`docs/13`)
- [ ] Meta connector: **Claude.ai web**'de `mcp.facebook.com/ads` + OAuth (Claude Code DEĞİL).
- [ ] `kads doctor` → kritik eksik yok.

## 2) Ölçüm (Faz 2 — trafik yok)
- [ ] GTM container'ı seç (`docs/02`), `.env` + config'e yaz.
- [ ] Consent Mode v2 (`tracking/implementation/01`) <head>'e.
- [ ] GTM tag'leri kur (`tracking/implementation/02`): GA4, purchase, Ads conv (Enhanced), Pixel+Purchase.
- [ ] GA4 cross-domain + referral exclusion `hmshotel.net` (`tracking/implementation/03`).
- [ ] dataLayer olayları (`tracking/implementation/04`) — özellikle HMS onay `purchase`.
- [ ] Meta CAPI route (`tracking/implementation/05`) + `.env` token.
- [ ] HMS desteğine 6 soru (`fixes/05`). Onay sayfasına tag konabiliyor mu?
- [ ] **TEST REZERVASYONU** → GA4 DebugView + Meta Test Events'te aynı event_id ile tek Purchase.
- [ ] schema + güvenlik başlıkları + NAP (`fixes/02-04`).

## 3) Yazma (Faz 3 — ölçüm SONRASI)
- [ ] `config/ads-assets.yaml` write_guardrails.enabled: true + `.env` ADS_WRITES_ENABLED=true.
- [ ] Allowlist'i gerçek ID'lerle doldur.
- [ ] `kads build all` → Google Editor import (PAUSED) + Meta kurulum + SEO.
- [ ] Marka Search'ü guard ile yayına al: `kads guard --check change.json --approval "ONAYLA | ..."`.
- [ ] Meta Prospecting/WhatsApp (Purchase güvenilirse) — PAUSED → ENABLE (ikinci onay).
- [ ] Kreatifler: `creatives/` storyboard + şot listesi → çek/kurgula → 9:16 + 4:5.

## 4) Sürekli
- [ ] Haftalık: `kads report --metrics metrics.csv` + `kads rules` + `dashboard/rapor.html`.
- [ ] Doluluk-duyarlı harcama; sezon (Haz-Eyl koru / Kas-Mar kıs); negatif madenciliği.
- [ ] Retargeting (ay 2+, liste dolunca): `kads audiences`.
- [ ] Yorum toplama (`fixes/06`) — TripAdvisor + Google.
