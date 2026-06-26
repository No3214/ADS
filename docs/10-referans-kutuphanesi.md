# 10 — Vetted Referans Kütüphanesi (Claude Code · Google + Meta Ads)

Claude Code'a verilebilecek, kategorilere ayrılmış, **official vs community** işaretli kaynak
kütüphanesi. Her madde için kısa TR not + kaynak. (Kullanıcı tarafından sağlanan araştırma;
sistemin doğrulanmış gerçekleriyle örtüşür. Yıldız/sürüm Haziran 2026 anlık görüntüsüdür.)

## TL;DR
- En güvenli üretim yığını: **resmî, salt-okunur first-party MCP'ler** (Google
  `googleads/google-ads-mcp`; Meta `mcp.facebook.com/ads`) ile OKU; tüm YAZMA işlemleri
  dry-run / PAUSED / insan onayı arkasında. 30.000 TL/ay canlı hesapta otonom yazma erişimi VERME.
- Çapraz alan ölçümü (burada zorunlu — motor `hmshotel.net`): GA4 cross-domain + Consent Mode
  v2 (Advanced) + Enhanced Conversions + Meta CAPI (`event_id` dedup), `@next/third-parties` + GTM.
- **HMS Otel onay sayfası dönüşümü kamuya belgeli değil** → HMS desteğiyle netleştir.
  Kurulumun **en büyük açık riski** budur.

## Kilit bulgular
- İki resmî reklam MCP'si, zıt tasarımlı: **Google** (28 Nis 2026, açık kaynak, **salt okuma**;
  GAQL `search`, `list_accessible_customers`, `get_resource_metadata`). **Meta AI Connectors**
  (29 Nis 2026, **29 araç**, 5 kategori, okuma+yazma; yeni nesneler **PAUSED**) `mcp.facebook.com/ads`.
- **Meta MCP'de bilinen Claude Code OAuth bug'ı:** localhost callback URL'lerini kaydetmiyor →
  güvenilir yol **Claude.ai web connector**. CLI (`@meta/ads-cli`) terminal yolu ve nesneleri
  **VARSAYILAN ACTIVE** oluşturur — `--status PAUSED` şart. (kads guardrail'i bu yüzden kritik.)
- **MCP STDIO RCE** uyarı ailesi (OX Security, Nis 2026) gerçek: her MCP config'i güvenilmez
  kabul et, token'ı URL'ye koyma, env var kullan, resmî dizinleri tercih et.
- HMS motoru ayrı domainde (`*.hmshotel.net`) → cross-domain GA4 zorunlu; HMS yalnız UTM kanal
  takibini belgeler, GA4/Pixel/Ads dönüşüm alanı değil.

## Kategori 1 — Claude Code / MCP / Skills
**Official:**
- Claude Code MCP docs — https://code.claude.com/docs/en/mcp — MCP ekleme, araç izinleri, `.mcp.json`.
- Custom connectors (remote MCP) — https://support.claude.com/en/articles/11175166 — OAuth + güvenlik.
- Use connectors / permissions — https://support.claude.com/en/articles/11176164 — Always allow/Ask/Never.
- MCP connector API — https://platform.claude.com/docs/en/agents-and-tools/mcp-connector — araç allow/denylist.
- anthropics/claude-code · anthropics/skills · anthropics/claude-cookbooks (resmî).
- Agent Skills standard — https://agentskills.io/specification ; MCP — https://modelcontextprotocol.io ;
  MCP Registry — https://github.com/modelcontextprotocol/registry.
**Community dizinler (doğrulama için, tek başına güven sinyali değil):** PulseMCP, Glama, Smithery, mcpservers.org.

## Kategori 2 — Meta / Facebook Ads
**Official:**
- Meta Ads AI Connectors blog — https://www.facebook.com/business/news/meta-ads-ai-connectors
- Meta Business Help (AI agent) — https://www.facebook.com/business/help/1456422242197840 — OAuth kapsam katmanları.
- Endpoint — https://mcp.facebook.com/ads. Bilinen sınırlar: ~200 çağrı/saat, context şişmesi,
  Claude Code OAuth bug (Claude.ai web kullan), Lead Ads TOS hatası (Error 100 / 1815089).
- Meta CAPI dedup — https://developers.facebook.com/documentation/ads-commerce/conversions-api/deduplicate-pixel-and-server-events — `event_id`+`event_name`, 48s pencere.
**Community Meta MCP:**
- pipeboard-co/meta-ads-mcp — yazma yetenekli, default PAUSED; ama token-in-URL desteği (KAÇIN).
  Verdict: **TEST/FORK-ONLY** (resmî connector varken gereksiz). "CVE-2026-48039" **doğrulanamadı**.
- Genel: Resmî connector varken topluluk Meta MCP'leri production için **AVOID** (fork+audit hariç).

## Kategori 3 — Google Ads
**Official:**
- googleads/google-ads-mcp — https://github.com/googleads/google-ads-mcp — resmî, salt okuma;
  `account-performance-diagnostics` Agent Skill ile gelir. Raporlama/teşhis için **USE**.
- Developer guide — https://developers.google.com/google-ads/api/docs/developer-toolkit/mcp-server
- Duyuru — https://ads-developers.googleblog.com/2025/10/open-source-google-ads-api-mcp-server.html
- Token erişim seviyeleri — https://developers.google.com/google-ads/api/docs/api-policy/access-levels (Explorer ~2.880/gün, Basic 15.000/gün).
- validate_only dry-run — https://developers.google.com/google-ads/api/docs/best-practices/testing
- Hotel komisyon teklifi sunset (20 Şub 2025) — https://support.google.com/google-ads/answer/14280291 → tROAS/eCPC/PMax for travel.
- Hotel dönüşüm ölçümü (etiket onay sayfasında, 3. parti motorda bile) — https://support.google.com/google-ads/answer/9244174 (hmshotel.net için doğrudan ilgili).
- Ads API politikaları — https://support.google.com/adspolicy/answer/6169371.
**Community Google Ads MCP / skills (hepsi TEST/FORK-ONLY):**
- google-marketing-solutions/google_ads_mcp — deneysel, mutasyon `ADS_MCP_ENABLE_MUTATIONS=true`.
- cohnen/mcp-google-ads — ~600★, okuma odaklı.
- itallstartedwithaidea/google-ads-skills — güvenli yazma kalıpları + PPC matematiği.
- AgriciDaniel/claude-ads — 250+ denetim skill'i (Google/Meta), MIT, SSRF testleri. Audit/guardrail için iyi.
- nowork-studio/NotFair — RSA üreteci + Pixel/CAPI sağlık denetimi.
- Google Ads Editor CSV: Türkçe karakter (ş/ğ/ı/İ/ç/ö/ü) **UTF-8**; yanlış kodlama RSA'yı sessizce bozar. (kads zaten utf-8-sig BOM yazar.)

## Kategori 4 — Dönüşüm Ölçümü (cross-domain — bu otel için kritik)
- GA4 cross-domain — https://support.google.com/analytics/answer/10071811 (her iki domaini listele; `_gl` linker).
- Consent Mode v2 — https://support.google.com/analytics/answer/14275483 (4 sinyal; son ikisi olmadan Enhanced Conversions sessizce bozulur).
- Next.js third-parties — https://nextjs.org/docs/app/guides/third-party-libraries (`@next/third-parties/google`, `sendGTMEvent`).
- Meta CAPI dedup (Kat. 2). Bilinen ID'ler: GA4 `G-V3R66C3MEF`, Ads `AW-800024713`, Pixel `1781546559309505`.

## Kategori 5 — Öğrenme / Strateji
- Jon Loomer — https://www.jonloomer.com (ileri Meta; Advantage+, creative-first).
- Optmyzr — https://www.optmyzr.com (Google/Microsoft PPC otomasyon + guardrail).
- Search Engine Land — https://searchengineland.com. OtelCiro — https://otelciro.com/en/news (otel GA4 modeli; HMS-spesifik değil).

## Kategori 6 — Güvenlik / Guardrail / Ops
- OX Security MCP STDIO advisory — https://www.ox.security/blog/the-mother-of-all-ai-supply-chains-critical-systemic-vulnerability-at-the-core-of-the-mcp/ (+ CVE yazısı). MCP config'i güvenilmez kabul et, sandbox, sadece resmî dizin, asla token-in-URL.
- Claude Code güvenlik — https://code.claude.com/docs/en/mcp + https://generalanalysis.com/guides/anthropic-claude-code-security-best-practices.
- Kural: her secret env var / secret manager'da; asla `.mcp.json`'da, asla URL'de.

## HMS Otel — dürüst durum (en zayıf doğrulanan alan)
- hmsotel.com (vendor: Tasarım Rehberi, Denizli, 2003). UTM how-to: https://www.hmsotel.com/online-rezervasyon-takibi-nasil-yapilir/ (motorun `*.hmshotel.net` olduğunu + UTM şablonlarını doğrular).
- **Açık:** Hiçbir HMS dokümanı GA4/GTM/Ads/Pixel alanı ya da onay-sayfası dönüşüm olayı göstermiyor.
  **Aksiyon:** HMS desteğine ticket aç — `hmshotel.net` onay sayfasına Ads tag + Meta Pixel konabilir mi?
  Rakip dokümanları (Elektraweb/OtelCiro) HMS'e atfetme.

## Öneriler (fazlı rollout)
1. **Faz 1 — şimdi, salt okuma.** Google resmî read-only MCP + Meta AI Connector (Claude.ai web,
   Claude Code değil — OAuth bug). Meta MCP'yi raporlama araçlarıyla sınırla. Eşik: spend/CPA/ROAS güvenilir çekiliyor.
2. **Faz 2 — ölçüm temeli.** GA4 cross-domain + Consent v2 + Enhanced Conversions + Pixel/CAPI
   (`event_id`). HMS ticket. Eşik: test rezervasyonu GA4 + Meta'da dedup'lı purchase ("2 kaynaktan 1 olay").
3. **Faz 3 — kapılı yazma.** Meta PAUSED, Google `validate_only`, insan onayı, audit log. Hesap düzeyi
   günlük harcama sert tavanı. (kads guardrail bunu zorlar.)
4. **Teklif.** Düşük hacimde Maximize Clicks/Conversions; ~15-30 dönüşüm/ay sonrası tCPA/tROAS.
   Otel envanteri: tROAS/eCPC veya PMax for travel (komisyon teklifi öldü, 20 Şub 2025).
5. **Planı değiştiren tetikler.** Meta MCP beta'dan çıkıp OAuth düzelirse → Meta'yı Claude Code'a taşı;
   HMS onay sayfası tag alırsa → tam Purchase; aylık dönüşüm ~30'u geçerse → value-based Smart Bidding.

## Caveat'lar
- Meta MCP açık beta — araçlar değişir, sessiz hata; yazmadan önce yeniden doğrula.
- "pipeboard CVE-2026-48039" **doğrulanamadı** — gerçek doğrulanan risk OX Security STDIO ailesidir.
- Google Ads Editor CSV alan/kodlama detayını resmî Editor yardımıyla doğrula.
- HMS onay-sayfası davranışı belgeli değil — build'in en büyük bilinmeyeni; HMS ile çöz.
- Yıldız/aktiflik Haziran 2026 anlık; benimsemeden önce son-commit tarihine bak.
