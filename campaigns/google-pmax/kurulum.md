# Performance Max (PMax) Kurulum — Kozbeyli Konağı

PMax tek kampanyada tüm Google envanterini kullanır (Search + Display + YouTube +
Discover + Gmail + Maps). `kads pmax`, `kads pmax specs`, `kads pmax setup`.

## Ön koşul (ZORUNLU)
- Dönüşüm akışı kurulu olmalı: `purchase` + `generate_lead` Google Ads'e gelmeli
  (bkz. tracking/). PMax dönüşüme göre öğrenir; dönüşüm yoksa para yakar.
- Bütçe guardrail tavanına uymalı (scripts/guardrails.py): Google günlük ≤ 493 TL.

## Koruma kuralları (küçük bütçe + marka koruması)
1. **Brand exclusions** ekle → PMax marka aramalarını ucuza yazıp raporu şişirmesin.
2. **Final URL expansion KAPALI** (başta) → mevcut Search trafiğini çalmasın.
3. Ayrı **Marka Search** kampanyası açık kalsın (savunma).
4. PMax'i ay 2-3'te aç; önce Search + Meta otursun (docs/05).

## Adımlar
1. Yeni kampanya → **Performance Max**. Hedef: Satışlar / Potansiyel müşteri.
2. Dönüşim hedefi: rezervasyon (purchase) + WhatsApp/form (generate_lead).
3. Her tema için **1 asset group** (asset-group-spec.csv'deki 4 grup).
4. Her gruba: başlık/açıklama (CSV), 3+ yatay + 3+ kare + 1+ dikey görsel, logo, video.
5. **Kitle sinyali** (audience signal): kendi listelerin (site ziyaretçi, CRM) + ilgi.
6. Bütçe + 2-4 hafta öğrenme; erken kapatma.
7. 2 hafta sonra: arama terimleri (Insights), asset performansı (Low → değiştir).

## Varlık limitleri
`kads pmax specs` (özet): başlık ≤30 (8-15 adet), uzun başlık ≤90 (3-5),
açıklama ≤90 (4-5; 1 adet ≤60), işletme adı ≤25, görseller 1.91:1 + 1:1 + 4:5, logo, video ≥10sn.
