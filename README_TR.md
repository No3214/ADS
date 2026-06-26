# Kozbeyli Konağı — Claude/MCP Reklam Paketi v3

Claude'un Meta (Instagram) ve Google reklamlarını **otonom ama kod seviyesinde frenli**
yönetmesi için kurulabilir başlangıç paketi. Toplam bütçe 30.000 TL/ay (15.000 Google +
15.000 Meta).

## Bu sürümde doğrulanan kritik gerçekler

1. **Meta artık resmî bir AI connector sunuyor:** `https://mcp.facebook.com/ads`
   (29 Nisan 2026, "Meta Ads AI Connectors"). Okuma + yazma, OAuth, açık beta. Meta tarafının
   birincil yolu budur. Detay: `docs/00-architecture-and-verdicts.md`.
2. **Google resmî MCP'si yalnızca okumadır** (`googleads/google-ads-mcp`). Yazma için
   deneysel Google MCP veya Google Ads Editor CSV gerekir.
3. **Rezervasyon motoru = HMS Otel**, ve motor **ayrı alan adında**: `{slug}.hmshotel.net`.
   Bu yüzden **çapraz alan ölçümü zorunlu**. Detay: `docs/01-hms-otel-tracking.md`.

## Klasör yapısı

```
.mcp.json.example              Resmî Meta + resmî Google okuma + (kapalı) deneysel Google yazma
.env.example                   Kimlikler ve bütçe sınırları (secret'sız)
config/ads-assets.yaml         Doğrulanmış mimari, allowlist, bütçe, eksikler
scripts/guardrails.py          KOD SEVİYESİNDE güvenlik + audit log (paketin kalbi)
scripts/preflight.py           Ön kontrol
tracking/                      Next.js 15 Consent Mode v2 + GTM + olay helper'ları + HMS snippet
assets/                        Türkçe RSA varlıkları (+ uzunluk doğrulayıcı) + Meta kreatif konsept
plans/                         30.000 TL kanal planı
docs/                          Mimari/verdict, HMS tracking, GTM, 90 gün, güvenlik
.claude/skills/                Monitör (salt okunur) + Change (guardrail çağıran) skill'leri
```

## Bilinen ölçüm kimlikleri

- GA4: `G-V3R66C3MEF` · Google Ads: `AW-800024713` · Meta Pixel: `1781546559309505`
- Meta Business ID: `604201716594111`
- GTM adayları: `GTM-KCG6B4MJ`, `GTM-MSL2FLF5` (canlı olanı `docs/02` ile belirleyin)

## Eksikler (siz dolduracaksınız)

- Meta `act_...` reklam hesabı ID · Google Ads 10 haneli müşteri ID · doğru GTM container
- Google Developer Token + Cloud Project + OAuth/ADC
- `hmshotel.net` üzerindeki gerçek otel slug'ı + onay sayfası purchase davranışı

> Token, refresh token, client secret veya OAuth dosya içeriğini sohbete ya da GitHub'a
> koymayın. URL query'ye token koymayın. (Neden: `docs/04-security-and-ban-risk.md`)

## Kurulum

```bash
cp .mcp.json.example .mcp.json
cp .env.example .env            # .env'i doldurun (secret'lar burada, git-ignored)
python3 scripts/preflight.py    # ön kontrol
claude                          # Claude Code başlat, /mcp ile bağlantıları gör
```

İlk aşamada **yalnızca salt okunur** analiz yapın:

```text
/kozbeyli-ads-monitor son 7 günü önceki 7 günle karşılaştır
```

Tracking'i test rezervasyonuyla doğrulayın (`tracking/README_TRACKING_TR.md` + `docs/01`),
sonra yazmayı kademeli açın.

## Yazmayı açma (ölçüm doğrulandıktan SONRA)

1. `config/ads-assets.yaml` → `write_guardrails.enabled: true`
2. `.env` → `ADS_WRITES_ENABLED=true`
3. Allowlist'i gerçek ID'lerle doldur.
4. Değişiklikleri `/kozbeyli-ads-change` ile yap; her mutation `guardrails.py`'den geçer:
   ```bash
   python3 scripts/guardrails.py --check change.json --approval "ONAYLA | google | 123-456-7890 | create_campaign | 148"
   ```
   Çıkış: 0=izinli, 1=reddedildi, 2=onay bekliyor. `ENABLED` için ikinci onay (`ONAYLA-2`).

## Güvenlik özeti

- Onay prompt'ta DEĞİL, **kodda** zorunlu (`guardrails.py`) + connector izinlerinde
  (Needs approval / Blocked). Üç katman.
- Yeni kampanyalar PAUSED. Sabit bütçe tavanı. Delete/ödeme/kullanıcı/liste yükleme yok.
- Her işlem `logs/ads-change-audit.jsonl` içine kaydedilir.

## Önemli not (tahmin vs garanti)

Plandaki tüm CPC/CTR/CVR/CPA/rezervasyon sayıları **planlama tahminidir, garanti değildir**.
Gerçek maliyetler teklif, bütçe, reklam kalitesi, sezon, konum ve rekabete göre değişir.
