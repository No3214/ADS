"""Ölçüm (tracking) + domain/keyword regresyon kilitleri."""
import json
from pathlib import Path
from kads.cli import main
from kads import core, data
from kads import data_ext as dx

ROOT = Path(__file__).resolve().parents[1]


# ---- kads tracking komutu ---------------------------------------------------
def test_tracking_ok():
    assert main(["tracking"]) == core.EX_OK


def test_tracking_json_ok():
    assert main(["tracking", "--format", "json"]) == core.EX_OK


def test_tracking_json_pipe_clean(capsys):
    rc = main(["tracking", "--format", "json"])
    assert rc == core.EX_OK
    out = capsys.readouterr().out.strip()
    assert out and out[0] in "[{", "json banner ile kirlenmemeli"
    json.loads(out)  # geçerli JSON


def test_tracking_state_structure():
    assert len(dx.TRACKING_STATE) >= 8
    cols = {"bilesen", "durum", "detay", "aksiyon"}
    for r in dx.TRACKING_STATE:
        assert cols <= set(r.keys())
    blob = " ".join(r["bilesen"] for r in dx.TRACKING_STATE)
    assert "GTM-KCG6B4MJ" in blob
    assert "1781546559309505" in blob          # Meta Pixel
    assert "G-V3R66C3MEF" in blob              # GA4
    assert "AW-800024713" in blob              # Google Ads


def test_tracking_state_valid_status():
    allowed = {"CANLI", "EKSİK", "KAPALI", "ATIYOR", "YOK"}
    for r in dx.TRACKING_STATE:
        assert r["durum"] in allowed, r["durum"]


# ---- domain regresyonu: .com.tr asla geri gelmesin --------------------------
def test_no_hotel_comtr_in_source():
    for mod in ("data/__init__.py", "data_ext.py", "seo.py", "presence.py"):
        txt = (ROOT / "kads" / mod).read_text(encoding="utf-8")
        assert "kozbeylikonagi.com.tr" not in txt, f"{mod} .com.tr içeriyor"


def test_no_hotel_comtr_in_campaigns():
    camp = ROOT / "campaigns"
    if camp.exists():
        for f in camp.rglob("*.csv"):
            assert "kozbeylikonagi.com.tr" not in f.read_text(encoding="utf-8"), f"{f} .com.tr"


def test_final_url_is_dotcom():
    # data_ext final_url(ler) .com olmalı (.com.tr değil)
    txt = (ROOT / "kads" / "data_ext.py").read_text(encoding="utf-8")
    assert "www.kozbeylikonagi.com/" in txt


# ---- bölge kelimeleri (Yeni Foça) -------------------------------------------
def test_region_keywords_present():
    terms = {t for g in data.KEYWORDS.values() for t in g["terms"]}
    for kw in ("yeni foça otel", "yeni foça konaklama", "kozbeyli foça"):
        assert kw in terms, f"bölge kelimesi eksik: {kw}"


# ---- config ölçüm alanları --------------------------------------------------
def test_config_tracking_fields():
    cfg = (ROOT / "config" / "ads-assets.yaml").read_text(encoding="utf-8")
    assert "gtm_status:" in cfg
    assert "measurement_gap:" in cfg
    assert "GTM-KCG6B4MJ" in cfg
