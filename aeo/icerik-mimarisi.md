# İçerik Mimarisi (sayfa → niyet → şema)

İskelet: **Soru-H1 → 40–70 kelime yanıt → detay → liste/adım → karşılaştırma → FAQ → tarih → CTA.**

| Sayfa | Niyet | Şema |
|---|---|---|
| Ana sayfa | Marka + varlık | Hotel, Organization, WebSite, BreadcrumbList |
| /odalar + oda detay | Ticari | Hotel (parent) + HotelRoom (+Offer), BreadcrumbList |
| /gastronomi + /menu | Deneyimsel | Restaurant, BreadcrumbList |
| /organizasyonlar | Etkinlik | Hotel + düz içerik + FAQPage (Event YALNIZ gerçek tarihli) |
| /lokasyon | Yerel | Hotel (geo), BreadcrumbList |
| /sss | Hepsi | FAQPage (görünür sorularla birebir) |
| /deneyimler/* | Bilgilendirme | Article/TouristAttraction, BreadcrumbList |
| YENİ: Foça'ya nasıl gidilir | Yerel | FAQPage + Article |
| YENİ: Foça mı Alaçatı mı | Karşılaştırma | Article + FAQPage |
| YENİ: Foça'da ne zaman gidilir | Mevsimsel | Article + FAQPage |

**Yapma:** geçmiş tarihli Event şeması; sahte puan/fiyat; client-side render'a geçme.
