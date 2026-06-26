# 05 — Optimizasyon Playbook'u (Kurallar, Eşikler, Sezon)

Bu belge "kampanyaları açtıktan sonra ne yapacağız" sorusunun cevabıdır. Tüm
sayılar **planlama eşiğidir**, kanun değil; hesabın gerçek verisiyle güncellenir.
Altın kural: **önce ölçüm, sonra trafik, sonra optimizasyon.** Optimizasyon
blended (Google+Meta) CPA ve ROAS ile yapılır; tek platform metriğine takılma.

## 0. Optimizasyon kadansı
- **Günlük (2 dk):** harcama pacing + anomali (sıfır gösterim, ani CPA artışı).
- **Haftalık (20 dk):** `kads brief` → arama terimleri, negatifler, kreatif rotasyonu,
  teklif. Doluluk takvimine göre bütçeyi kaydır.
- **Aylık:** faz geçişi (marka → non-brand → Meta retargeting), teklif stratejisi.
- Aşırı düzenleme yapma: Meta'da saatte onlarca değişiklik işaretlenme riski (docs/04).

## 1. Google Search — karar kuralları

### Arama terimi madenciliği (en önemli kaldıraç)
- Haftalık arama terimi raporunu aç. Niyetsiz her terimi **negatif** yap
  (`campaigns/google-editor/05_negative_keywords.csv` listesini büyüt).
- Dönüşen yeni terimi ilgili reklam grubuna **exact** ekle.

### Teklif stratejisi geçişi
| Durum | Strateji |
|---|---|
| Ölçüm doğru, hesap yeni, veri yok | Maximize Clicks + CPC limiti (~6 TL) |
| Son 30 günde yeterli dönüşüm birikti | Maximize Conversions değerlendir |
| Net ekonomik hedef + geçmiş var | tCPA (keyfi değer girme) |
> "15 dönüşüm/30 gün" zorunluluk değil, güçlü tavsiyedir. Eşik dolmadan tCPA'ya geçme.

### Reklam grubu sağlığı
- CTR düşükse (< %2 non-brand): başlık/uzantı testi; alaka düşükse keyword'ü daralt.
- Marka CTR genelde yüksek (> %8); düşükse açılış sayfası uyumunu kontrol et.
- Quality Score düşük keyword → açılış sayfası + reklam alaka + beklenen CTR üçlüsü.

### Bütçe
- Marka her zaman dolu beslenir (en yüksek CVR, OTA savunması).
- Non-brand'i arama terimi temizlenene kadar **dar** tut. Test kampanyası küçük kalsın.

## 2. Meta — karar kuralları

### Öğrenme aşaması
- Ad set haftada ~50 optimizasyon olayına ulaşmalı (öğrenmeden çıkış). Bütçeyi çok
  sayıda küçük ad sete bölme; **tek ad set, 3-4 kreatif** ile başla.
- İlk ay ≤ 2 kampanya, ikinci ay ≤ 3 kampanya.

### Kreatif testi
- Aynı görselin sadece metnini değil, **farklı hikâyeyi** test et (4 konsept hazır:
  `campaigns/meta/meta-reklam-metinleri.csv`).
- Yorgun kreatif sinyali: sıklık (frequency) > 2.5 + CTR düşüşü → kreatifi yenile.

### Optimizasyon olayı seçimi
- Purchase güvenilirse → Website Sales / Purchase.
- Purchase güvenilmezse → önce `begin_checkout` veya `Lead`; WhatsApp akışını çalıştır.
- Retargeting yalnızca site/IG kitlesi dolunca açılır.

### WhatsApp kalite
- Nitelikli lead'i ölç (tarih + kişi sayısı veren). Bot/spam'i filtrele.
- `Maksimum CPL = rezervasyon CPA × (lead→rezervasyon oranı)`.
  Örnek: CPA 2.000 TL, kapanış %15 → maksimum CPL 300 TL. CPL bunu aşarsa daralt.

## 3. Doluluk-duyarlı harcama (16 oda kısıtı)
Otelin envanteri sınırlı; reklamın işi **boş geceleri** doldurmak.
- **Dolu tarihlerde** harcamayı kıs (o tarihlere reklam = israf). HMS doluluk takvimini
  haftalık kontrol et.
- **Boş/düşük dönemlere** bütçeyi yönlendir; Meta'da tarih-temalı mesaj ("bu hafta birkaç oda").
- Son dakika boşluk → WhatsApp/retargeting'i artır (en hızlı dönüş).

## 4. Sezon
- **Yüksek sezon (Haz–Eyl):** talep yüksek; marka tabanını koru, non-brand'de CPC artışına
  hazır ol, dolu tarihlerde kısma kuralını sıkı uygula.
- **Düşük sezon (Kas–Mar):** dar non-brand'i kıs; marka + retargeting + içerik/WhatsApp ile
  doğrudan talebi besle. Hafta içi sakin kaçış mesajı bu dönemde güçlü.
- **Geçiş (Nis–May, Eki):** balayı/çift, evcil dostu, köy kahvaltısı temalarını öne çıkar.

## 5. Eşik tablosu (başlangıç; veriyle güncelle)
| Metrik | İzle | Aksiyon eşiği (öneri) |
|---|---|---|
| Blended ROAS | Haftalık | < 2x → kıs/optimize; ≥ 3x → ölçekle |
| Blended CPA | Haftalık | Rezervasyon CPA hedefini (örn. 2.000 TL) aşarsa daralt |
| Non-brand CTR | Haftalık | < %2 → başlık/keyword revizyonu |
| Meta frequency | Haftalık | > 2.5 → kreatif yenile |
| Marka pay (impression share) | Aylık | Düşükse marka bütçesini artır |
| Arama terimi israfı | Haftalık | Niyetsiz terim → negatif |

## 6. Değişiklik güvenliği
Her mutation `kads guard` / `scripts/guardrails.py` ve `/kozbeyli-ads-change`
üzerinden gider: allowlist + PAUSED + bütçe tavanı + açık onay + ENABLE için ikinci
onay + audit log. Optimizasyon "hızlı" olabilir ama **kontrolsüz** olamaz (docs/04).
