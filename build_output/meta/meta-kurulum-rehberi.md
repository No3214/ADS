# Meta Ads Manager — Kurulum Rehberi (Kozbeyli Konağı)

Bütçe: Meta 15.000 TL/ay. Tüm kampanyalar **PAUSED** kurulur. Website Sales
yalnızca Pixel+CAPI'de `Purchase` güvenilirse açılır; değilse önce tracking +
WhatsApp akışı çalışır, en derin güvenilir olaya (`begin_checkout`) optimize edilir.

Kreatif oranları: Reels/Stories **9:16**, Feed **4:5**. Yerleşim: **Advantage+**
(küçük bütçede manuel bölme yok). İlk ay **en fazla 2 kampanya**.

Resmî yol: `https://mcp.facebook.com/ads` connector (OAuth) veya Ads Manager elle.

## Faz 1 — İlk 30 gün (2 kampanya)

### Kozbeyli | Prospecting | Website Sales
- **Amaç (Objective):** Sales (Conversions)
- **Bütçe:** 350 TL/gün (10500 TL/ay) — CBO uygun
- **Durum:** PAUSED (review'dan sonra ENABLE)
- **Kitle:** Prospecting (detay aşağıda)
- **Optimizasyon olayı:** Purchase (güvenilirse) — değilse begin_checkout / Lead
- **Yerleşim:** Advantage+ (otomatik)
- **Kreatifler:** Konsept1-TasKonak, Konsept2-Manzara, Konsept3-Kahvalti, Konsept4-Evcil

### Kozbeyli | WhatsApp | Mesaj
- **Amaç (Objective):** Engagement (Messaging → WhatsApp)
- **Bütçe:** 150 TL/gün (4500 TL/ay) — CBO uygun
- **Durum:** PAUSED (review'dan sonra ENABLE)
- **Kitle:** Prospecting (detay aşağıda)
- **Optimizasyon olayı:** Conversations (mesaj başlatma)
- **Yerleşim:** Advantage+ (otomatik)
- **Kreatifler:** Konsept5-WhatsApp, Konsept2-Manzara

## Faz 2 — Ay 2+ (3 kampanya)

### Kozbeyli | Prospecting | Website Sales
- **Amaç (Objective):** Sales (Conversions)
- **Bütçe:** 300 TL/gün (9000 TL/ay) — CBO uygun
- **Durum:** PAUSED (review'dan sonra ENABLE)
- **Kitle:** Prospecting (detay aşağıda)
- **Optimizasyon olayı:** Purchase
- **Yerleşim:** Advantage+ (otomatik)
- **Kreatifler:** Konsept1-TasKonak, Konsept2-Manzara, Konsept3-Kahvalti

### Kozbeyli | Retargeting | Website Sales
- **Amaç (Objective):** Sales (Conversions)
- **Bütçe:** 100 TL/gün (3000 TL/ay) — CBO uygun
- **Durum:** PAUSED (review'dan sonra ENABLE)
- **Kitle:** Retargeting (detay aşağıda)
- **Optimizasyon olayı:** Purchase
- **Yerleşim:** Advantage+ (otomatik)
- **Kreatifler:** Konsept2-Manzara, Konsept4-Evcil

### Kozbeyli | WhatsApp | Mesaj
- **Amaç (Objective):** Engagement (Messaging → WhatsApp)
- **Bütçe:** 100 TL/gün (3000 TL/ay) — CBO uygun
- **Durum:** PAUSED (review'dan sonra ENABLE)
- **Kitle:** Prospecting (detay aşağıda)
- **Optimizasyon olayı:** Conversations
- **Yerleşim:** Advantage+ (otomatik)
- **Kreatifler:** Konsept5-WhatsApp

## Kitleler

### Prospecting
- **tip:** Geniş + ilgi sinyali (Advantage+ kitle önerilir, dar tutma)
- **konum:** İstanbul, Ankara, İzmir, Bursa + 25 km Foça çevresi
- **yas:** 28-60
- **diller:** Türkçe
- **ilgi:** Butik otel, Seyahat, Hafta sonu kaçamağı, Doğa turizmi, Gurme/yeme-içme, Evcil hayvan sahipleri, Ege/Foça
- **not:** Öğrenme aşaması için kitleyi aşırı daraltma; tek ad set, 3-4 kreatif.

### Retargeting
- **tip:** Custom Audience (ay 2+, liste dolunca)
- **kaynaklar:** Site ziyaretçisi 30/60 gün, IG/FB etkileşim 365 gün, rezervasyon başlatıp tamamlamayan (begin_checkout)
- **not:** Site/IG kitlesi yeterince dolmadan AÇMA.

### Lookalike
- **tip:** LLA %1-3 (yeterli dönüşüm/etkileşim sonrası)
- **kaynak:** Purchase veya WhatsApp lead custom audience
- **not:** Veri eşiği oluşmadan açma; prospecting'i önce doğrula.

## Reklam metinleri
Konsept bazında primary text / başlık / CTA için `meta-reklam-metinleri.csv`.

## Kurulum sırası (Ads Manager)
1. Pixel + CAPI doğrula (Test Events: Purchase / InitiateCheckout / Lead).
2. Kampanya oluştur (amaç), bütçe gir, PAUSED bırak.
3. Ad set: kitle + yerleşim (Advantage+) + optimizasyon olayı.
4. Reklamlar: her konsept için 9:16 + 4:5 kreatif, metni CSV'den yapıştır.
5. Review → ölçüm doğrulanınca ENABLE (ikinci onay: `kads guard`).

## KPI
- Maksimum CPL = rezervasyon CPA × (lead→rezervasyon oranı)
- Örnek: Rezervasyon CPA 2.000 TL, kapanış %15 → maksimum WhatsApp lead maliyeti 300 TL.
- Başarı blended (Google+Meta) CPA ve ROAS ile ölçülür; tek platform metriğine takılma.