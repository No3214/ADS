# 25 — Google Search Console + Bing Webmaster Kurulumu (Vercel DNS)

Tarayıcıda/DNS'te canlı doğrulandı (Haz 2026). Amaç: organik arama görünürlüğü + AEO ön koşulu.

## ⚠️ ÖNCE: doğru alan adını gir
GSC ekranında **"wwwkozbeylikonagi.com"** (www ile kozbeyli arasında nokta yok) görünüyordu — bu **YANLIŞ/var olmayan** alan.
**Alan adı (Domain) mülkü** seç ve tam olarak şunu yaz: **`kozbeylikonagi.com`** — www YOK, https:// YOK, nokta eksiksiz.

## Neden Domain mülkü
Tüm alt alanlar (www, root) + http/https tek mülkte toplanır — en iyi kapsam. Doğrulama = **DNS TXT**.

## DNS = Vercel (doğrulandı: ns1/ns2.vercel-dns.com)
TXT kaydı GoDaddy/Cloudflare'e DEĞİL, **Vercel'e** eklenir.
1. GSC: Domain mülkü → `kozbeylikonagi.com` → GSC sana bir **TXT değeri** verir: `google-site-verification=XXXXXXXX`.
2. **vercel.com** → `kozbeylikonagi.com` projesi → **Settings → Domains** (veya DNS bölümü) → **Add / DNS Records**.
3. Yeni kayıt: **Type=TXT · Name=`@`** (kök; Vercel'de boş/`@`) · **Value=** GSC'nin verdiği `google-site-verification=...` · TTL=varsayılan → **Save**.
4. **Mevcut SPF TXT'ye DOKUNMA** (`v=spf1 include:_spf.protection.veridyen.com include:relay.mailchannels.net ~all`) — e-postan ona bağlı. Yeni TXT'yi AYRI kayıt olarak ekle.
5. 5-30 dk bekle → GSC'de **Doğrula**.

## Doğrulama sonrası (sırayla)
1. **Sitemap gönder:** GSC → Sitemaps → `sitemap.xml` yaz, gönder. (Canlı: `https://www.kozbeylikonagi.com/sitemap.xml`, hreflang tr/en, ~57 URL.)
2. **URL İnceleme → Dizine ekleme iste:** ana sayfa, /odalar, /rezervasyon, /gastronomi, /lokasyon.
3. **Bing Webmaster Tools** (bing.com/webmasters): **"Import from Google Search Console"** (1 tık, GSC doğrulandıktan sonra en hızlı) → sitemap gönder → **IndexNow AÇ**.
   *Bu, ChatGPT alıntılarının ön koşulu — rakiplerin atladığı ucuz avantaj.*
4. (Opsiyonel) **Yandex Webmaster** — TR trafiği için; sitemap gönder.

## İyi haber (canlı doğrulandı)
- **robots.txt** tüm AI botlarına AÇIK: GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot/Claude-User/Claude-SearchBot, PerplexityBot, Google-Extended, Bingbot, Applebot-Extended — engel YOK + `Sitemap:` tanımlı. AEO temeli sağlam.
- **sitemap.xml** canlı, hreflang TR/EN, taze lastmod.
- Eksik = sadece doğrulama + sitemap submit + Bing/IndexNow. İçerik tarafı (şema/FAQ) için docs/22-24.

## Alternatif (Domain DNS'i yapamazsan)
URL-prefix mülkü `https://www.kozbeylikonagi.com` → **HTML tag** yöntemi: Next.js `app/layout` head'ine GSC'nin verdiği
`<meta name="google-site-verification" ...>` ekle (Vercel deploy). Ama Domain mülkü daha geniş — onu tercih et.
