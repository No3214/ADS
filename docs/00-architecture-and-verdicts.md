# 00 — Mimari Kararı ve Repo Değerlendirmeleri (v3)

Bu belge, "tüm GitHub repolarını ve resmî bağlantıları araştır" isteğinin sonucudur.
Karar tarihi: Haziran 2026. Bağlantılar zamanla değişebilir; her madde kaynaklıdır.

## TL;DR — Önerilen mimari

```
Claude (otonom, ama kod seviyesinde frenli)
├── Skill: strateji + reklam metni + analiz (Türkçe güvenli)
├── META  → RESMİ Meta Ads connector  (https://mcp.facebook.com/ads)   [okuma+yazma]
├── GOOGLE(okuma) → RESMİ google-ads-mcp                               [yalnızca okuma]
├── GOOGLE(yazma) → Editor CSV (güvenli)  veya  deneysel google_ads_mcp (mutasyon bayraklı)
└── Yazma katmanı (guardrails.py + change skill):
    allowlist · PAUSED · bütçe tavanı · dry-run · açık onay · ENABLE için 2. onay · audit log
```

**En önemli değişiklik (eski plana göre):** Artık Meta'nın **resmî** AI connector'ı var.
29 Nisan 2026'da "Meta Ads AI Connectors" adıyla yayınlandı ve `https://mcp.facebook.com/ads`
adresinde barındırılıyor. Bu, üçüncü taraf Meta MCP'lerine olan ihtiyacı azaltır ve Meta
tarafını ciddi biçimde güvenli hale getirir. (Kaynak: Meta for Developers duyurusu; çoklu
pazarlama kaynağı, Mayıs 2026.) Eski ChatGPT belgesi bu URL'yi "uydurma" gibi göstermeden
doğru tahmin etmişti; doğrulandı: **gerçek ve resmî.**

## Repo değerlendirme tablosu

| Repo / Servis | Ne yapar | Yazma? | Bakım/Durum | Karar |
|---|---|---|---|---|
| **Meta Ads AI Connectors** (`mcp.facebook.com/ads`) | Resmî Meta connector: hesap/kampanya/ad set/ad okuma + oluşturma/güncelleme/pause | Evet | Resmî, açık beta, ücretsiz (yalnız reklam harcaması) | **KULLAN** (Meta için birincil) |
| **googleads/google-ads-mcp** | Resmî Google MCP: `search` (GAQL), `list_accessible_customers`, `get_resource_metadata` | Hayır (tasarım gereği salt okunur) | Resmî, aktif (son güncelleme ~haftalar) | **KULLAN** (Google okuma/raporlama) |
| **google-marketing-solutions/google_ads_mcp** | Google yazdı; mutasyonlar `ADS_MCP_ENABLE_MUTATIONS=true` ile: bütçe/kampanya/ad grubu/ad/kriter oluşturma | Evet (bayraklı) | Google-authored ama "**production için DEĞİL**, deneysel" | **TEST/FORK** (yazma için, guardrail ile) |
| **anuraagraavi/...Bulk-Editor-Claude-Skill** | Google Ads Editor için CSV üretir; API'ye yazmaz | Hayır (elle import) | Topluluk | **DÜZELTİLEREK** (Türkçe karakter yasağı kaldırılırsa güvenli) |
| **pipeboard-co/meta-ads-mcp** (+ Google/TikTok/Snap/Reddit) | Tek auth ile 5 platform, 230+ araç, yazma onay modeli | Evet | Üçüncü taraf; README token'ı URL query'ye koyuyor (`?token=...`) | **İLK TERCİH DEĞİL** (resmî MCP'ler varken gereksiz; veri 3. tarafta) |
| **ivangfalco/ads-skills** | Meta/Google/LinkedIn doğrudan yazan Python scriptleri | Evet | Topluluk; güvenlik çoğu prompt seviyesinde, secret'lar .env'de | **BİLGİ TABANI** (write scriptleri production'da çalıştırma) |
| **hashcott/meta-ads-mcp-server** | TS Meta MCP; 35 okuma + 19 opt-in yazma | Evet (bayraklı) | Topluluk, aktif | **TEST/FORK** (resmî yoksa alternatif) |
| **çeşitli `*/google-ads-mcp` (samihalawa, gomarble, DigitalRocket vb.)** | Topluluk Google MCP'leri (yazma dahil bazıları) | Değişir | Değişken; biri README'sinde **gerçek secret sızdırmış** | **DİKKAT** (kimlik bilgisi hijyenine örnek; production'a olduğu gibi bağlama) |

> Not (CVE): Eski belgenin "pipeboard CVE-2026-48039, CVSS 9.1" iddiasını **bağımsız
> doğrulayamadım** (CISA/CVE veritabanlarında bu kayda ulaşamadım). Bu yüzden bunu kesin
> gerçek olarak tekrar etmiyorum. Doğrulanabilir olan: pipeboard üçüncü taraftır, README
> token'ı URL'ye koyar (kimlik sızıntısı anti-deseni) ve 2025–2026'da MCP STDIO RCE
> açıkları ailesi belgelenmiştir. Güvenlik önlemi bu doğrulanabilir gerekçelerle ayakta kalır.

## Neden bu mimari

1. **Meta resmî connector** → yazma da dahil olmak üzere ilk taraf, OAuth, "pause-by-default"
   önerisi Meta'nın kendi rehberinde. Üçüncü taraf veri akışı yok.
2. **Google okuma resmî** → raporlama/analiz için en düşük riskli yol; kampanya değiştiremez.
3. **Google yazma** → resmî MCP yazamadığı için iki seçenek: (a) **Editor CSV** (en güvenli,
   elle import), (b) **deneysel Google MCP** mutasyonları, ikisi de `guardrails.py` + change
   skill'in arkasında. Üretimde önce CSV yolu önerilir; tam otonom yazma istenirse deneysel
   MCP guardrail ile açılır.
4. **guardrails.py** → "önce onay al" kuralını prompt'a değil **koda** koyar. Talimat
   enjeksiyonu prompt'u atlasa bile allowlist/PAUSED/bütçe/onay kod seviyesinde durur.

## Claude bağlantı izinleri (tool permissions)

Claude arayüzünde her connector için araç izinleri:

| İşlem türü | Meta | Google |
|---|---|---|
| Raporlama / insights / hesap listeleme | Always allow | Always allow |
| Kampanya/ad set/ad oluşturma | Needs approval | Needs approval |
| Bütçe değiştirme | Needs approval | Needs approval |
| Pause / resume | Needs approval | Needs approval |
| Silme | Blocked | Blocked |
| Ödeme / hesap kullanıcıları | Blocked | Blocked |

Bu izinler `guardrails.py`'ye EK katmandır (savunma derinliği), onun yerine geçmez.
