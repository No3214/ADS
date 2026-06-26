# 17 — Sağlamlık, Self-Check ve Otonomi (kırılmaz sistem)

Hedef: kusursuza yakın, kendini denetleyen, kolay toparlanan bir sistem. Dürüst sınır: Claude
oturum-tabanlıdır (7/24 kendi başına çalışmaz); "otonomi" = çağrıldığında tam çalışır + tekrar
eden işler **zamanlanmış görevle** otomatikleşir. Aşağıdakiler sistemi "kırılmaz"a yaklaştırır.

## Neden sağlam
- **Deterministik çekirdek:** tek kaynak (`kads/data.py` + `data_ext.py`); aynı girdi → aynı çıktı.
- **Sıfır bağımlılık:** kads stdlib ile çalışır; kurulum kırılganlığı yok.
- **Guardrail (kod seviyesinde):** para harcayan işlemler allowlist + PAUSED + bütçe tavanı + onay
  + audit log. Prompt enjeksiyonu bunu atlayamaz (`scripts/guardrails.py`).
- **Testler + CI:** pytest (55+) her değişiklikte; GitHub Actions otomatik koşar.
- **Yedek:** `ADS.bundle` (tüm geçmiş) + GitHub (`push.bat`). Tek dosyadan tam geri yükleme.

## Self-check (kendini denetleyen)
`kads selfcheck` — bütünlük denetimi: RSA uzunluk, bütçe=plan, JSON-LD + manifest geçerli, üretim
(CSV/şema), 20 paket mevcut, guardrails + yedek. Çıkış 0 = sağlam, 1 = sorun. Haftalık veya her
değişiklikten sonra çalıştır. `kads doctor` (ortam/kimlik) + `kads status` (paket/hazırlık) tamamlar.

## Toparlanma (recovery)
- Bozulan dosya/klasör → bundle'dan geri al: `git clone ADS.bundle geri && ...`.
- Bozuk .git (OneDrive) → `push.bat` fresh init + force (PUSH-SORUN.md).
- Yanlış değişiklik → git geçmişinden geri al; selfcheck ile doğrula.

## Kendini iyileştirme (öğrenme)
- `memory/learnings.md`: tekrarlayan hata/karar/öğrenmeyi yaz → sistem zamanla iyileşir
  (agentic-core self-improve deseni). Kural ekle, selfcheck'e kontrol ekle.

## Gerçek otonomi (zamanlanmış)
- Tekrar eden işler için **zamanlanmış görev**: haftalık rakip/yorum izleme (Apify) + rapor;
  aylık B2B prospecting brief; sezon başı bütçe/teklif güncelleme. (Cowork scheduled tasks.)
- İnsan-onay kapısı korunur: para/yazma işlemleri her zaman guardrail + açık onaydan geçer.

## Kapsam (tüm işler tek sistem)
Otel (B2C turizm) · Restoran · Organizasyon/düğün (B2C) · **B2B kurumsal (Aliağa sanayi)** —
hepsi aynı kads + içerik paketleriyle yönetilir. Bağlantılı: reklam, SEO/AEO, sosyal, e-posta,
WhatsApp, izleme, finans, frontend. `kads help` tüm komutlar; `BASLA.md` başlangıç.
