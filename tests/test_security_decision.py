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



# ---- evaluate_change tüm karar dalları (guardrail matrisi) ------------------
_BASE_CFG = {
    "writes_enabled": True,
    "google_monthly_try": 15000, "meta_monthly_try": 15000,
    "google_daily_try": 500, "meta_daily_try": 500,
    "google_allowlist": {"1234567890"}, "meta_allowlist": {"act_123"},
}


def _cfg(**over):
    c = dict(_BASE_CFG); c.update(over); return c


def test_unknown_platform_denied():
    d, r = evaluate_change({"platform": "tiktok", "account_id": "x", "action": "pause"}, _cfg(), None)
    assert d == "DENY" and "Bilinmeyen platform" in r[-1]


def test_hard_blocked_action_denied():
    d, r = evaluate_change(
        {"platform": "google", "account_id": "1234567890", "action": "delete_campaign"}, _cfg(), None)
    assert d == "DENY" and "kalıcı olarak engellendi" in r[-1]


def test_action_not_in_allowlist_denied():
    d, r = evaluate_change(
        {"platform": "google", "account_id": "1234567890", "action": "hack_stuff"}, _cfg(), None)
    assert d == "DENY" and "izinli listede değil" in r[-1]


def test_google_allowlist_empty_denied():
    d, r = evaluate_change(
        {"platform": "google", "account_id": "1234567890", "action": "pause"},
        _cfg(google_allowlist=set()), None)
    assert d == "DENY" and "allowlist boş" in r[-1]


def test_google_account_not_allowed_denied():
    d, r = evaluate_change(
        {"platform": "google", "account_id": "9999999999", "action": "pause"}, _cfg(), None)
    assert d == "DENY" and "allowlist dışında" in r[-1]


def test_meta_allowlist_empty_denied():
    d, r = evaluate_change(
        {"platform": "meta", "account_id": "act_123", "action": "pause"},
        _cfg(meta_allowlist=set()), None)
    assert d == "DENY" and "allowlist boş" in r[-1]


def test_meta_account_not_allowed_denied():
    d, r = evaluate_change(
        {"platform": "meta", "account_id": "act_999", "action": "pause"}, _cfg(), None)
    assert d == "DENY" and "allowlist dışında" in r[-1]


def test_daily_budget_over_cap_denied():
    d, r = evaluate_change(
        {"platform": "google", "account_id": "1234567890", "action": "update_budget",
         "daily_budget_try": 600}, _cfg(), "ONAYLA | google | 1234567890 | update_budget | 600")
    assert d == "DENY" and "Günlük bütçe tavanı" in r[-1]


def test_invalid_daily_budget_denied():
    d, r = evaluate_change(
        {"platform": "google", "account_id": "1234567890", "action": "update_budget",
         "daily_budget_try": "abc"}, _cfg(), "ONAYLA | google | 1234567890 | update_budget | 100")
    assert d == "DENY" and "Geçersiz daily" in r[-1]


def test_monthly_budget_over_cap_denied():
    d, r = evaluate_change(
        {"platform": "meta", "account_id": "act_123", "action": "update_budget",
         "monthly_budget_try": 99999}, _cfg(), "ONAYLA | meta | act_123 | update_budget | 100")
    assert d == "DENY" and "Aylık bütçe tavanı" in r[-1]


def test_no_approval_needs_approval():
    d, r = evaluate_change(
        {"platform": "google", "account_id": "1234567890", "action": "pause"}, _cfg(), None)
    assert d == "NEEDS_APPROVAL" and "Açık onay gerekli" in r[-1]


def test_valid_approval_allows():
    d, r = evaluate_change(
        {"platform": "google", "account_id": "1234567890", "action": "pause"},
        _cfg(), "ONAYLA | google | 1234567890 | pause | 0")
    assert d == "ALLOW" and "Tüm korkuluklar geçildi" in r[-1]


def test_enable_needs_second_approval():
    # normal onay yeterli değil, ENABLE ikinci onay ister
    d, r = evaluate_change(
        {"platform": "google", "account_id": "1234567890", "action": "enable"},
        _cfg(), "ONAYLA | google | 1234567890 | enable | 100")
    assert d == "NEEDS_APPROVAL" and "ikinci onay" in r[-1]


def test_enable_with_second_marker_allows():
    d, r = evaluate_change(
        {"platform": "google", "account_id": "1234567890", "action": "enable"},
        _cfg(), "ONAYLA-2 | google | 1234567890 | enable | 100")
    assert d == "ALLOW"


def test_approval_wrong_platform_rejected():
    # onay meta diyor ama değişiklik google -> eşleşmez -> NEEDS_APPROVAL
    d, r = evaluate_change(
        {"platform": "google", "account_id": "1234567890", "action": "pause"},
        _cfg(), "ONAYLA | meta | 1234567890 | pause | 0")
    assert d == "NEEDS_APPROVAL"


def test_approval_too_few_parts_rejected():
    d, r = evaluate_change(
        {"platform": "google", "account_id": "1234567890", "action": "pause"},
        _cfg(), "ONAYLA | google")
    assert d == "NEEDS_APPROVAL"
