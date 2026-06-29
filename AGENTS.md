# AGENTS.md — Bu repoda çalışan AI agent'lar için

Bu repo, **Kozbeyli Konağı** (Foça/İzmir butik taş otel) reklam + dijital varlık
operasyonlarını yönetir. Otonom çalışabilirsin ama **para harcayan her işlem kod
seviyesinde guardrail + açık onaydan geçer.** Aşağıdaki kurallar bağlayıcıdır.

## Altın kurallar
1. **Önce ölçüm, sonra trafik.** Tracking test rezervasyonuyla doğrulanmadan hiçbir
   kampanya ENABLE edilmez (`docs/03`).
2. **Yazma varsayılan KAPALI.** Gerçek mutation yalnızca `config/ads-assets.yaml` →
   `write_guardrails.enabled: true` VE `.env` → `ADS_WRITES_ENABLED=true` ise mümkün.
3. **Her mutation `scripts/guardrails.py` / `kads guard`'dan geçer:** allowlist + PAUSED +
   bütçe tavanı + açık onay + ENABLE için ikinci onay + audit log (`logs/`).
4. **Sır yazma.** Token/secret/refresh/OAuth içeriğini sohbete, GitHub'a veya URL'ye
   ASLA yazma. Secret'lar yalnız `.env` (git-ignored). (`docs/04`)
5. **Türkçe yaz.** Cümle başı tire yerine nokta; cümle içi tire yerine virgül.
6. **Tahmin ≠ garanti.** CPC/CTR/CVR/ROAS sayıları planlamadır. Markalı arama #1
   ulaşılabilir; jenerik organik #1 garanti edilemez.

## Sistem haritası
- **CLI:** `kads` (girişi `kads/cli.py:main`). Komutlar: `doctor · config · plan · budget ·
  kpi · keywords · creative · build · seo · presence · validate · guard · monitor · brief`.
- **Tek kaynak:** `kads/data.py` (otel, plan, bütçe, kelime, RSA, Meta kopya).
- **Platformlar:** `kads/platforms/google.py` (Editor CSV), `meta.py` (kurulum rehberi),
  `kads/seo.py` (JSON-LD + GBP), `kads/presence.py` (dijital denetim).
- **Üretilmiş varlıklar:** `campaigns/` (launch-hazır), `dashboard/kontrol-merkezi.html`.
- **Skills:** `.agents/skills/kozbeyli-ads-monitor` (salt okunur), `.agents/skills/kozbeyli-ads-change`
  (guardrail'li değişiklik).
- **Bağlantılar:** Meta resmî connector `https://mcp.facebook.com/ads`; Google okuma
  `googleads/google-ads-mcp`; Google yazma = Editor CSV (güvenli) veya deneysel MCP.

## Tipik akış
1. `kads doctor` → eksikleri gör. 2. `.env` + `config` doldur (kimlikler, GTM).
3. Tracking doğrula (test rezervasyonu). 4. `kads build all` → import-hazır dosyalar.
5. Google: Editor import (PAUSED). Meta: kurulum rehberi. 6. Değişiklik → `kads guard`.
7. `kads presence` → dijital düzeltmeleri uygula (önce 4 Kritik).

## Bunu yapma
- Otomatik ENABLE, bütçe tavanı aşımı, delete/ödeme/kullanıcı yönetimi/liste yükleme.
- Üçüncü taraf MCP'ye reklam verisi akıtmak (resmî connector varken).
- Token'ı URL query'ye koymak.

## Bağlantı gerçekleri & caveat'lar (docs/10)
- Meta resmî connector `mcp.facebook.com/ads`: 29 araç, yeni nesneler PAUSED. **Claude Code
  OAuth bug'ı** → **Claude.ai web connector** kullan (Claude Code değil). `@meta/ads-cli`
  nesneleri **VARSAYILAN ACTIVE** oluşturur → `--status PAUSED` ŞART. ~200 çağrı/saat.
- Google resmî MCP salt okuma; yazma = Editor CSV (`kads build google`) veya deneysel MCP (`validate_only`).
- Token'ı asla `.mcp.json`/URL'ye koyma (OX Security STDIO advisory). Topluluk skill'leri **fork+audit**.
- Ek araçlar: docs/11 (Meta analiz skill'leri, Palmier video, Codex plugin). Web güvenlik / Shannon:
  docs/12 — yalnız **sahibi olduğun sistemde, staging'de, yetkiyle**; canlı prod'a otonom exploit YOK.

