# 26 — Canlı Site Sayfa-İçi SEO + Şema Denetimi (Haz 2026)

Yöntem: `www.kozbeylikonagi.com` canlı tarayıcıda render edilmiş halinden okundu (ana sayfa + /lokasyon),
robots.txt + sitemap.xml ayrıca doğrulandı. Tahmin yok.

## Sonuç: site SEO'su GÜÇLÜ — asıl iş on-page değil, ÖLÇÜM
Site teknik/sayfa-içi SEO açısından iyi kurulmuş. Reklama hazır; öncelik docs/24 (GTM etiket) + docs/25 (GSC/Bing).

## Sayfa denetimi
| Sayfa | Title (uzn) | Meta (uzn) | H1 | JSON-LD | hreflang |
|---|---|---|---|---|---|
| Ana (`/`) | "Kozbeyli Konağı \| Foça Taş Butik Otel & Restoran" (48) | 120 | 1 — "Tarihin Kalbinde Zarif Bir Ege Kaçamağı" | **Hotel/LodgingBusiness/Restaurant + BreadcrumbList + FAQPage** | tr/en/x-default |
| `/lokasyon` | "Lokasyon & Yol Tarifi \| Kozbeyli Konağı" (39) | 147 | 1 — "Kozbeyli'nin Merkezinde" | Hotel/LodgingBusiness/Restaurant + BreadcrumbList | tr/en/x-default |

## Güçlü yanlar (doğrulandı)
- Title 39-60 ve meta 120-160 aralığında, **tek H1** her sayfada — temiz yapı.
- **Zengin JSON-LD**: Hotel + LodgingBusiness + Restaurant + BreadcrumbList; **ana sayfada FAQPage** (AI alıntısı için ideal).
- **hreflang tr / en / x-default** + canonical doğru (self-canonical).
- **robots.txt** tüm AI botlarına açık (GPTBot/ClaudeBot/PerplexityBot/Bingbot...) + `Sitemap:` tanımlı.
- **sitemap.xml** canlı, hreflang'li, taze lastmod.

## Küçük fırsatlar (opsiyonel, düşük öncelik)
1. **HotelRoom şeması** — oda detay sayfalarına `HotelRoom` (ad, fiyat, manzara, kapasite) ekle → zengin oda sonucu + retargeting.
2. **Meta ViewContent** — oda sayfalarında ateşlemiyor (docs/23); content_ids+value ile ekle.
3. **H1'de bölge kelimesi** — ana H1 "Tarihin Kalbinde..." şiirsel; "Foça butik otel" gibi bir kelime H2/alt başlıkta güçlendirilebilir (opsiyonel; mevcut yapı zaten iyi).

## ⚠️ DOĞRULANACAK: Foça'ya mesafe
Sistemde/GBP'de **"Foça merkeze ~13 km"** geçiyor; ama `/lokasyon` sayfasında metinde km figürü görünmedi ve coğrafi
kaynak (MEB) Kozbeyli'yi **Eski Foça merkeze ~22 km / Yeni Foça'ya ~10 km** konumlandırıyor. "13 km" sürüş mesafesi
olabilir ama **doğrulanmadı**. Güvenli pazarlama dili: **"Yeni Foça'ya yakın"** (doğrulandı). Net km kullanılacaksa
sahip teyit etsin; reklam/GBP'de yanlış sabit sayı = küçük itibar/uyum riski.

## Özet
On-page SEO + şema: **GÜÇLÜ, müdahale gerektirmiyor** (küçük HotelRoom/ViewContent fırsatları hariç). Darboğaz
on-page değil — **ölçüm (GTM içi GA4/Ads etiketi) + GSC/Bing doğrulama + Google yorum hızı.** Bkz. docs/22-25.
