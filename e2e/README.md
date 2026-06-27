# e2e/ — Playwright tarayıcı testleri (pano/HTML)

Varsayılan `pytest` suite'inin DIŞINDA (hızı bozmasın). Gerçek Chromium ile panoları
(kontrol-merkezi, rapor, sell-sheet) yükler, render + konsol-hatası kontrolü yapar.

## Çalıştırma
```
pip install pytest-playwright
python -m playwright install --with-deps chromium   # CI/Linux: sistem lib'leri dahil
pytest e2e/
```
Tarayıcı başlatılamazsa testler **skip** olur (suite kırılmaz). Browsersiz statik HTML
doğrulaması `tests/test_dashboards_html.py` her yerde çalışır.
