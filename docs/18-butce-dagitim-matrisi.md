# 18 — Bütçe Dağıtım Matrisi (30.000 TL/ay)

`kads allocate` · `kads allocate funnel` · `kads allocate rules`. PLAN ile tutarlı;
ay1 (lansman, retargeting kapalı) ve ay2+ (oturmuş, retargeting açık) ayrı ayrı 30.000 TL.

## Kanal × huni × ay
| Kanal | Huni | Ay1 | Ay2+ | Gerekçe |
|---|---|---:|---:|---|
| Meta Prospecting | TOF/MOF | 10.500 (35%) | 9.000 (30%) | Yeni talep; ay2'de retargeting'e yer aç |
| Meta Retargeting | BOF/Retention | 0 | 3.000 (10%) | Liste min boyuta gelince (ay2+) |
| Meta WhatsApp | BOF | 4.500 (15%) | 3.000 (10%) | Nitelikli rezervasyon görüşmesi |
| Google Non-brand Search | MOF/BOF | 9.000 (30%) | 9.000 (30%) | Yüksek niyetli yeni talep |
| Google Marka Search | BOF | 4.500 (15%) | 4.500 (15%) | Marka + OTA savunması |
| Google Test → Demand Gen | TOF/test | 1.500 (5%) | 1.500 (5%) | Ay1 terim testi; ay2 Demand Gen |
| **Toplam** | | **30.000** | **30.000** | Google 15k + Meta 15k |

## Huni görünümü (ay2+)
TOF Farkındalık 35% · MOF Değerlendirme 30% · BOF Dönüşüm 25% · Retention 10%.

## Yeniden dağıtım kuralları (`kads allocate rules`)
- Kanal ROAS > 3x blended (2 hafta) → +%20 bütçe (test/zayıftan al).
- Kanal CPA > 1.5x hedef (2 hafta) → −%30 veya duraklat.
- Retargeting listesi dolu + ay2 → %10 ayır.
- Sezon: yüksek → marka koru/indirimi kıs; düşük → WhatsApp+retargeting+içeriğe kaydır (docs/19).
- Günlük tavanı aşma: Google 493 / Meta 500 TL/gün (guardrails.py).
