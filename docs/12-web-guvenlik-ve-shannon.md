# 12 — Web Güvenliği + Shannon (yetkili kullanım)

## Shannon nedir
`KeygraphHQ/shannon` — açık kaynak, **otonom beyaz-kutu AI pentester** (web app + API). Kaynak
kodunu analiz eder, saldırı yollarını bulur ve **çalışan uygulamaya karşı gerçek exploit
çalıştırır**. Claude Agent SDK ile çalışır. Repo: https://github.com/KeygraphHQ/shannon
(GitHub'ın en çok yıldızlı açık kaynak AI pentester'ı; XBOW benchmark'ta yüksek başarı).

## Neden Claude burada onu canlı siteye karşı ÇALIŞTIRMADI (dürüst)
Bu, meşru bir güvenlik aracıdır ama sorumlu kullanım sınırları var; bu oturumdan otelin
**canlı production** sitesine karşı otonom exploit çalıştırmak doğru/güvenli değil:
1. **Yetki + kapsam:** Pentest yalnız **sahibi olduğun/izin verdiğin** sistemde yapılır. Site
   senin → yetkiyi sen verebilirsin; ama bu, kayıt altında ve kontrollü ortamda yapılmalı.
2. **Production riski:** "Gerçek exploit çalıştırma" canlı rezervasyon sitesinde kesinti/veri
   riski üretebilir. Önce **staging/kopya** üzerinde çalıştır.
3. **Beyaz-kutu girdisi:** Shannon en iyi sonucu **kaynak kodla** verir; sitenin kaynağı bu
   ortamda yok.
4. **Ortam:** Tam pentest çatısını (browser automation + exploit araçları) bu sandbox'tan dış
   prod'a sürmek uygun değil.

Doğru yol: **kendi makinende, kendi sitene/staging'ine karşı, yetkiyle** çalıştır (aşağıda).

## Shannon'u doğru çalıştırma (kendi ortamında)
```bash
git clone https://github.com/KeygraphHQ/shannon.git
cd shannon
# README'deki kurulum (Node + bağımlılıklar). Reasoning motoru için:
export ANTHROPIC_API_KEY=...        # sohbete/URL'ye yazma; env var
# Hedef: ÖNCE staging veya yerel kopya. Kaynak kod erişimi beyaz-kutu için ideal.
# Yetki: yalnız sahibi olduğun sistem. Yedek al. Çalışmayı kayıt altına al.
```
> Çıktıyı (bulgu + kanıt) bir güvenlik raporu olarak sakla; düzeltmeleri staging'de uygula,
> sonra production'a al. Şüphede profesyonel destek al.

## Bu arada: pasif güvenlik hijyeni (exploit'siz, denetimden)
Dijital denetimde (docs/09) çıkan, exploit gerektirmeyen güvenlik/itibar bulguları:
- **`kozbeylikonagiotel.com` `http://` (HTTPS yok)** + yanlış telefon → kaldır/301. Hem güvenlik
  (şifresiz) hem marka riski. **Kritik.**
- **Üç domain = gereksiz saldırı yüzeyi.** `.com` canonical, diğerlerini 301 → yüzeyi küçült.
- **Güvenlik başlıkları** (öneri, `.com` için): `Strict-Transport-Security` (HSTS),
  `Content-Security-Policy`, `X-Content-Type-Options: nosniff`, `Referrer-Policy`,
  `X-Frame-Options`/frame-ancestors. Next.js'te `next.config.js` headers() ile eklenir.
- **Bağımlılık hijyeni:** Next.js + paketleri güncel tut (bilinen CVE'ler için `npm audit`).
- **HMS rezervasyon:** ödeme akışı HMS'te; kart verisi sitende tutulmuyor (iyi). HMS tarafı
  güvenliği sağlayıcıda — onları PCI/güvenlik için teyit et.
- **Form/WhatsApp:** iletişim formunda rate-limit + spam koruması; WhatsApp linki doğru numara.

## Önerilen sıra
1. Önce pasif hijyen (yukarıdaki 6 madde) — hızlı, risksiz, yüksek getiri.
2. `.com`'a güvenlik başlıkları + HSTS.
3. Sonra staging'de Shannon ile beyaz-kutu pentest (yetkiyle, yedekle).
