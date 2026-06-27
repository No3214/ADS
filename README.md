# Kozbeyli Konağı — Reklam & Dijital Operasyon Sistemi

[![CI](https://github.com/No3214/ADS/actions/workflows/ci.yml/badge.svg)](https://github.com/No3214/ADS/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.8%2B-3f6b4f)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![deps](https://img.shields.io/badge/runtime%20deps-0-success)](pyproject.toml)

Foça'daki **Kozbeyli Konağı** butik taş otelinin Google + Meta reklamlarını **ve** tüm
dijital varlığını (site, Maps, Google İşletme, sosyal, OTA) tek yerden, **otonom ama kod
seviyesinde frenli** yönetmek için kurulan operasyon sistemi. Bütçe: **30.000 TL/ay**
(15.000 Google + 15.000 Meta).

> Başlangıç paketi (`README_TR.md`) bir **operasyon sistemine** dönüştürüldü: `kads` CLI +
> launch-hazır kampanyalar + yerel SEO/GBP + kanıt temelli dijital denetim + kontrol panosu.
> Tasarım, iki "god-tier" agent-CLI projesinin (Agent-Reach, OpenCLI) kanıtlanmış
> desenlerinden esinlenir (`docs/07`).

## ⚡ Hızlı başlangıç
```bash
pip install -e .          # 'kads' komutunu kurar (sıfır zorunlu bağımlılık)
kads doctor               # ortam + config + kanal teşhisi
kads presence             # tüm dijital varlığın denetimi + kritik düzeltmeler
kads build all            # Google + Meta + SEO dosyalarını üret (campaigns/)
kads plan                 # 30.000 TL çapraz kanal planı
```
`pip` istemiyorsan: `python3 -m kads <komut>` da çalışır.

## 🧭 Mimari
```
                       ┌──────────────  kads (CLI)  ──────────────┐
                       │ doctor · plan · budget · kpi · keywords  │
   kads/data.py  ───▶  │ creative · build · seo · presence        │  ──▶  table/json/yaml/md/csv
   (tek kaynak)        │ validate · guard · monitor · brief       │       sysexits çıkış kodları
                       └───┬───────────────┬──────────────┬───────┘
                           │               │              │
                  platforms/google   platforms/meta     seo + presence
                  (Editor CSV)       (kurulum rehberi)  (JSON-LD, GBP, denetim)
                           │               │              │
                  campaigns/google-editor  campaigns/meta  campaigns/seo · dashboard/
                           │               │
        Meta resmî connector (mcp.facebook.com/ads) · Google okuma MCP · guardrails.py
```

## 📦 Komut referansı
| Komut | Ne yapar |
|---|---|
| `kads doctor` | Ortam, config, kimlik, ağ ve veri bütünlüğü teşhisi |
| `kads plan / budget / kpi` | Kanal planı, bütçe tavanları, blended ROAS + rezervasyon matematiği |
| `kads keywords` | Google anahtar kelime + negatif setleri |
| `kads creative google\|meta` | RSA varlıkları / Meta reklam metinleri |
| `kads build google\|meta\|seo\|all` | Import-hazır dosyalar üretir (`--out DIR`) |
| `kads seo schema\|gbp\|local\|brand` | Hotel JSON-LD, GBP listesi, NAP atıfları, marka hâkimiyeti |
| `kads presence [fixes\|props]` | Dijital varlık denetimi + önceliklendirilmiş düzeltmeler |
| `kads validate` | RSA uzunluk + bütçe + CSV bütünlük doğrulaması |
| `kads mcp / skills` | Bağlantı durumu · Meta reklam skill paketi |
| `kads audiences` | Retargeting / Lookalike kitleleri |
| `kads rules / report [--metrics f.csv]` | Optimizasyon kuralları · blended KPI raporu |
| `kads competitors` | Rakip izleme listesi |
| `kads calendar / publish` | Çok kanallı içerik takvimi · Postiz-hazır yayın (oto publisher) |
| `kads setup / status` | Kurulum asistanı · sistem özeti |
| `kads apify` | Web veri actor reçeteleri (yorum/fiyat/SERP) |
| `kads aeo [schema]` | AI motoru görünürlüğü: soru kümeleri + JSON-LD |
| `kads season [detail] / funnel / offers` | Sezon planı (+detay) · dönüşüm hunisi · teklif/paketler |
| `kads web` | Frontend kontrol listesi (perf / a11y / PWA / meta) |
| `kads b2b [packages]` | Kurumsal motor (Aliağa sanayi): hedef + MICE paket |
| `kads pmax [specs|setup]` | Performance Max: asset group + varlık + kurulum |
| `kads demandgen [audiences]` | Demand Gen: format + kitle + varlık |
| `kads remarketing [rlsa|flow]` | Google remarketing + RLSA + kanal akışı |
| `kads utm [build|rules]` | UTM standardı + tutarlı link üretici |
| `kads attribution` | Attribution modeli + çift sayım dedup |
| `kads allocate [funnel|rules]` | Bütçe dağıtım matrisi (kanal × huni × ay) |
| `kads conversions [offline|enhanced|calls]` | Dönüşüm ölçüm döngüsü (online + offline/call import) |
| `kads events` | Yerel talep etkinlikleri (Foça festival vb.) + zamanlama |
| `kads tracking` | **Ölçüm durumu**: GTM/GA4/Ads/Pixel canlı mı + açık kalemler |
| `kads selfcheck` | Sistem bütünlük denetimi (kırılmaz) |
| `kads golive` | Fazlı yayına alma kapısı (hazırlık denetimi) |
| `kads guard --check change.json` | Değişiklik guardrail kontrolü (yazma için) |
| `kads monitor / brief` | Salt-okunur izleme yolu / haftalık brief şablonu |

Her komut `--format table\|json\|yaml\|md\|csv` destekler. Çıkış kodları Unix `sysexits.h`.

## 🗂️ Klasör yapısı
```
kads/                  CLI paketi (core, data, cli, platforms/, seo, presence)
campaigns/             Launch-hazır: google-editor/ (CSV), meta/ (rehber), seo/ (JSON-LD)
dashboard/             kontrol-merkezi.html + rapor.html (KPI/ROAS, offline)
docs/                  00-04 mimari/güvenlik · 05 optimizasyon · 06 benchmark
                       07 repo araştırması · 08 yerel SEO/GBP · 09 dijital denetim
                       10 referans kütüphanesi · 11 araç zinciri · 12 web güvenlik/Shannon
                       13 kurulum runbook (GitHub/MCP/connector/skill)
                       14-19 büyüme/AEO/web/B2B · 20-21 platform+canlı veri analizi
                       22 bütçe-dostu reklam/AEO · 23 Meta Pixel denetimi · 24 GTM etiket kurulumu
scripts/               guardrails.py (güvenlik kalbi) · preflight.py
assets/ tracking/ plans/ config/   RSA/kreatif · Consent+GTM+HMS · 30k plan · doğrulanmış config
tests/                 pytest (guardrails + build + CLI)
.claude/skills/        monitor (salt okunur) + change (guardrail'li)
```

## 🔒 Güvenlik modeli (üç katman)
1. **Prompt:** skill talimatları. 2. **Kod:** `scripts/guardrails.py` (allowlist + PAUSED +
bütçe tavanı + açık onay + ENABLE için ikinci onay + audit log). 3. **Connector izni:**
raporlama=Always allow, oluşturma/bütçe/pause=Needs approval, silme/ödeme=Blocked.
Yeni kampanyalar PAUSED. Yazma varsayılan KAPALI. Token/secret asla sohbete/GitHub'a/URL'ye.

## 🔎 Dijital varlık denetimi (en kritik bulgular — `docs/09`)
- **Tek odak: `www.kozbeylikonagi.com`** (gerçek Next.js sitesi). `.com.tr` kapsam dışı — sahip ayrı yönetiyor; sistem gündemine alma.
  ve **YANLIŞ telefon** (0232 218 2109) gösteriyor. Öneri: **`.com` canonical, diğerleri 301**.
- `.com` = gerçek Next.js sitesi (JSON-LD VAR). Tüm reklam/SEO/tracking `.com`.
- Marka SERP'i **OTA-dominant**; Google İşletme sahiplik + NAP standardı şart.
- HMS rezervasyonu ayrı domain → **cross-domain ölçüm** kurulmalı.
Tam liste + öncelik: `kads presence fixes`.

## 🎯 "Google'da kozbeyli yazınca öne çık" (dürüst çerçeve)
**Markalı** "Kozbeyli Konağı" aramasında ilk sıra çok ulaşılabilir: site `<title>`/H1 +
JSON-LD şema + eksiksiz Google İşletme + Marka Search kampanyası SERP'i kaplar. **Jenerik
organik #1'i hiç kimse garanti edemez** ("kozbeyli" köy adıdır, bilgi niyeti baskın); orada
hedef GBP + Maps + içerik + paid savunmayla görünür olmaktır. Detay: `docs/08`, `kads seo`.

## 🧩 Eksikler (siz dolduracaksınız)
Meta `act_...` · Google 10 haneli müşteri ID · doğru GTM container · Google Developer
Token + OAuth · HMS otel slug'ı + onay sayfası davranışı · canonical domain kararı.
`kads doctor` hepsini listeler.

## ⚠️ Sorumluluk reddi
Tüm CPC/CTR/CVR/CPA/ROAS ve rezervasyon sayıları **planlama tahminidir, garanti değildir**.
Gerçek maliyetler teklif, kalite, sezon, konum ve rekabete göre değişir.

## 🙏 Esinlenme
Agent-Reach (channels, doctor, safe/dry-run, SKILL kaydı) · OpenCLI (birleşik yüzey,
`--format`, sysexits, hub). Detay ve neyi bilinçli almadığımız: `docs/07`.

— Üretim: `kads v1.0` · MIT · Kurulum detayları için ayrıca `README_TR.md`.
