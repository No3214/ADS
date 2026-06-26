# HMS Otel destek talebi (cross-domain ölçüm) — e-posta taslağı

Konu: Rezervasyon motoru (hmshotel.net) dönüşüm takibi — GA4/GTM/Pixel

Merhaba,

Kozbeyli Konağı olarak rezervasyon motorumuz `kozbeyli-konagi.hmshotel.net` üzerinde
çalışıyor. Web sitemiz (`kozbeylikonagi.com`) ile motor ayrı alan adında olduğu için
çapraz alan (cross-domain) dönüşüm ölçümü kurmamız gerekiyor. Lütfen şu 6 noktayı netleştirin:

1. Otelimizin gerçek alt alanı `kozbeyli-konagi.hmshotel.net` mi? (teyit)
2. Onay (teşekkür) sayfasının URL deseni nedir? (dönüşüm tetikleyicisi buna bağlanır)
3. Panelde GA4 / GTM / Meta Pixel / Google Ads ID girilebilecek bir alan var mı?
4. Onay sayfasına kendi GTM container'ımızı veya gtag/fbq snippet'imizi ekleyebilir miyiz?
5. Onay sayfası `dataLayer` ile `transaction_id`, `value`, `currency` (TRY) veriyor mu?
6. Ödeme akışı tam sayfa yönlendirme mi? (cross-domain linker bBuna göre kurulur)

Mümkünse onay sayfasına Google Ads dönüşüm etiketi + Meta Pixel koymak istiyoruz; mümkün
değilse offline dönüşüm yükleme / CAPI yedeğine geçeceğiz (docs/01). Yardımınız için teşekkürler.

Saygılarımızla,
Kozbeyli Konağı — +90 532 234 2686
