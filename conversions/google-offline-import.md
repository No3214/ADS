# Google Offline Conversion Import (OCI) — telefon/WhatsApp rezervasyonu

`kads conversions offline`. Amaç: reklamı tıklayıp sonra **telefonla/WhatsApp'tan** rezervasyon
yapan müşteriyi Google'a "dönüşüm" olarak geri yüklemek. Böylece Smart Bidding offline kapananları
da öğrenir.

## Ön kurulum (bir kez)
1. Google Ads > Hedefler > Dönüşümler > **Yeni > İçe aktarma > Diğer veri kaynakları / CSV**.
2. Dönüşüm adı: `booking_offline`. Kategori: Satın alma. Değer: kullan (rezervasyon tutarı).
3. Sitedeki forma `gclid-capture.html` snippet'ini ekle (GCLID yakalansın).

## Her rezervasyonda (akış)
1. **GCLID yakala**: ziyaretçi formu gönderirken gizli alan `gclid` (snippet doldurur).
   Yoksa `wbraid`/`gbraid` (iOS/uygulama).
2. **Lead'i sakla**: WhatsApp/telefon görüşmesini gclid + zaman + kişi ile Sheets/CRM'e yaz.
3. **Kapanınca**: satır ekle → `offline-import-template.csv` formatında: GCLID, booking_offline,
   zaman (+0300), tutar, TRY.
4. **Yükle**: Dönüşümler > Yüklemeler > CSV (veya API). **90 gün** içinde olmalı.
5. **Doğrula**: Dönüşümler raporunda `booking_offline` görünür; "Yükleme tanılaması" hatasız olmalı.

## Notlar
- Zaman dilimi satırı (`Parameters:TimeZone=+0300;`) CSV'nin İLK satırı olmalı.
- GCLID yoksa o lead OCI ile yüklenemez; Meta tarafı için `meta-offline-capi.md` (hash'li eşleşme).
- KVKK: kişisel veriyi rıza ile sakla; CSV'de sadece GCLID + tutar yeterli (PII gerekmez).
