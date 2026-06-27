"""Gercek tarayici (Playwright/chromium) ile pano dogrulama: sayfa render olur,
<title> dolu, 'Kozbeyli' icerigi gelir, KONSOL HATASI yok. Browser yoksa skip."""
from pathlib import Path
import pytest

pytest.importorskip("playwright")
from playwright.sync_api import sync_playwright  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
PAGES = ["dashboard/kontrol-merkezi.html", "dashboard/rapor.html", "b2b/sell-sheet.html"]


def _browser_available() -> bool:
    try:
        with sync_playwright() as p:
            p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage"]).close()
        return True
    except Exception:
        return False


pytestmark = pytest.mark.skipif(
    not _browser_available(),
    reason="Playwright chromium baslatilamadi (lokal sistem lib eksik); CI'da --with-deps ile calisir",
)


@pytest.mark.parametrize("rel", PAGES)
def test_dashboard_renders_clean(page, rel):
    errors = []
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto((ROOT / rel).as_uri())
    assert page.title().strip(), f"{rel}: bos <title>"
    assert "Kozbeyli" in page.content(), f"{rel}: icerik render olmadi"
    assert errors == [], f"{rel}: konsol/sayfa hatasi -> {errors[:3]}"
