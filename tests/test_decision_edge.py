"""Karar katmanı edge case'leri: risk_score tüm dallar, MMM sınırlar, engine transfer."""
from kads.decision.risk_score import calculate_risk_score
from kads.decision.mmm import calculate_saturation_point as analyze_campaign_mmm
from kads.decision.engine import run_agent_council


# ---- risk_score: her dal ----------------------------------------------------
def test_risk_high_budget():
    r = calculate_risk_score({"action": "update_budget", "daily_budget_try": 500})
    assert r.risk_score >= 0.25 and "High daily budget" in " ".join(r.reasons)


def test_risk_medium_budget():
    r = calculate_risk_score({"action": "update_budget", "daily_budget_try": 250})
    assert any("Medium daily budget" in x for x in r.reasons)


def test_risk_invalid_budget():
    r = calculate_risk_score({"action": "update_budget", "daily_budget_try": "xx"})
    assert any("Invalid or unparseable" in x for x in r.reasons)


def test_risk_low_tracking():
    r = calculate_risk_score({"action": "pause"}, tracking_score=50.0)
    assert any("Low tracking health" in x for x in r.reasons)


def test_risk_suboptimal_tracking():
    r = calculate_risk_score({"action": "pause"}, tracking_score=90.0)
    assert any("Suboptimal tracking" in x for x in r.reasons)


def test_risk_entity_creation():
    r = calculate_risk_score({"action_type": "create_campaign"})
    assert any("Entity creation" in x for x in r.reasons)


def test_risk_activation():
    r = calculate_risk_score({"action_type": "enable"})
    assert any("Activating" in x for x in r.reasons)


def test_risk_clamped_and_critical():
    # yüksek bütçe + düşük tracking + create -> >=0.75 critical/block
    r = calculate_risk_score(
        {"action_type": "create_campaign", "daily_budget_try": 500}, tracking_score=50.0)
    assert r.risk_score <= 1.0
    assert r.risk_level == "critical" and r.required_action == "block"


def test_risk_levels_boundaries():
    assert calculate_risk_score({"action": "pause"}).risk_level == "low"
    # medium: sadece create (0.2)
    assert calculate_risk_score({"action_type": "create_campaign"}).risk_level == "medium"


# ---- MMM: sınır durumlar ----------------------------------------------------
def test_mmm_zero_spend():
    r = analyze_campaign_mmm(spend=0.0, revenue=0.0)
    assert r["status"] == "scalable" and r["suggested_cap"] == 500.0


def test_mmm_underperforming():
    r = analyze_campaign_mmm(spend=100.0, revenue=100.0)  # ROAS 1.0 < 1.5
    assert r["status"] == "underperforming" and r["suggested_cap"] <= 100.0


def test_mmm_stable():
    r = analyze_campaign_mmm(spend=100.0, revenue=200.0)  # ROAS 2.0
    assert r["status"] == "stable" and r["suggested_cap"] == 100.0


def test_mmm_scalable_bolder_at_high_roas():
    low = analyze_campaign_mmm(spend=100.0, revenue=300.0)   # ROAS 3.0
    high = analyze_campaign_mmm(spend=100.0, revenue=1000.0)  # ROAS 10
    assert low["status"] == high["status"] == "scalable"
    assert high["suggested_cap"] > low["suggested_cap"]  # yüksek ROAS daha cesur


# ---- engine: cross-platform bütçe transferi ---------------------------------
def _camp(cid, plat, spend, rev, budget=100.0, status="active"):
    return {"campaign_id": cid, "campaign_name": f"{plat} {cid}", "platform": plat,
            "status": status, "budget": budget, "bid_strategy": "tCPA",
            "spend": spend, "clicks": 50, "impressions": 500, "conversions": 5, "revenue": rev}


def test_engine_cross_platform_transfer_google_to_meta():
    """Google yüksek-ROAS + Meta düşük-ROAS/yüksek-harcama -> transfer aksiyonları."""
    g_high = _camp("g_hi", "google", spend=100.0, rev=400.0)   # 4.0x
    m_low = _camp("m_lo", "meta", spend=200.0, rev=200.0, budget=200.0)  # 1.0x, spend>100
    actions = run_agent_council([g_high], [m_low])
    kinds = {(a.platform, a.action_type) for a in actions}
    assert ("meta", "budget_decrease") in kinds
    assert ("google", "budget_increase") in kinds
    assert any("Transfer" in (a.expected_impact or "") for a in actions)


def test_engine_no_actions_on_balanced():
    """Dengeli, sağlıklı tek kampanya -> transfer tetiklenmez."""
    g = _camp("g_ok", "google", spend=100.0, rev=250.0)  # 2.5x, ne yüksek ne düşük
    actions = run_agent_council([g], [])
    assert all("Transfer" not in (a.expected_impact or "") for a in actions)
