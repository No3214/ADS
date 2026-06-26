# Değişiklik Günlüğü

## [1.0.0] — 2026-06-26
İlk "god-tier" sürüm. Başlangıç paketi (guardrails + tracking + plan + assets) bir
operasyon sistemine dönüştürüldü.

### Eklendi
- **`kads` CLI** (Python, sıfır bağımlılık): `doctor · config · plan · budget · kpi ·
  keywords · creative · build · seo · presence · validate · guard · monitor · brief ·
  help · version`. Her komut `--format table|json|yaml|md|csv`, Unix sysexits çıkış kodları.
- **Takılabilir platformlar:** `kads/platforms/google.py` (Google Ads Editor import CSV
  üretimi), `kads/platforms/meta.py` (Ads Manager kurulum rehberi + reklam metni).
- **Tek kaynak:** `kads/data.py` — otel gerçekleri, plan, bütçe, anahtar kelimeler,
  negatifler, RSA, Meta kopya (web ile doğrulandı, Haziran 2026).
- **Launch-hazır kampanyalar:** `campaigns/` — 3 Google kampanyası (PAUSED), 51 kelime,
  57 negatif, 2 RSA seti, uzantılar; Meta 5 konsept + kurulum rehberi.
- **Yerel SEO + GBP:** `kads/seo.py` — geçerli `Hotel` JSON-LD şeması, GBP kontrol listesi,
  NAP atıf listesi, markalı arama hâkimiyeti. `docs/08`.
- **Dijital varlık denetimi:** `kads/presence.py` + `docs/09` — 3 domain + sosyal + OTA +
  Maps kanıt temelli denetim; 14 maddelik önceliklendirilmiş düzeltme listesi.
- **Kontrol merkezi panosu:** `dashboard/kontrol-merkezi.html` (bağımsız, offline).
- **Araştırma dokümanları:** `docs/05` optimizasyon playbook, `docs/06` Türkiye otel
  benchmark + rekabet, `docs/07` repo araştırması (Agent-Reach + OpenCLI) ve kads mimarisi.
- **Repo altyapısı:** `pyproject.toml` (pip install -e . → `kads`), `tests/` (pytest),
  `Makefile`, GitHub Actions CI, `AGENTS.md`, `LICENSE` (MIT).

### Korundu
- `scripts/guardrails.py` kod seviyesinde güvenlik kalbi; `kads guard` bunu sarmalar.
- `.claude/skills/` monitor (salt okunur) + change (guardrail) skill'leri.
- `tracking/` Consent Mode v2 + GTM + HMS snippet; `docs/00–04` mimari/güvenlik.

### Notlar
- Tüm metrik tahminleri planlamadır, garanti değildir.
- Yazma varsayılan KAPALI; ölçüm doğrulanmadan ENABLE yok.

## [1.1.0] — 2026-06-26
### Eklendi
- **docs/10 — Vetted referans kütüphanesi:** Claude Code'a verilebilecek, official vs community
  işaretli kaynaklar (MCP/Claude Code, Meta, Google, ölçüm, strateji, güvenlik) + HMS durum +
  fazlı rollout + caveat'lar.
- **docs/11 — Araç zinciri:** 5 Meta reklam Claude skill'i (`/spy`, `/competitive-ads-extractor`,
  `/bulk-creative`, `/ads meta`, `/ads-score` — AgriciDaniel/claude-ads vb.); **Palmier Pro**
  ücretsiz açık kaynak AI video editörü (MCP'li; macOS + Windows portu + alternatifler);
  Codex plugin (geliştirme).
- **docs/12 — Web güvenliği + Shannon:** KeygraphHQ/shannon (otonom AI pentester) yetkili/staging
  kullanımı + pasif güvenlik hijyeni (http parazit domain, güvenlik başlıkları, bağımlılık).
### Değişti
- docs/04 + AGENTS.md: Meta `@meta/ads-cli` VARSAYILAN ACTIVE uyarısı + Claude Code OAuth bug
  (Claude.ai web connector) + OX Security STDIO advisory.

## [1.2.0] — 2026-06-26
### Eklendi
- **Yeni kads komutları:** `mcp` (bağlantı durumu), `skills` (Meta reklam skill paketi),
  `audiences` (retargeting/lookalike), `rules` (bütçe/teklif optimizasyon önerileri),
  `report` (blended KPI + metrik şablonu).
- **Kampanya şablonları:** Google Display (PAUSED remarketing) + Meta yerleşim şablonları
  (Feed 4:5 / Stories 9:16 / Reels 9:16). `campaigns/google-editor/09-10`, `campaigns/meta/*`.
- **A/B yapıları:** her Google reklam grubunda 3 RSA varyantı (A-Miras/B-Manzara/C-Direkt);
  her Meta konseptinde 3 reklam varyantı (A-Hikaye/B-Fayda/C-Aciliyet).
- **Retargeting kitleleri:** site 30/60g, oda/rezervasyon görüntüleyen, begin_checkout terk,
  IG/FB etkileşim, video %50+, LLA %1-3 (`campaigns/meta/meta-retargeting-kitleleri.csv`).
- **Optimizasyon kuralları:** `kads/rules.py` (10 deterministik kural) — ROAS scale/cut, CPA,
  CTR, frekans, CPC, öğrenme, teklif geçişi, pacing. Otomatik UYGULAMAZ; guardrail'den geçer.
- **Raporlama:** `kads/report.py` + `dashboard/rapor.html` (metrik yapıştır → blended ROAS/CPA/
  CTR/CPC + otomatik öneriler, offline).
- **Entegrasyon:** gerçek `.mcp.json` (Google read-only + Meta connector); gh-aware `push.bat`;
  `scripts/install-skills.sh/.bat`; `docs/13` kurulum runbook.
### Test
- 35 pytest (was 23): data_ext, display, A/B, yerleşim, kitle, rules, report dahil.

## [1.3.0] — 2026-06-26
### Eklendi
- **fixes/ — denetim düzeltme paketi (docs/09 → kopyala-yapıştır):** domain birleştirme 301
  (Vercel/Netlify/Apache/Nginx), güvenlik başlıkları (next.config + Apache/Nginx, CSP Report-Only),
  schema.org JSON-LD gömme (Next.js JsonLd.jsx), tek NAP standardı, HMS cross-domain destek
  e-postası (6 soru), TR yorum toplama şablonları, hreflang TR/EN.
- **content/ — SEO içerik brief'leri:** Kozbeyli köyü rehberi, Foça gezi rehberi, köy kahvaltısı
  (markalı + yerel "kozbeyli" sıralaması için).
- **`kads golive`** — fazlı yayına alma kapısı: Okuma / Ölçüm / Yazma fazları, env'den otomatik
  hazırlık denetimi + manuel kapılar.
### Test
- 37 pytest (golive dahil).

## [1.4.0] — 2026-06-26
### Eklendi
- **tracking/implementation/ — ölçüm implementasyon paketi** (.com + hmshotel.net): Consent Mode v2
  (KVKK-güvenli, denied default), GTM tag spesifikasyonu (GA4/purchase/Ads Enhanced/Pixel),
  GA4 cross-domain + referral exclusion, dataLayer olay şeması, **Meta CAPI route (Next.js, event_id dedup)**.
- **creatives/ — görsel kreatif paketi:** Reels/Stories 9:16 + Feed 4:5 şot listeleri, TR altyazı
  script'leri, **storyboard.html** (5 konsept görsel brief).
- **golive/YAYINA-ALMA.md** — bugünden ilk canlı kampanyaya faz faz runbook.
### Notlar
- Kod değişikliği yok; 37 pytest geçmeye devam ediyor. Secret yok (CAPI token .env'de).

## [1.5.0] — 2026-06-26
### Eklendi
- **profiles/ — platform profil içerik kiti (paste-hazır, NAP-tutarlı):** Google İşletme tam
  içeriği (açıklama ~750ch, kategoriler, öznitelikler, hizmet/ürün, haftalık postlar, Q&A seed,
  yorum yanıtı), OTA profil metinleri TR+EN (Booking/trivago/TripAdvisor/neredekal/obilet +
  platform bazında düzeltme), sosyal bio (IG/FB), master eşitleme kontrol listesi.
- Denetim bulguları #4/#7/#8'i (NAP tutarsızlığı, OTA-dominant marka SERP, TripAdvisor düşük) çözer.

## [1.6.0] — 2026-06-26
### Eklendi
- **competitors/ + `kads competitors`:** Foça butik rakip izleme (Bülbül Yuvası/Huri Nuri/Foça Ensar
  + OTA), karşı-mesaj, izleme şablonu CSV, /spy + nimble araçları.
- **`kads calendar` + content/takvim/:** 30 günlük çok kanallı içerik takvimi (IG/FB/TikTok/LinkedIn/X +
  Google İşletme), 5 konsept + pik saatler (~69 post).
- **Otomatik publisher — `kads publish` + publishing/:** Postiz entegrasyonu (açık kaynak, self-host
  ücretsiz; IG/FB/TikTok/LinkedIn/X + 20 kanal; API/n8n). Takvimi Postiz-hazır CSV'ye çevirir.
- **`kads setup`:** .env + .mcp.json'u örnekten oluşturur, doldurulacakları listeler.
### Test
- 44 pytest (calendar/publish/competitors/setup dahil).

## [1.7.0] — 2026-06-26
### Eklendi
- **whatsapp/ — WhatsApp rezervasyon şablonları:** hızlı yanıt (müsaitlik/fiyat/oda/evcil/ulaşım/kapanış),
  SSS, takip mesajları (varış öncesi/çıkış/geri kazanım). Otelin ana rezervasyon kanalı.
- **BASLA.md** — kod bilmeden tek sayfa başlangıç rehberi (kur → doldur → ölç → üret → yayınla → optimize).
- **docs/14 — aylık/haftalık operasyon rutini** (günlük/haftalık/aylık/sezonluk/çeyreklik ritim).
- **`kads status`** — capstone sistem özeti: 12 paket durumu + kimlik hazırlığı + sonraki adım.
### Test
- 45 pytest (status dahil). Toplam 25 kads komutu.

## [1.8.0] — 2026-06-26
### Eklendi
- **Apify MCP entegrasyonu (doğrulandı + çalıştırıldı):** apify/ paketi — rag-web-browser test run
  (runId 8gcfVqcb...) ile canlı listeleme URL'leri keşfedildi. `kads apify` komutu + 6 actor reçetesi:
  Google Maps yorumları (compass), TripAdvisor yorumları (maxcopell, URL doğrulandı), Booking rakip
  fiyat (santamaria), marka SERP (scraperlink), RAG web browser. Hepsi free-tier (pay-per-event).
- apify/actor-recipes.md (call-actor JSON + maxItems maliyet kontrolü) + monitoring-plan.md (kadans + bütçe).
### Test
- 47 pytest (apify dahil). 26 kads komutu.

## [1.9.0] — 2026-06-26
### Eklendi
- **aeo/ — AEO/GEO uygulama paketi (AI motoru görünürlüğü):** denetimin en kritik bulgusu (sitede
  JSON-LD yok) drop-in koda çevrildi. `schema/` (Hotel/HotelRoom/Restaurant/FAQPage/Breadcrumb .jsonld
  + HotelSchema.tsx @graph), AI-bot dostu `robots.txt`, refine `llms.txt` (doğrulanmış gerçekler),
  `hreflang-nextjs.md`, soru kümeleri (A-H), içerik mimarisi, GA4 AI-kanal ölçümü, 7/30-gün plan,
  `alinti-testi.csv`. Doğrulanmış gerçekler: SSR site, ~82 km havalimanı, resort havuz yok, 7/24 değil.
- **`kads aeo` + `kads aeo schema`** — soru kümeleri + JSON-LD şema kontrol listesi.
### Not / Test
- 50 pytest (aeo dahil; JSON-LD geçerlilik + sahte-puan-yok kontrolü). 27 kads komutu.
- Dürüst çerçeve: AEO garanti vermez; sahte yorum/puan/ödül/fiyat YOK.

## [1.10.0] — 2026-06-26
### Eklendi
- **email/ — e-posta pazarlama:** 6 şablon (karşılama, varış öncesi, çıkış-yorum, sezonsal bülten,
  win-back, rezervasyon terki) + sıra/tetik akışı (KVKK izinli).
- **landing/ — açılış sayfası A/B yapıları:** 7 elementli varyant matrisi (hero/H1/CTA/sosyal kanıt/
  teklif/yol/form) + hipotez + yürütme planı (tek değişken, anlamlılık).
- **docs/15 sezon kampanya planı** (yüksek/düşük/geçiş) + **docs/16 dönüşüm hunisi** (5 aşama + tıkanma teşhisi).
- **`kads season` / `kads funnel` / `kads offers`** komutları (SEASONS/FUNNEL/OFFERS).
### Test
- 53 pytest. 30 kads komutu.

## [1.11.0] — 2026-06-26
### Eklendi
- **outreach/ — mikro-influencer & PR:** strateji (kriter/kademe/keşif), DM+e-posta şablonları,
  brief, barter, takip CSV, Apify keşif reçetesi. Butik otel için düşük maliyetli büyüme.
- **reputation/ — itibar & kriz:** yorum yanıt protokolü (severity bazlı, 48h, TripAdvisor 3/5
  düzeltme) + kriz iletişimi playbook (senaryolar, kanallar, toparlanma).
- **finance/ — Bütçe & Öngörü Excel modeli** (5 sayfa, formüllü, sıfır hata doğrulandı): bütçe
  dağılımı, ROAS senaryo (3x/4x→rezervasyon+başabaş), 12 ay tracker, sezon ağırlığı, funnel KPI.
### Test
- 53 pytest (kod değişmedi; xlsx LibreOffice recalc ile 0 hata). 30 kads komutu, 19 paket.

## [1.12.0] — 2026-06-26
### Eklendi
- **web/ — frontend uygulama paketi (kozbeylikonagi.com, Next.js 15 drop-in):**
  - performance/: next.config (AVIF/WebP + cache başlıkları), next/image lazy + priority,
    next/dynamic, next/font, web-vitals→GA4, bundle analiz + hedefler.
  - accessibility/: WCAG 2.1 AA kontrol listesi, skip link + erişilebilir form + focus snippet,
    reduced-motion CSS, renk kontrastı (4.5:1).
  - meta/: tam generateMetadata (OpenGraph/Twitter/canonical/hreflang) + dinamik opengraph-image.
  - pwa/: geçerli manifest.webmanifest + Serwist SW kurulumu + ikon notu.
  - responsive/: mobil kontrol listesi + viewport (zoom engelleme yok).
  - animations/: reduced-motion saygılı, transform/opacity-only zarif reveal (CSS + Framer Motion).
- **`kads web`** — frontend kontrol listesi. Hedef: Lighthouse ≥90/95, CWV Good.
### Test
- 55 pytest (web checklist + manifest JSON geçerlilik dahil). 31 kads komutu, 20 paket.

## [1.13.0] — 2026-06-26
### Eklendi
- **b2b/ — Kurumsal gelir motoru (Aliağa sanayi):** konum doğrulandı (Aliağa kalbine ~25–30 km).
  Hedef çapa firmalar (STAR Rafineri/SOCAR, Petkim, Tüpraş, İzmir Demir Çelik, Habaş, gemi söküm,
  Nemrut limanları, Aliağa OSB 72 firma), değer önerisi, kurumsal rate card, MICE paketleri,
  LinkedIn+e-posta outreach şablonları, hesap CSV (çapa firmalarla), prospecting reçeteleri.
  `kads b2b` / `kads b2b packages`.
- **`kads selfcheck`** — sistem bütünlük denetimi (RSA/bütçe/JSON-LD/manifest/üretim/20 paket/
  guardrails/yedek) → kırılmaz/kendini denetleyen. **docs/17** sağlamlık+otonomi modeli; **memory/learnings.md**.
### Test
- 60 pytest. 33 kads komutu, 21 paket. selfcheck PASS.
