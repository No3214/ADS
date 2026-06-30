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


def test_anti_loop_guard():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from kads.data.warehouse import db as db_mod
    from kads.data.warehouse.models import FactActionJournal
    import datetime
    
    engine = create_engine("sqlite:///:memory:")
    db_mod.Base.metadata.create_all(bind=engine)
    TestingSession = sessionmaker(bind=engine)
    db = TestingSession()
    
    # Setup two failures in the last 24h
    for i in range(2):
        f_action = FactActionJournal(
            action_id=f"failed_act_{i}",
            platform="google",
            entity_type="budget",
            entity_id="g_123",
            action_type="budget_increase",
            current_state={"budget": 150.0},
            proposed_state={"budget": 180.0},
            risk_score=0.1,
            confidence=0.9,
            status="failed",
            executed_at=datetime.datetime.utcnow(),
        )
        db.add(f_action)
    db.commit()
    
    # We will temporarily mock kads.data.warehouse.db.SessionLocal
    import kads.data.warehouse.db as db_module
    old_session_local = db_module.SessionLocal
    db_module.SessionLocal = lambda: db
    
    try:
        cfg = {
            "writes_enabled": True,
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
            "action": "budget_increase",
            "entity": "budget",
        }
        decision, reasons = evaluate_change(change, cfg, None)
        assert decision == "DENY"
        assert "Anti-Loop Policy triggered" in reasons[0]
    finally:
        db_module.SessionLocal = old_session_local
        db.close()
        db_mod.Base.metadata.drop_all(bind=engine)

