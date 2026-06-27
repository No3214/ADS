"""kads buyume katmani testleri: PMax / Demand Gen / Google remarketing."""
from kads.cli import main
from kads import data_growth as dg


def test_pmax_ok(): assert main(["pmax", "-f", "json"]) == 0
def test_pmax_specs_ok(): assert main(["pmax", "specs"]) == 0
def test_pmax_setup_ok(): assert main(["pmax", "setup", "-f", "json"]) == 0
def test_demandgen_ok(): assert main(["demandgen", "-f", "json"]) == 0
def test_demandgen_aud_ok(): assert main(["demandgen", "audiences", "-f", "csv"]) == 0
def test_demandgen_specs_ok(): assert main(["demandgen", "specs"]) == 0
def test_remarketing_ok(): assert main(["remarketing", "-f", "json"]) == 0
def test_remarketing_rlsa_ok(): assert main(["remarketing", "rlsa", "-f", "json"]) == 0
def test_remarketing_flow_ok(): assert main(["remarketing", "flow"]) == 0


def test_pmax_data():
    assert len(dg.PMAX_ASSET_GROUPS) >= 4
    assert all(g.get("final_url", "").startswith("https://") for g in dg.PMAX_ASSET_GROUPS)
    assert len(dg.PMAX_ASSET_SPECS) >= 8 and dg.PMAX_NOTE


def test_demandgen_data():
    assert len(dg.DEMAND_GEN_FORMATS) >= 3
    assert len(dg.DEMAND_GEN_AUDIENCES) >= 4


def test_remarketing_data():
    assert len(dg.GOOGLE_REMARKETING) >= 6
    assert all(isinstance(r["uyelik_gun"], int) and r["uyelik_gun"] > 0 for r in dg.GOOGLE_REMARKETING)
    assert len(dg.RLSA_RULES) >= 4 and len(dg.REMARKETING_FLOW) >= 5


def test_utm_matrix_ok(): assert main(["utm", "-f", "json"]) == 0
def test_utm_rules_ok(): assert main(["utm", "rules"]) == 0
def test_utm_build_ok(): assert main(["utm", "build", "--url", "https://x.com/a", "--channel", "google-pmax"]) == 0
def test_utm_build_custom_ok(): assert main(["utm", "build", "--url", "https://x.com/a?q=1", "--source", "meta", "--medium", "paid_social", "--campaign", "retargeting"]) == 0
def test_utm_build_missing_args(): assert main(["utm", "build", "--url", "https://x.com"]) != 0
def test_utm_build_bad_channel(): assert main(["utm", "build", "--url", "https://x.com", "--channel", "yok-boyle"]) != 0
def test_attribution_ok(): assert main(["attribution", "-f", "json"]) == 0


def test_utm_data():
    assert len(dg.UTM_MATRIX) >= 12
    assert all(r["utm_source"] == r["utm_source"].lower() and " " not in r["utm_campaign"] for r in dg.UTM_MATRIX)


def test_attribution_data():
    assert len(dg.ATTRIBUTION) >= 6 and len(dg.ATTRIBUTION_NOTES) >= 4


def test_allocate_ok(): assert main(["allocate", "-f", "json"]) == 0
def test_allocate_funnel_ok(): assert main(["allocate", "funnel"]) == 0
def test_allocate_rules_ok(): assert main(["allocate", "rules", "-f", "json"]) == 0
def test_season_detail_ok(): assert main(["season", "detail", "-f", "json"]) == 0
def test_season_default_ok(): assert main(["season"]) == 0


def test_budget_sums_30k():
    a1 = sum(r["ay1_try"] for r in dg.BUDGET_MATRIX)
    a2 = sum(r["ay2_try"] for r in dg.BUDGET_MATRIX)
    assert a1 == dg.BUDGET_TOTAL_TRY == a2 == 30000


def test_season_detail_data():
    assert len(dg.SEASON_DETAIL) == 3 and all("b2b" in s and s["aylar"] for s in dg.SEASON_DETAIL)
    assert len(dg.BUDGET_BY_FUNNEL) >= 4 and len(dg.BUDGET_REALLOCATION_RULES) >= 5


def test_conversions_ok(): assert main(["conversions", "-f", "json"]) == 0
def test_conversions_offline_ok(): assert main(["conversions", "offline", "-f", "json"]) == 0
def test_conversions_enhanced_ok(): assert main(["conversions", "enhanced"]) == 0
def test_conversions_calls_ok(): assert main(["conversions", "calls", "-f", "csv"]) == 0


def test_conversions_data():
    assert len(dg.CONVERSION_ACTIONS) >= 6
    assert any(a["olay"] == "booking_offline" for a in dg.CONVERSION_ACTIONS)
    assert len(dg.OFFLINE_IMPORT_GOOGLE) >= 5 and len(dg.OFFLINE_IMPORT_META) >= 4
    assert len(dg.ENHANCED_MATCHING) >= 3 and len(dg.CALL_TRACKING) >= 4 and dg.CONVERSION_NOTE


def test_events_ok(): assert main(["events", "-f", "json"]) == 0
def test_events_data():
    assert len(dg.LOCAL_EVENTS) >= 3
    assert any("What A Fest" in e["etkinlik"] for e in dg.LOCAL_EVENTS)
    assert all({"etkinlik", "tarih", "etki", "aksiyon"} <= set(e) for e in dg.LOCAL_EVENTS)
