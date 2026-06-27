# 21 — Gerçek Hesap Verisiyle Kampanya Analizi & Yeniden Kurulum (27 Haz 2026)

Canlı Google Ads hesabı (Customer ID **648-937-2864**, "Kozbeyli Konağı") incelenerek
yapıldı — varsayım değil, **gerçek performans verisi**.

## Kök sorun (kritik): reklamlar reddediliyordu
Hesaptaki reklamlar **"Onaylanmadı — Çalışmayan hedef"** ile reddedilmişti. Sebep: final URL'ler
**ölü `kozbeylikonagi.com`** kabuğuna gidiyordu. Bizim sistemde de aynı hata vardı.
**Düzeltildi:** tüm reklam/uzantı URL'leri çalışan `www.kozbeylikonagi.com` + doğru yollara çekildi
(/rezervasyon /odalar /gastronomi /organizasyonlar /galeri /lokasyon). Bu tek başına reddi çözer.

## Gerçek kazananlar (hesaptan) → kelime setine işlendi
| Kelime | Tık | TO | Karar |
|---|---|---|---|
| foça konaklama | 562 | **%10,12** | Tut/öne çıkar |
| otel foça | 440 | **%9,99** | EKLENDİ |
| en uygun otel fiyatları | 266 | %12,22 | dikkatli (jenerik) |
| foça otelleri | yüksek | iyi | Tut |
| izmir (geniş) | 6.025 | **%2,13** | ₺5.481 boşa — geniş yok, negatif izmir-kombinasyonları |

Eklenen gerçek terimler: otel foça, eski foça otel(leri), foça kozbeyli, foça antik otel,
kozbeyli konağı yorum, yeni foça otelleri, foça merkez otel. Toplam 39 kelime (Phrase/Exact).

## Gerçek boşa-harcama (arama terimi madenciliği) → negatife alındı (57→90)
Hesabın arama terimlerinden alakasızlar: plaj/beach/koy/deniz, kamp/glamping/bungalow/orman,
gezilecek yerler, kordon/kemeraltı/seyir tepesi/bostanlı, başka şehirler (urla/manisa/bergama/
dikili/karaburun), öğretmenevi/sosyal tesis, **rakip isimleri** (gaia, saklı cennet, club med,
voodoo, kybele, palandız). Küçük bütçede negatif = en güçlü kaldıraç.

## Hesabın durumu (denetim)
7 kampanya, ~**₺70.700** ömür-boyu harcama. Sadece "Search / Foça Otel" aktif (onaysız reklamla),
diğerleri duraklatılmış ("reklam planı anahtar kelime" ₺18k ama %2,2 TO = zayıf; PMax ₺13,6k;
"Yeni Foça" ₺10,7k %2,7). Çoğu para zayıf-TO eski yapılarda harcanmış.

## Yeniden kurulum planı (eskiyi kapat, sadece yeni kalsın)
1. **Import:** `campaigns/google-editor/` CSV'lerini Google Ads Editor'e al — tümü **PAUSED**, URL'ler
   çalışıyor, kelimeler gerçek-veri, 90 negatif.
2. **Ölçüm doğrula:** GTM siteye kur (GA4 G-V3R66C3MEF + Ads AW-800024713 + Pixel/CAPI) → test
   rezervasyonuyla purchase'ı gör.
3. **Yenileri ENABLE et** (ikinci onay + guardrail), 1-2 hafta öğren.
4. **Eski 7 kampanyayı duraklat** — sadece yeni, temiz yapı kalsın.

## Maps + Organik #1 (doğru kelimelerle)
- **GBP sahiplen + doğrula** (en kritik Maps sinyali). NAP tek standart: docs/08, fixes/04.
- Maps/organik hedef kelimeler (gerçek arama hacmi): foça otel, foça konaklama, foça butik otel,
  eski foça otel, kozbeyli (marka). Bunları GBP açıklaması + kategorisi + gönderilerinde kullan.
- Yorum: **TripAdvisor 3.0 zayıf halka** → mutlu misafiri oraya yönlendir (Otelpuan 8.6/Yandex 4.3 iyi).
- Şema `.com`'da VAR (PostalAddress+Geo) — Rich Results ile tamamla. "kozbeyli" markasında #1 ulaşılabilir;
  jenerik "foça otel" organik #1 GARANTİ değil (Maps + reklam + içerikle güçlenir).

## Düzenli kontrol (schedule)
Haftalık otonom görev: arama terimi madenciliği → yeni negatif önerisi, kazanan kelimeye bütçe,
zayıf kampanyayı kıs. (kozbeyli-haftalik-kontrol görevine eklendi.)
