# Attribution Modeli — Kozbeyli Konağı

`kads attribution` bu modeli özetler. Amaç: bütçeyi doğru kanala vermek için
dönüşümü adil dağıtmak ve aynı rezervasyonu iki kez saymamak.

## Katmanlar
| Katman | Model | Pencere | Not |
|---|---|---|---|
| GA4 raporlama | Data-driven (DDA) | 30 gün tıkla / 1 gün gör | Turizmde karar uzun |
| Google Ads dönüşüm | Data-driven (DDA) | 30 gün | Son-tık değil; tüm yolu değerlendirir |
| Meta Ads | 7 gün tıkla / 1 gün gör | 7-1 | View-through'a şüpheli yaklaş |
| Kaynak otorite (dedup) | GA4 = tek gerçek | - | Google+Meta aynı rezervasyonu sayar |
| purchase tekillik | transaction_id (HMS rez. no) | - | Aynı rez. iki kez sayılmaz |
| Meta CAPI dedup | event_id eşleşme | - | Pixel+CAPI aynı event_id |
| Karar (yönetim) | Blended CPA/ROAS | aylık | Tek platform metriğine takılma |

## İlkeler
1. **Cross-domain zorunlu**: purchase `{slug}.hmshotel.net`'te olur; GA4 cross-domain yoksa
   yolculuk kopar ve dönüşümler "(direct)" görünür (tracking/implementation/03).
2. **Çift sayım**: Google ve Meta her ikisi de aynı rezervasyonu kendine yazar → toplam şişer.
   GA4'ü hakem al, kararı **blended** (Google+Meta birleşik) ROAS/CPA ile ver.
3. **View-through** dönüşümü ayrı raporla; kararı click-through ağırlıklı ver.
4. **Lookback** turizmde uzun (30 gün tıkla); kısa pencere yeni talebi öldüren gösterir.
5. **UTM tutarlılığı** attribution'un temelidir → her linki `kads utm` ile etiketle.
