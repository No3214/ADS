@echo off
title Kozbeyli ADS - GitHub Push
cd /d "%~dp0"

echo ===================================================
echo   Kozbeyli ADS  -^>  github.com/No3214/ADS
echo ===================================================
echo.

where git >nul 2>nul
if errorlevel 1 goto nogit

if exist ".git" rmdir /s /q ".git"

git init -b main
git config user.name "Yunuscan Oruk"
git config user.email "yunuscanoruk@gmail.com"
git add -A
git commit -m "kads - Kozbeyli Konagi reklam ve dijital operasyon sistemi"
if errorlevel 1 goto nocommit

git remote remove origin >nul 2>nul
git remote add origin https://github.com/No3214/ADS.git

echo.
echo PUSH basliyor. Ilk kez ise GitHub giris penceresi acilabilir, giris yap.
echo.
git push -u origin main --force
if errorlevel 1 goto pushfail

echo.
echo ============== BASARILI ==============
echo   https://github.com/No3214/ADS
git ls-remote --heads origin
goto end

:nogit
echo.
echo  HATA: git kurulu degil.
echo  Kur: https://git-scm.com/download/win  (Git Credential Manager secili kalsin)
echo  Kurduktan sonra bu dosyayi tekrar calistir.
goto end

:nocommit
echo.
echo  HATA: commit olusmadi (klasorde dosya yok mu?).
goto end

:pushfail
echo.
echo  HATA: push basarisiz. Muhtemel sebep:
echo   - Giris yapilmadi: acilan pencerede GitHub'a giris yap, tekrar calistir.
echo   - "Permission denied" / 403: No3214 hesabiyla giris yapmalisin.
echo   - En kolay yol: GitHub Desktop  https://desktop.github.com
goto end

:end
echo.
echo Bu pencere kapanmayacak. Sonucu/ustteki HATA satirini oku.
pause
