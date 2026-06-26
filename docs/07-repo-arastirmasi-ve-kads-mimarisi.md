# 07 — Repo Araştırması ve `kads` Mimarisi

"Tüm web'i ve repoları araştır, işimize yararsa kullan, benzerlerini araştır, en iyi
işi çıkar" isteğinin çıktısı. İncelenen iki referans repo + benzerleri, ve bunların
`kads` CLI tasarımına nasıl yansıdığı. (Reklam connector repoları için ayrıca docs/00.)

## İncelenen referanslar

### 1) Panniantong/Agent-Reach (~20k★, Python)
"AI agent'a internet gözü tak" — tek CLI + **takılabilir kanal (channel)** mimarisi
(web, Twitter, Reddit, YouTube, GitHub…). Öne çıkan desenler:
- **`doctor`** tek komutla "hangi kanal çalışıyor/çalışmıyor, nasıl düzeltilir".
- **Takılabilir kanal:** her platform bağımsız bir dosya; beğenmezsen değiştir (scaffolding).
- **SKILL.md kaydı:** agent ihtiyacı görünce hangi aracı çağıracağını bilir.
- **`--safe` / `--dry-run`:** sistemi otomatik değiştirme; önce ne yapacağını göster.
- **Kimlik hijyeni:** cookie/token yalnızca yerelde, dosya izni 600, sızdırma yok.

### 2) jackwener/OpenCLI (~14k★, TypeScript)
"Her web sitesini/aracı CLI yap" — birleşik komut yüzeyi + AI-native runtime. Desenler:
- **Birleşik yüzey:** `opencli <hedef> <komut>` — tek tutarlı arayüz.
- **`--format` table|json|yaml|md|csv:** deterministik, pipe'lanabilir çıktı.
- **Unix `sysexits.h` çıkış kodları:** 0/2/66/69/77/78… CI ve shell ile doğal entegrasyon.
- **`doctor`:** kendi kendini teşhis/iyileştirme.
- **CLI Hub passthrough:** gh/docker gibi dış araçları aynı yüzeyden çağır.
- **Deterministik:** aynı komut → aynı şema, her sefer.

### Benzerleri (kısaca)
- Resmî **Meta Ads AI Connectors** (`mcp.facebook.com/ads`) ve **googleads/google-ads-mcp**
  (okuma) — reklam tarafının birinci-taraf yolu (docs/00).
- Topluluk MCP'leri (pipeboard, hashcott vb.) — esinlenme evet, production'da çalıştırma
  hayır; biri README'de gerçek secret sızdırmıştı (docs/04). Token'ı URL'ye koyma anti-deseni.

## `kads` neyi aldı (ve neyi bilinçli almadı)

| Desen | Kaynak | kads'te karşılığı |
|---|---|---|
| `doctor` kendi kendini teşhis | Agent-Reach + OpenCLI | `kads doctor` (ortam+config+kanal+ağ) |
| Takılabilir platform (channel) | Agent-Reach | `kads/platforms/{google,meta}.py` + `kads/seo.py` |
| `--format` çoklu çıktı | OpenCLI | her komutta table/json/yaml/md/csv (`kads.core.emit`) |
| `sysexits.h` çıkış kodları | OpenCLI | `kads.core.EX_*` (0/2/66/69/77/78) |
| `--safe` / dry-run varsayılan | Agent-Reach | yazma varsayılan KAPALI; her mutation guardrail'li |
| SKILL kaydı (agent bilir) | Agent-Reach | `.claude/skills/` (monitor + change) + AGENTS.md |
| Birleşik komut yüzeyi | OpenCLI | tek `kads` girişi, alt komutlar |
| Deterministik şema | OpenCLI | tek kaynak `kads/data.py` → tekrarlanabilir CSV |
| Dış araç passthrough | OpenCLI Hub | `kads guard` → `scripts/guardrails.py` sarmalar |
| Kimlik hijyeni | Agent-Reach + docs/04 | secret yalnız `.env`, config'te maskeleme, URL'de token yok |

**Bilinçli ALMADIKLARIMIZ (neden):**
- **Reklam platformlarını scrape etme yok.** Reklam verisi birinci-taraf kalır (resmî
  connector / okuma MCP). Üçüncü taraf veri akışına bağımlılık yok (docs/04).
- **Otomatik sistem değişikliği yok.** Para harcayan işlemler her zaman guardrail + açık
  onay arkasında (prompt değil, kod seviyesinde).
- **Cookie/oturum yeniden kullanımı (OpenCLI tarayıcı modu) yok.** Reklam hesabı için
  OAuth tabanlı resmî yol tercih edilir; ban/askıya alma riski düşer.

## Sonuç: `kads` ne oldu
Başlangıç paketinin (guardrails + tracking + plan + assets) üzerine, iki "god-tier"
agent-CLI'nin kanıtlanmış desenlerini giydiren **birleşik reklam operasyon yüzeyi**:
`doctor · config · plan · budget · kpi · keywords · creative · build · seo · validate ·
guard · monitor · brief`. Hepsi deterministik, `--format`'lı, sysexits çıkış kodlu,
guardrail-güvenli ve Türkçe. Kurulum: `pip install -e .` → `kads`.
