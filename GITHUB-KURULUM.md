# GitHub'a Yükleme — github.com/No3214/ADS

Her şey hazır ve commit'lendi (temiz, secret yok). Push için **senin GitHub kimliğin**
gerekiyor — güvenlik gereği token'ı sohbete yazmıyoruz; aşağıdaki adımları **kendi
bilgisayarında** çalıştır (Windows'ta Git, OneDrive klasöründe sorunsuz çalışır).

## Önce: repo var mı?
`https://github.com/No3214/ADS` şu an **404** veriyor (yok ya da özel). Push'tan önce:
- GitHub'da **New repository → ad: ADS** (boş; README ekleme) oluştur, **veya**
- Repo özelse, o hesapla giriş yaptığından emin ol.

## Yol A — Tek tık (önerilen)
Klasördeki **`push.bat`** (Windows) dosyasına çift tıkla. Şunları yapar:
1. Bozuk/eski `.git` varsa siler. 2. `git init` + tüm dosyaları ekler (`.env`/`logs` hariç).
3. Commit'ler. 4. `origin = No3214/ADS` ayarlar. 5. `git push` — tarayıcıda GitHub girişi açılır.

## Yol A — Elle (aynısı)
Klasörde bir terminal aç ve sırayla:
```bash
rmdir /s /q .git            REM (Windows) bozuk .git'i sil  —  mac/linux: rm -rf .git
git init -b main
git add -A
git commit -m "feat: kads v1.0 — Kozbeyli Konagi reklam & dijital operasyon sistemi"
git remote add origin https://github.com/No3214/ADS.git
git push -u origin main
```
İlk push'ta GitHub kimlik doğrulaması ister: **tarayıcıdan giriş** (Git Credential Manager)
veya kişisel erişim anahtarı (PAT) — anahtarı **sohbete değil**, sadece git'in sorduğu
pencereye gir.

## Yol B — Bundle'dan (alternatif, geçmişiyle birlikte)
Klasörde `ADS.bundle` var (tüm commit geçmişini taşır). Temiz bir kopya istersen:
```bash
git clone ADS.bundle ADS-temiz
cd ADS-temiz
git remote set-url origin https://github.com/No3214/ADS.git   REM yoksa: git remote add origin ...
git push -u origin main
```

## Doğrulama
Push sonrası GitHub'da: 65+ dosya, README rozetleri, `kads/`, `campaigns/`, `docs/00-09`,
`dashboard/`, `tests/`, CI (`.github/workflows/ci.yml`) görünür. Actions sekmesinde
testler yeşil olmalı.

## Notlar
- `.env` ve `logs/` **bilerek** gönderilmez (`.gitignore`). Token/secret repoya girmez.
- Repoyu **özel (private)** tutman önerilir (reklam/iş verisi).
