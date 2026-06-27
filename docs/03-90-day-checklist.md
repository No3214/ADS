# 03 — 90 Günlük Uygulama Kontrol Listesi ("Önce Ölçüm, Sonra Trafik")

Bütçe: Google 15.000 TL/ay + Meta 15.000 TL/ay = 30.000 TL/ay.
Kural: Tag'ler test rezervasyonuyla doğrulanmadan hiçbir kampanya `ENABLED` yapılmaz.

## Hafta 1–3 — ÖLÇÜM (henüz trafik yok)
- [ ] GTM container'ı belirle (docs/02) ve `.env` + `config` güncelle.
- [ ] `ConsentAndGtm.tsx`'i `app/layout.tsx`'e ekle; Consent Mode v2 default denied.
- [ ] GTM içinde GA4 (`G-V3R66C3MEF`), Google Ads (`AW-800024713`, Satın alma), Meta
      Pixel (`1781546559309505`) etiketlerini kur.
- [ ] Çapraz alan: GA4'e `kozbeylikonagi.com` + `hmshotel.net`; `hmshotel.net`
      istenmeyen yönlendirmelere.
- [ ] HMS desteğine 6 soruyu sor (docs/01); gerçek otel slug'ını ve onay sayfası
      davranışını öğren.
- [ ] Dönüşüm aksiyonları: `purchase` (transaction_id), `generate_lead`. Google Ads–GA4
      bağlantısı + Enhanced Conversions.
- [ ] Meta Pixel + CAPI; `Purchase`/`InitiateCheckout`/`Lead` aynı event_id.
- [ ] TEST REZERVASYONU ile doğrula (docs/01, 5 madde). Geçmeden devam etme.

## Hafta 3–5 — Marka Search (Google)
- [ ] `config` → `write_guardrails.enabled: true`, `.env` → `ADS_WRITES_ENABLED=true`.
- [ ] Allowlist'i gerçek ID'lerle doldur (Meta `act_...`, Google 10 hane).
- [ ] Marka kampanyası PAUSED hazırla (Maximize Clicks veya düşük CPC limiti).
- [ ] Hesap düzeyi negatif liste + uzantılar (assets/google-rsa-tr.yaml).
- [ ] guardrails.py'den ALLOW al → açık onay → kampanyayı yayına al.
- [ ] Düşük günlük taban: ~148 TL/gün (4.500 TL/ay).

## Hafta 4–6 — Meta başlangıç (2 kampanya)
- [ ] Prospecting (Website Sales) 10.500 TL/ay; YALNIZCA Purchase güvenilirse.
- [ ] WhatsApp/Mesaj 4.500 TL/ay (tracking hazır değilse önce SADECE bu).
- [ ] 4+ kreatif konsepti (assets/meta-creative-concepts-tr.md); Reels/Stories 9:16, Feed 4:5.

## Hafta 5–8 — Dar non-brand Search (Google)
- [ ] 6–8 yüksek niyetli anahtar kelime, tam/öbek eşleme.
- [ ] İzmir/Foça çevresi + büyük şehir kaynak hedeflemesi; coğrafi daraltma.
- [ ] Arama terimi raporunu izle; negatifleri büyüt. ~296 TL/gün (9.000 TL/ay).

## Hafta 8–12 — Meta retargeting + optimizasyon
- [ ] Meta retargeting 3.000 TL/ay (liste dolunca). Prospecting 9.000, WhatsApp 3.000.
- [ ] Teklif geçişi: kampanyada son 30 günde yeterli dönüşüm birikince Maximize
      Conversions/Target CPA değerlendir (eşikler tavsiye niteliğinde; bkz. plan notu).
- [ ] Google remarketing AÇILMAZ (retargeting Meta'da).

## Şimdi AÇMA (ertelenenler)
- [ ] PMax / Performance Max for travel, görüntülü prospecting, video. Marka + dar
      non-brand + Meta retargeting doygunluğa ulaşıp veri birikene kadar bekleyin.
- [ ] Not: Hotel Ads komisyon tabanlı teklif yeni kampanyalar için kaldırıldı; alternatifler
      (tROAS, Performance Max for travel) HMS'in canlı fiyat/müsaitlik feed'ini gerektirir.

## Sürekli
- [ ] Dolu olduğunuz tarihlerde harcamayı kıs, boş dönemlere yönlendir (16 oda kısıtı).
- [ ] Yüksek sezon Haz–Eyl: marka tabanını koru. Düşük sezon Kas–Mar: dar non-brand'i kıs.
- [ ] Haftalık: blended CPA + blended ROAS (yalnız platform metriği değil).
