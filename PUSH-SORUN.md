# Push olmadı mı? (repo var ama boş)

Repo `github.com/No3214/ADS` **var ve public**, ama **boş** görünüyor → dosyalar yüklenmemiş.
Sebep neredeyse her zaman ikisinden biri:

## 1) git kurulu değil
`git-scm.com/download/win` → kur (Credential Manager seçili kalsın) → `push.bat`'ı tekrar çalıştır.

## 2) GitHub girişi (auth) tamamlanmadı
`git push` ilk kez çalışınca tarayıcıda GitHub girişi ister. Giriş yapmadıysan push durur.
Çözüm: `push.bat`'ı tekrar çalıştır, açılan pencerede giriş yap.

## En kolay yol (kod yok): GitHub Desktop
1. https://desktop.github.com indir + kur, GitHub hesabınla giriş yap.
2. File > Add local repository > bu klasörü seç (`kozbeyli-ads-claude-starter-v3`).
3. "Publish repository" / "Push origin" → No3214/ADS.
   (Repo zaten var; "Publish" yerine mevcut remote'a push de olur.)

## Alternatif: bundle'dan
Klasörde `ADS.bundle` var (tüm geçmiş). Başka makinede/temizde:
`git clone ADS.bundle ADS && cd ADS && git remote add origin https://github.com/No3214/ADS.git && git push -u origin main --force`

## Doğrulama
Push sonrası: `git ls-remote --heads origin` çıktı vermeli; GitHub'da dosyalar görünür.
Olmazsa `push.bat`'ın son satırlarını (hata mesajı) bana ilet.
