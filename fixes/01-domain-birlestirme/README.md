> **GÜNCEL (Haz 2026):** `.com.tr` TERK EDİLDİ (menü `.com`'a taşındı). Bu 301 yönlendirme artık ZORUNLU DEĞİL; yalnızca `.com.tr`/`kozbeylikonagiotel.com` hâlâ erişilebiliyorsa marka koruması için uygulayın.

# Domain birleştirme (301) — en yüksek getirili düzeltme

Hedef: tek kanonik domain **`https://www.kozbeylikonagi.com`**. Yönlendirmeler **kaynak
domainin** (yani `.com.tr` ve `kozbeylikonagiotel.com`) barındırıldığı yere konur, hepsi
`.com`'a 301. Ayrıca `.com`'da `www` kanonikleştir + `<link rel="canonical">` self.

Adımlar:
1. `.com` = kanonik. `.com`'da her sayfada self-canonical (Next.js `metadata.alternates.canonical`).
2. `.com.tr` host'una: tüm yolları `https://www.kozbeylikonagi.com/$1`'e 301 (aşağıdaki configlerden biri).
3. `kozbeylikonagiotel.com` host'una: aynı 301 + **yanlış telefonu kaldır**; sahiplik aracıda ise iletişime geç.
4. Search Console'da adres değişikliği + sitemap'i `.com`'a güncelle. OTA/GBP/sosyal linkleri `.com`.

Hangi dosya: Vercel → `vercel.json`; Netlify → `netlify.toml` veya `_redirects`;
Apache → `apache.htaccess`; Nginx → `nginx.conf`.
