# 23 — Meta Pixel Canlı Denetimi (tarayıcı, Haz 2026)

Yöntem: `www.kozbeylikonagi.com` canlı tarayıcıda; fbq durumu + `facebook.com/tr/` beacon'ları
3 sayfada okundu (ana, /odalar, /rezervasyon). Tahmin yok — gerçek ağ kanıtı.

## ÇALIŞAN (doğru kurulmuş — dokunma)
- **Tek pixel: `1781546559309505`** — duplicate YOK, tek `fbevents.js`, sürüm 2.9.346, `fbp` çerezi var.
- **PageView** her sayfada ateşliyor (ana, odalar, rezervasyon).
- **InitiateCheckout** `/rezervasyon`'da ateşliyor (`ev=InitiateCheckout`, ec=1) — rezervasyon-başlangıcı Meta'ya gidiyor. İyi.

## EKSİK / DÜZELTİLECEK (öncelik sırası)

**1. Purchase (tamamlanan rezervasyon) YOK — en kritik.**
InitiateCheckout var ama gerçek rezervasyon **hmshotel.net** (ayrı domain) üzerinde tamamlanıyor; pixel
muhtemelen orada YOK → Meta "rezervasyona başladı"yı görüyor, "rezervasyon tamamlandı"yı GÖRMÜYOR. Optimizasyon
ve ROAS bu yüzden kör. **Fix:** HMS onay/teşekkür sayfasına pixel + `Purchase` (value+currency ile). Hazır:
`tracking/hms-confirmation-snippet.html`. HMS şablon düzenleme erişimi gerekir.

**2. Automatic Advanced Matching KAPALI — ücretsiz, 1 tık.**
Beacon'larda `ud[...]` kullanıcı-verisi parametresi yok → AM kapalı. Events Manager → Veri kaynakları →
pixel → Ayarlar → **Automatic Advanced Matching: AÇ.** Eşleşme oranını ve atfı artırır, bedava.

**3. Conversions API (CAPI) yok — önerilir (iOS/adblock dayanıklılığı).**
Sadece tarayıcı-pixel (`cdl=API_unavailable`). Sunucu-taraflı CAPI + event dedup (eventID) ileride. Hazır
şablon: `tracking/implementation/05-meta-capi-route.ts`. Bütçe kısıtlıysa 1-2'den sonra gelir.

**4. ViewContent oda sayfalarında yok — orta.**
`/odalar`'da sadece PageView. Oda detay sayfalarına `ViewContent` (content_ids + value) → retargeting/katalog
ve "oda gezip rezerve etmeyen" kitlesi için. 

**5. InitiateCheckout'ta value/currency yok — küçük.**
`ev=InitiateCheckout` parametresiz. `value` + `currency: TRY` eklenirse değer-bazlı optimizasyon açılır.

**6. Consent API `API_unavailable` — KVKK kontrolü.**
Her beacon'da `cdl=API_unavailable`: consent mode pixel'e bağlı değil. Pixel yine de atıyor; KVKK/consent
doğruluğu için consent sinyalini pixel'e bağla (repo: Consent Mode v2 hazır, `tracking/implementation/01-consent-mode-v2.html`).

## Özet
Pixel TABANI doğru (tek pixel, PageView + InitiateCheckout çalışıyor) — "yanlış kurmuş olabilirim" endişen
büyük ölçüde yersiz. Asıl boşluk **Purchase (HMS onay sayfası)** ve **Advanced Matching (1 tık, bedava)**.
Bu ikisi tamamlanınca Meta hunisi uçtan uca ölçülür. Google tarafıyla aynı desen: niyet ölçülüyor, tamamlanma değil.
