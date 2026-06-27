"""Dashboard/HTML statik dogrulama — yalniz stdlib (browsersiz; sandbox/Windows/CI her yerde).
Gercek tarayici e2e (konsol hatasi vs.) ayri: tests/e2e/. Bu katman HTML iskeleti + <title> +
anahtar icerik + sell-sheet'te kanonik NAP + sahte-puan yoklugu garanti eder."""
from html.parser import HTMLParser
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "dashboard/kontrol-merkezi.html": ["Kozbeyli"],
    "dashboard/rapor.html": ["Kozbeyli"],
    "b2b/sell-sheet.html": ["Kozbeyli Konağı", "Küme Evler No:188", "+90 532 234 2686"],
    "creatives/storyboard.html": [],
}


class _V(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = set(); self.titles = 0; self._in_title = False; self.title_text = ""
    def handle_starttag(self, t, a):
        self.tags.add(t)
        if t == "title":
            self._in_title = True; self.titles += 1
    def handle_endtag(self, t):
        if t == "title":
            self._in_title = False
    def handle_data(self, d):
        if self._in_title:
            self.title_text += d


@pytest.mark.parametrize("rel,must", list(PAGES.items()))
def test_html_valid_and_content(rel, must):
    p = ROOT / rel
    assert p.exists(), f"sayfa yok: {rel}"
    html = p.read_text(encoding="utf-8")
    v = _V(); v.feed(html)  # parse hatasi -> exception = test fail
    for skel in ("html", "head", "body", "title"):
        assert skel in v.tags, f"{rel}: <{skel}> eksik"
    assert v.titles >= 1 and v.title_text.strip(), f"{rel}: <title> bos"
    for m in must:
        assert m in html, f"{rel}: beklenen icerik yok -> {m}"


def test_sell_sheet_canonical_nap():
    html = (ROOT / "b2b/sell-sheet.html").read_text(encoding="utf-8")
    assert "Kozbeyli Köyü, Küme Evler No:188, 35680 Foça / İzmir" in html


def test_dashboards_no_fake_rating():
    # Durustluk: panolarda/sell-sheet'te sahte yildiz/puan/odul olmamali
    for rel in ("b2b/sell-sheet.html", "dashboard/kontrol-merkezi.html"):
        low = (ROOT / rel).read_text(encoding="utf-8").lower()
        for bad in ("★★★", "5/5 yıldız", "ödüllü otel", "ratingvalue"):
            assert bad not in low, f"{rel}: sahte puan/odul izi -> {bad}"
