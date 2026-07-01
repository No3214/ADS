"""Ölçüm (tracking) + domain/keyword regresyon kilitleri."""

import json
from pathlib import Path

from kads import core, data
from kads import data_ext as dx
from kads.cli import main

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
    assert "1781546559309505" in blob  # Meta Pixel
    assert "G-V3R66C3MEF" in blob  # GA4
    assert "AW-800024713" in blob  # Google Ads


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
            assert "kozbeylikonagi.com.tr" not in f.read_text(
                encoding="utf-8"
            ), f"{f} .com.tr"


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


# ---- doğrulanmamış mesafe iddiası: müşteriye dönük "13 km" asla -------------
def test_no_unverified_distance_in_customer_copy():
    """13 km DOĞRULANMADI (MEB: Yeni Foça ~10 km). Reklam/GBP/OTA/şema metninde
    sabit yanlış mesafe = uyum/itibar riski. Sadece iç denetim docs/ hariç."""
    targets = ["campaigns", "profiles", "fixes", "aeo"]
    src = ["kads/data/__init__.py", "kads/data_ext.py", "kads/seo.py", "kads/presence.py"]
    bad = []
    for d in targets:
        p = ROOT / d
        if not p.exists():
            continue
        for f in p.rglob("*"):
            if f.suffix in {".md", ".csv", ".json", ".jsonld", ".txt", ".html"} and "13 km" in f.read_text(encoding="utf-8"):
                bad.append(str(f.relative_to(ROOT)))
    for s in src:
        if "13 km" in (ROOT / "kads" / Path(s).name).read_text(encoding="utf-8"):
            bad.append(s)
    assert not bad, f"doğrulanmamış '13 km' müşteri metninde: {bad}"


def test_brand_rsa_pinned_to_position_one():
    """Marka kampanyasında marka adı 1. pozisyona sabit (OTA savunması)."""
    from kads.platforms import google as _g
    marka = [r for r in _g.rsa_rows() if r["Ad Group"] == "Marka"]
    assert marka, "Marka RSA yok"
    r = marka[0]
    assert r.get("Headline 1 position") == 1 and r.get("Headline 2 position") == 1
    assert "Kozbeyli" in r["Headline 1"]


# ---- kads deliver: reklam teslim paketi durumu ------------------------------
def test_deliver_ok():
    assert main(["deliver"]) == core.EX_OK


def test_deliver_json_pipe_clean(capsys):
    rc = main(["deliver", "--format", "json"])
    assert rc == core.EX_OK
    out = capsys.readouterr().out.strip()
    assert out and out[0] == "[", "json banner ile kirlenmemeli"
    json.loads(out)


def test_delivery_status_structure():
    assert len(dx.DELIVERY_STATUS) == 9  # #2..#10
    cols = {"no", "baslik", "durum", "konum", "aksiyon"}
    for r in dx.DELIVERY_STATUS:
        assert cols <= set(r.keys())
    d = {r["no"]: r["durum"] for r in dx.DELIVERY_STATUS}
    assert d["#5"] != "HAZIR", "Tracking kalemi ölçüm-bekliyor işaretli olmalı"
    assert d["#10"] != "HAZIR", "30 gün planı ölçüm-kapısı işaretli olmalı"


def test_deliver_package_doc_exists():
    assert (ROOT / "docs" / "REKLAM-TESLIM-PAKETI.md").exists()


def test_ads_delivery_skill_valid():
    """skills/ads-delivery/SKILL.md var ve name/description frontmatter'ı geçerli."""
    p = ROOT / "skills" / "ads-delivery" / "SKILL.md"
    assert p.exists(), "SKILL.md yok"
    txt = p.read_text(encoding="utf-8")
    assert txt.startswith("---"), "YAML frontmatter yok"
    fm = txt.split("---", 2)[1]
    assert "name: ads-delivery" in fm
    assert "description:" in fm
    # gövde teslim paketini referans almalı
    assert "REKLAM-TESLIM-PAKETI.md" in txt and "kads deliver" in txt
