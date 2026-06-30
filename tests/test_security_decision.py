import pytest

from kads.core.schemas import RiskSchema
from kads.core.security import evaluate_change, load_security_config
from kads.decision.risk_score import calculate_risk_score


def test_load_security_config():
    cfg = load_security_config()
    assert isinstance(cfg, dict)
    assert "google_monthly_try" in cfg
    assert "writes_enabled" in cfg


def test_evaluate_change_dry_run_denied():
    cfg = {
        "writes_enabled": False,
        "google_monthly_try": 15000,
        "meta_monthly_try": 15000,
        "google_daily_try": 500,
        "meta_daily_try": 500,
        "google_allowlist": {"1234567890"},
        "meta_allowlist": {"act_123"},
    }
    change = {
        "platform": "google",
        "account_id": "1234567890",
        "action": "pause",
        "entity": "campaign",
    }
    decision, reasons = evaluate_change(change, cfg, None)
    assert decision == "DENY"
    assert "Gerçek yazma kapalı" in reasons[0]


def test_risk_score_calculation():
    # Low risk
    action = {"action": "pause", "daily_budget_try": 100}
    risk = calculate_risk_score(action, tracking_score=100.0)
    assert isinstance(risk, RiskSchema)
    assert risk.risk_score == 0.0
    assert risk.risk_level == "low"
    assert risk.required_action == "none"

    # Critical risk - budget impact + tracking low + entity creation
    action2 = {"action": "create_campaign", "daily_budget_try": 500}
    risk2 = calculate_risk_score(action2, tracking_score=75.0)
    assert risk2.risk_score == 0.75
    assert risk2.risk_level == "critical"
    assert risk2.required_action == "block"
