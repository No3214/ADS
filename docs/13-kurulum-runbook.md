# 13 — Kurulum Runbook (GitHub · Google MCP · Meta connector · Skill'ler)

Senin makinende çalıştırılacak adımlar. Sıra: GitHub → Google okuma MCP → Meta connector →
skill'ler. Her şey hazır; bu, "canlıya bağlama" tarafı.

## 1) GitHub (No3214/ADS)
```bat
:: Klasörde push.bat'a çift tıkla — veya:
push.bat
```
- `push.bat` gh varsa repoyu **private** oluşturur + push eder; yoksa önce
  https://github.com/new ile `ADS` reposu oluştur, sonra push.bat manuel push yapar.
- gh kur: https://cli.github.com → `gh auth login` (tarayıcı). Token'ı sohbete yazma.

## 2) Google Ads okuma MCP (resmî, salt okuma)
`.mcp.json` hazır (`google-ads-readonly`). Gerekenler (`.env`'e):
```
GOOGLE_PROJECT_ID=...
GOOGLE_ADS_DEVELOPER_TOKEN=...        # en az Explorer erişimi
GOOGLE_ADS_MCP_OAUTH_CLIENT_ID=...
GOOGLE_ADS_MCP_OAUTH_CLIENT_SECRET=...
GOOGLE_ADS_CUSTOMER_ID=XXX-XXX-XXXX   # 10 hane
```
- pipx kur (`pip install pipx`). Claude Code: `claude` → `/mcp` ile `google-ads-readonly` bağlı mı bak.
- Test: "son 7 günü önceki 7 günle karşılaştır" → `/kozbeyli-ads-monitor`. Yazma YOK (salt okuma).
- Durum: `kads mcp`.

## 3) Meta Ads connector (Claude.ai web — OAuth bug'dan kaçın)
- **Claude.ai web** > Settings > Connectors > Add custom connector >
  URL: `https://mcp.facebook.com/ads` > Facebook ile OAuth.
- **Claude Code'a EKLEME** (localhost callback OAuth bug'ı var). Terminalde `@meta/ads-cli`
  kullanırsan nesneler **VARSAYILAN ACTIVE** olur → her zaman `--status PAUSED` ver.
- İzinler (Claude arayüzü): raporlama=Always allow, oluşturma/bütçe/pause=Needs approval,
  silme/ödeme=Blocked. Yeni nesneler PAUSED.
- Token kapsamı: önce yalnız okuma; ölçüm doğrulanınca (docs/01) yazmayı kademeli aç.

## 4) Meta reklam skill'leri (analiz/read)
```bash
scripts/install-skills.sh        # mac/linux   (Windows: scripts\install-skills.bat)
export META_ACCESS_TOKEN=...     # Meta Ad Library API; sohbete/URL'ye YAZMA
```
- Skill'ler: `/spy`, `/competitive-ads-extractor`, `/bulk-creative`, `/ads meta`, `/ads-score`.
- Liste/özet: `kads skills`. Detay/zincir: docs/11. Topluluk → fork+audit (docs/04).

## Sonra: günlük/haftalık akış
1. `kads doctor` (hazırlık) → `.env` eksiklerini kapat.
2. Ölçümü doğrula (test rezervasyonu, docs/01) — yazmadan ÖNCE.
3. `kads build all` → Google Editor import (PAUSED) + Meta kurulum + SEO.
4. Haftalık: `kads report --metrics metrics.csv` (KPI + öneri) · `kads rules` · `dashboard/rapor.html`.
5. Değişiklik: `kads guard --check change.json --approval "ONAYLA | ..."` → uygula → doğrula.

> Yazma kapısı: `config/ads-assets.yaml` write_guardrails.enabled + `.env` ADS_WRITES_ENABLED.
> Ölçüm doğrulanmadan açma.
