"""Genişletme testleri: display, A/B, yerleşim, kitle, kurallar, rapor."""
from kads import data_ext as dx
from kads import rules, report
from kads.platforms import google as gx
from kads.platforms import meta as mx


def test_data_ext_shapes():
    assert dx.GOOGLE_DISPLAY["status"] == "Paused"
    assert len(dx.META_PLACEMENT_SPECS) == 3
    assert len(dx.OPT_RULES) >= 8
    assert len(dx.RETARGETING_AUDIENCES) >= 6
    assert len(dx.AB_ANGLES) == 3 and len(dx.META_AB_HOOKS) == 3


def test_google_display_and_ab():
    assert len(gx.display_rows()) == 1
    ab = gx.rsa_ab_rows()
    assert len(ab) == 15  # 5 reklam grubu × 3 varyant
    for r in ab:
        for k, v in r.items():
            if k.startswith("Headline ") and isinstance(v, str):
                assert len(v) <= 30, f">30: {v}"


def test_meta_placements_audiences_ab():
    assert len(mx.placement_rows()) == 3
    aud = mx.audiences_rows()
    assert len(aud) >= 6 and all(r["Kullanim"] for r in aud)
    assert len(mx.copy_ab_rows()) == 15  # 5 konsept × 3


def test_rules_ascii_keys_and_eval():
    for r in rules.rule_rows():
        assert set(["oncelik", "id", "metrik", "kosul", "aksiyon"]).issubset(r.keys())
    trig = rules.evaluate({"blended_roas": 3.5, "blended_cpa_try": 2500, "meta_frequency": 3.0})
    ids = [t["id"] for t in trig]
    assert "ROAS_SCALE" in ids and "CPA_OVER" in ids and "FREQ_HIGH" in ids
    # risk önce
    assert trig[0]["oncelik"] == "Risk"


def test_report_compute():
    k = report.compute({"google_spend_try": 15000, "meta_spend_try": 15000,
                        "tracked_revenue_try": 90000, "google_conversions": 6, "meta_purchases": 6})
    assert k["toplam_harcama_try"] == 30000
    assert k["blended_roas"] == 3.0
    assert abs(k["blended_cpa_try"] - 2500) < 1


def test_report_template(tmp_path):
    n = report.write_template(tmp_path / "metrics.csv")
    assert (tmp_path / "metrics.csv").exists() and n >= 15


def test_build_includes_new_files(tmp_path):
    res = dict(gx.build(tmp_path / "g"))
    assert "09_display_campaign.csv" in res and "10_rsa_ab_variants.csv" in res
    res2 = dict(mx.build(tmp_path / "m"))
    assert "meta-yerlesim-sablonlari.csv" in res2 and "meta-retargeting-kitleleri.csv" in res2


def test_calendar_generate():
    from kads import calendar as cal
    import datetime
    rows = cal.generate(30, datetime.date(2026, 7, 1))
    assert len(rows) > 40
    chans = {r["kanal"] for r in rows}
    assert {"Instagram", "TikTok", "X", "LinkedIn", "Facebook"}.issubset(chans)


def test_publish_rows_match():
    from kads import calendar as cal, publish
    rows = cal.generate(14)
    assert len(publish.to_postiz_rows(rows)) == len(rows)


def test_competitors_data():
    from kads import data_ext as dx
    assert len(dx.COMPETITORS) >= 4
    assert len(dx.CHANNELS) >= 5 and "TikTok" in dx.CHANNELS


def test_apify_actors():
    from kads import data_ext as dx
    assert len(dx.APIFY_ACTORS) >= 5
    assert any("rag-web-browser" in a["actor"] for a in dx.APIFY_ACTORS)
    assert "tripadvisor" in dx.APIFY_LIVE_URLS


def test_aeo_data():
    from kads import data_ext as dx
    assert len(dx.AEO_CLUSTERS) == 8
    assert len(dx.AEO_SCHEMA_CHECKLIST) == 5


def test_aeo_schemas_valid_json():
    import json, glob
    from pathlib import Path
    root = Path(__file__).resolve().parents[1]
    files = glob.glob(str(root / "aeo" / "schema" / "*.jsonld"))
    assert len(files) >= 5
    for f in files:
        d = json.load(open(f, encoding="utf-8"))
        assert d.get("@context") == "https://schema.org"
        # sahte puan eklenmemis olmali
        assert "aggregateRating" not in d


def test_season_funnel_offers_data():
    from kads import data_ext as dx
    assert len(dx.SEASONS) == 3
    assert len(dx.FUNNEL_STAGES) == 5
    assert len(dx.OFFERS) >= 4


def test_web_checklist_and_manifest():
    import json
    from pathlib import Path
    from kads import data_ext as dx
    assert len(dx.WEB_CHECKLIST) == 6
    root = Path(__file__).resolve().parents[1]
    man = json.load(open(root / "web" / "pwa" / "manifest.webmanifest", encoding="utf-8"))
    assert man["display"] == "standalone" and man["start_url"].startswith("/")
    assert any(i["sizes"] == "512x512" for i in man["icons"])


def test_b2b_data():
    from kads import data_ext as dx
    assert len(dx.B2B_TARGETS) == 4 and len(dx.B2B_PACKAGES) == 5
    assert any("SOCAR" in t["cap_firma"] or "STAR" in t["cap_firma"] for t in dx.B2B_TARGETS)
