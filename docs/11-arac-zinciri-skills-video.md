# 11 — Araç Zinciri: Meta Skill'leri · Video Kreatif · Geliştirme

Kozbeyli sistemine eklenebilecek, dış (topluluk) araçlar. Hepsi **opsiyonel**; reklam hesabına
yazan her şey yine `kads guard` / guardrails + açık onaydan geçer. Topluluk skill'lerini
production'da kullanmadan önce **fork + audit** et (docs/04, docs/10).

## A. Meta reklam Claude Code skill'leri (analiz/read tarafı — düşük risk)
Kaynak: "5 Claude Code Skills That Replace Your Meta Ads Agency" (Cindy / @cindiezhu) +
referans kütüphanesi (docs/10). Çoğu **AgriciDaniel/claude-ads** paketinde.

| Skill | Ne yapar | Kurulum |
|---|---|---|
| `/spy` | Bir FB sayfasının tüm aktif reklamlarını Meta Ad Library API'den çeker; geçen haftaya göre fark | `npx skills add https://github.com/AgriciDaniel/claude-ads` |
| `/competitive-ads-extractor` | 3-5 rakip → hook sıralaması + gap analizi (kimsenin kullanmadığı açı) | `npx skills add https://github.com/ComposioHQ/awesome-claude-skills/tree/master/competitive-ads-extractor` |
| `/bulk-creative` | Ürün + CLAUDE.md marka bağlamı → ~20 reklam metni varyantı (~10 dk) | `npx skills add https://github.com/AgriciDaniel/claude-ads` |
| `/ads meta` | Meta hesabında 186 kontrol: kreatif yorgunluğu, kitle çakışması, CPM/frekans anomalisi; 0-100 sağlık skoru | `npx skills add https://github.com/AgriciDaniel/claude-ads` |
| `/ads-score` | Bir reklamı 6 boyutta (hook/kopya/CTA/duygu/teklif/görsel-uyum) 1-10 puanlar | `npx skills add https://github.com/AgriciDaniel/claude-ads` |

**Zincir (haftalık < 1 saat):** `/spy` (Pzt rakip taraması) → `/competitive-ads-extractor` (gap) →
`/bulk-creative` (20 varyant) → `/ads-score` (yayından önce, <7 ise hook'u değiştir) →
`/ads meta` (haftalık fatigue/overlap).
**Ön koşul:** Meta Ad Library API token → `export META_ACCESS_TOKEN=...` (sohbete yazma).
**Kozbeyli notu:** Bunlar rakip istihbaratı + kreatif üretimi + denetim için ideal (Bülbül
Yuvası, Huri Nuri, Foça Ensar + Foça OTA'larını izle). Üretilen metinleri `campaigns/meta/`
ile birleştir. **Yazma yok** — sadece analiz/öneri; hesaba değişiklik kads guardrail ile gider.
**Bonus:** `coreyhaines31/marketingskills` — CRO/copywriting/SEO/analytics skill'leri (community).

## B. Video kreatif — Palmier Pro (ücretsiz, açık kaynak, AI-native)
Meta için Reels/Stories **9:16** ve Feed **4:5** video üretmek gerekiyor (docs/06). En uygun
araç: **Palmier Pro** — Claude'un timeline'ı MCP ile sürebildiği açık kaynak (GPLv3) video editörü.
- Repo: https://github.com/palmier-io/palmier-pro (~3.500★). Site: https://www.palmier.io/
- **Ücretsiz:** çekirdek editör + MCP sunucusu + agent chat açık kaynak ve login'siz (CapCut/Premiere gibi).
  Yalnızca **generatif AI** işleme kapalı/abonelik.
- **Platform:** **yalnız macOS 26 (Tahoe) + Apple Silicon.** Sen Windows'tasın → seçenekler:
  - **Windows portu (topluluk, audit et):** https://github.com/Voidsprog/palmier-pro-windows
  - **Ücretsiz alternatifler:** DaVinci Resolve (ücretsiz), Shotcut, OpenShot, CapCut (ücretsiz).
  - **Kod ile (AI-dostu):** Remotion / revideo (React ile programatik video — markalı şablon üretimi).
- **Claude'a bağlama (macOS'ta MCP):** Palmier'in MCP sunucusunu Claude connector olarak ekle;
  Claude "konaktan terasa geçiş, 9:16, gün batımı" gibi kreatif konseptleri (campaigns/meta) timeline'a uygular.
- **Kozbeyli iş akışı:** ham çekim (konak/oda/teras/kahvaltı/evcil) → konsept (META_COPY) → Palmier'de
  kurgu → 9:16 + 4:5 dışa aktar → `campaigns/meta` metniyle yayınla.

## C. Geliştirme — Codex plugin (kads kod bakımı için)
Kaynak: yasinarsal rehberi. `openai/codex-plugin-cc` (resmî OpenAI Claude Code plugin'i, ~19k★,
Apache-2.0) Codex'i Claude Code'a subagent takar: Claude planlar, Codex kod cerrahisi, sen review.
- Kurulum: `/plugin marketplace add openai/codex-plugin-cc` → `/plugin install codex@openai-codex`
  → `/reload-plugins` → `/codex:setup` (→ gerekirse `/codex login`).
- Faydalı komutlar: `/codex:review --background`, `/codex:adversarial-review --challenge "..."`,
  `/codex:rescue --background "..."` (Claude bir bug döngüsüne girince devret).
- **Kozbeyli notu:** `kads` paketini büyütürken (yeni platform/komut) review/rescue için kullanışlı.
  Yeni billing açmaz (ChatGPT/OpenAI key'ine sayılır). Review-gate'i sürekli açık bırakma.

> Tüm bu araçlar harici/topluluktur. Reklam hesabına veya siteye etki eden hiçbir işlem,
> Kozbeyli guardrail'lerini (PAUSED + bütçe tavanı + açık onay + audit) atlamaz.
