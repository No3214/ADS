# 02 — Doğru GTM Container'ı Belirleme

Elinizde iki aday var: `GTM-KCG6B4MJ` ve `GTM-MSL2FLF5`. Yalnızca biri canlı sitede
çalışıyor olmalı; ikisi birden yüklüyse **çift etiketleme** (double tagging) ve şişmiş
veri riski vardır.

## Neden curl ile bulunamadı

`kozbeylikonagi.com` istemci tarafında render edilen bir Next.js uygulamasıdır.
Etiketler sayfa yüklendikten SONRA JavaScript ile enjekte edilir; sunucudan gelen ham
HTML'de (`curl`/view-source) görünmezler. Bu yüzden container'ı **gerçek tarayıcıda**
belirlemek gerekir.

## Yöntem A — Tag Assistant (en kesin)
1. `tagassistant.google.com` > "Add domain" > `https://www.kozbeylikonagi.com`.
2. Bağlandığında yüklenen container ID(leri) listelenir.
3. Hangi `GTM-XXXX`'in ateşlediğini not edin. İki tane görünüyorsa biri kaldırılmalı.

## Yöntem B — Tarayıcı DevTools
1. Siteyi açın > F12 > Network sekmesi > filtreye `gtm.js` yazın.
2. İstek URL'sinde `?id=GTM-XXXXXXX` parametresini okuyun.
3. Console'da şunu çalıştırın:
   ```js
   (window.dataLayer||[]).filter(x => x && x['gtm.start'])
   document.querySelectorAll('script[src*="gtm.js"]').forEach(s=>console.log(s.src))
   ```
   Çıkan ID(ler) canlı container'dır.

## Yöntem C — GTM Preview
1. `tagmanager.google.com` > doğru hesaba girin.
2. Her iki container için "Preview" > site URL'si ile bağlanmayı deneyin.
3. Hangi container siteyle başarılı bağlanıyorsa canlı odur.

## Karar kuralı
- Sitede **fiilen ateşleyen** container'ı kullanın; diğerini arşivleyin.
- Seçtiğiniz ID'yi şuralara yazın: `.env` (`NEXT_PUBLIC_GTM_ID`, `GTM_CONTAINER_ID`) ve
  `config/ads-assets.yaml` (`tracking.gtm_status: resolved` + tek ID).
- `hmshotel.net` onay sayfasına da mümkünse **aynı** container'ı koyun (tek yerden yönetim).

## Çift container bulursanız
İkisi de ateşliyorsa: GA4/Ads/Pixel etiketleri hangisinde tanımlıysa onu bırakın,
diğerini siteden kaldırın. Aksi halde dönüşümler iki kez sayılabilir.
