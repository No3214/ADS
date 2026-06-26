"""kads veri + uretim testleri."""
import json
from pathlib import Path
from kads import data, seo, presence
from kads.platforms import google as gx
from kads.platforms import meta as mx


def test_rsa_lengths():
    for grp, a in data.RSA.items():
        assert len(a["headlines"]) == 15, f"{grp} 15 başlık olmalı"
        assert len(a["descriptions"]) == 4, f"{grp} 4 açıklama olmalı"
        for h in a["headlines"]:
            assert len(h) <= 30, f"başlık >30: {h!r} ({len(h)})"
        for d in a["descriptions"]:
            assert len(d) <= 90, f"açıklama >90: {d!r} ({len(d)})"


def test_budget_caps_match_plan():
    assert data.BUDGET_CAPS["google_monthly_try"] == data.PLAN["google_monthly_try"]
    assert data.BUDGET_CAPS["meta_monthly_try"] == data.PLAN["meta_monthly_try"]
    assert data.PLAN["total_monthly_try"] == 30000


def test_keywords_and_negatives():
    total = sum(len(s["terms"]) for s in data.KEYWORDS.values())
    assert total >= 25
    assert len(data.NEGATIVES) >= 30
    assert len(data.NEGATIVES) == len(set(data.NEGATIVES)), "negatifte tekrar yok"


def test_google_build(tmp_path):
    res = dict(gx.build(tmp_path))
    for f in ("01_campaigns.csv", "03_keywords.csv", "04_responsive_search_ads.csv",
              "05_negative_keywords.csv"):
        assert (tmp_path / f).exists() and (tmp_path / f).stat().st_size > 0
    assert res["01_campaigns.csv"] == 3
    assert res["03_keywords.csv"] >= 25


def test_meta_build(tmp_path):
    res = dict(mx.build(tmp_path))
    assert (tmp_path / "meta-kurulum-rehberi.md").exists()
    assert res["meta-reklam-metinleri.csv"] >= 5


def test_seo_schema_valid(tmp_path):
    d = seo.schema_jsonld()
    json.dumps(d)  # serileşebilir
    assert d["@type"] == "Hotel"
    assert d["telephone"] == "+905322342686"
    assert "geo" in d and "address" in d
    assert "aggregateRating" not in d, "sahte puan eklenmemeli"
    res = dict(seo.build(tmp_path))
    assert (tmp_path / "schema-lodgingbusiness.jsonld").exists()


def test_presence_data():
    assert len(presence.PROPERTIES) >= 8
    assert len(presence.FIXES) == 14
    c = presence.counts()
    assert c["Kritik"] >= 3
