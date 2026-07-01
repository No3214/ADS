import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from kads.data.warehouse import db as db_mod
from kads.data.warehouse.models import DimCampaignState, FactActionJournal
from kads.execution.executor import execute_action, rollback_action, CircuitBreakerState, get_circuit_breaker_state


@pytest.fixture(scope="function")
def test_db():
    engine = create_engine("sqlite:///:memory:")
    db_mod.Base.metadata.create_all(bind=engine)
    TestingSession = sessionmaker(bind=engine)
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()
        db_mod.Base.metadata.drop_all(bind=engine)


def test_execution_and_rollback_budget(test_db):
    camp = DimCampaignState(
        campaign_id="g_123",
        campaign_name="Google Search Brand",
        platform="google",
        status="active",
        budget=150.0,
        bid_strategy="tCPA",
    )
    test_db.add(camp)

    action = FactActionJournal(
        action_id="act_123",
        platform="google",
        entity_type="budget",
        entity_id="g_123",
        action_type="budget_increase",
        current_state={"budget": 150.0},
        proposed_state={"budget": 180.0},
        risk_score=0.1,
        confidence=0.9,
        status="approved",
        rollback_plan={"budget": 150.0},
    )
    test_db.add(action)
    test_db.commit()

    success = execute_action(action, test_db)
    assert success is True
    assert action.status == "executed"
    assert camp.budget == 180.0

    rollback_success = rollback_action(action, test_db)
    assert rollback_success is True
    assert action.status == "rolled_back"
    assert camp.budget == 150.0


def test_circuit_breaker(test_db):
    # Setup two failed actions in the last 24 hours
    import datetime
    
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
        test_db.add(f_action)
    
    # An approved action we wish to execute
    approved_action = FactActionJournal(
        action_id="approved_act",
        platform="google",
        entity_type="budget",
        entity_id="g_123",
        action_type="budget_increase",
        current_state={"budget": 150.0},
        proposed_state={"budget": 180.0},
        risk_score=0.1,
        confidence=0.9,
        status="approved",
    )
    test_db.add(approved_action)
    test_db.commit()
    
    # Execute should return False and fail because of circuit breaker
    success = execute_action(approved_action, test_db)
    assert success is False
    assert approved_action.status == "approved"  # Remains unchanged
    
    # Test HALF_OPEN State
    # Move the failures back by 2 hours so it transitions to HALF_OPEN
    two_hours_ago = datetime.datetime.utcnow() - datetime.timedelta(hours=2)
    for f in test_db.query(FactActionJournal).filter_by(status="failed").all():
        f.executed_at = two_hours_ago
    test_db.commit()
    
    cb_state = get_circuit_breaker_state(test_db)
    assert cb_state == CircuitBreakerState.HALF_OPEN
    
    # Budget increase should still fail in HALF_OPEN
    success = execute_action(approved_action, test_db)
    assert success is False
    
    # But a pause action should succeed
    pause_action = FactActionJournal(
        action_id="pause_act",
        platform="google",
        entity_type="campaign",
        entity_id="g_123",
        action_type="pause",
        current_state={"status": "active"},
        proposed_state={"status": "PAUSED"},
        risk_score=0.1,
        confidence=0.9,
        status="approved",
    )
    test_db.add(pause_action)
    test_db.commit()
    
    success = execute_action(pause_action, test_db)
    assert success is True



def test_budget_cap_guardrail_blocks(test_db):
    """Defense-in-depth: günlük bütçe tavanını aşan onaylı aksiyon ENGELLENMELİ (executor)."""
    camp = DimCampaignState(
        campaign_id="g_cap", campaign_name="Cap test", platform="google",
        status="active", budget=150.0, bid_strategy="tCPA",
    )
    test_db.add(camp)
    action = FactActionJournal(
        action_id="cap_act", platform="google", entity_type="budget", entity_id="g_cap",
        action_type="budget_increase", current_state={"budget": 150.0},
        proposed_state={"budget": 9000.0},  # tavanın çok üstü
        risk_score=0.1, confidence=0.9, status="approved", rollback_plan={"budget": 150.0},
    )
    test_db.add(action)
    test_db.commit()
    assert execute_action(action, test_db) is False
    assert camp.budget == 150.0  # değişmedi


def test_status_not_approved_blocks(test_db):
    """approved olmayan aksiyon yürütülemez."""
    a = FactActionJournal(
        action_id="pending_act", platform="google", entity_type="budget", entity_id="g_x",
        action_type="budget_increase", current_state={"budget": 100.0},
        proposed_state={"budget": 120.0}, risk_score=0.1, confidence=0.9, status="pending",
    )
    test_db.add(a); test_db.commit()
    assert execute_action(a, test_db) is False
    assert a.status == "pending"


def test_invalid_budget_guardrail_blocks(test_db):
    """Sayı olmayan proposed budget -> guardrail ENGELLE (TypeError/ValueError yolu)."""
    camp = DimCampaignState(campaign_id="g_inv", campaign_name="x", platform="google",
                            status="active", budget=100.0, bid_strategy="tCPA")
    a = FactActionJournal(
        action_id="inv_act", platform="google", entity_type="budget", entity_id="g_inv",
        action_type="budget_increase", current_state={"budget": 100.0},
        proposed_state={"budget": "abc"}, risk_score=0.1, confidence=0.9, status="approved",
    )
    test_db.add_all([camp, a]); test_db.commit()
    assert execute_action(a, test_db) is False
    assert camp.budget == 100.0


def test_flapping_guardrail_blocks(test_db):
    """Aynı entity 24s'de >=3 bütçe değişimi yapmışsa 4.'sü ENGELLE (flapping)."""
    import datetime
    camp = DimCampaignState(campaign_id="g_flap", campaign_name="x", platform="google",
                            status="active", budget=100.0, bid_strategy="tCPA")
    test_db.add(camp)
    now = datetime.datetime.utcnow()
    for i in range(3):  # 3 executed bütçe değişimi (tavan altı)
        test_db.add(FactActionJournal(
            action_id=f"flap_{i}", platform="google", entity_type="budget", entity_id="g_flap",
            action_type="budget_increase", current_state={"budget": 100.0},
            proposed_state={"budget": 110.0}, risk_score=0.1, confidence=0.9,
            status="executed", executed_at=now))
    a = FactActionJournal(
        action_id="flap_new", platform="google", entity_type="budget", entity_id="g_flap",
        action_type="budget_increase", current_state={"budget": 100.0},
        proposed_state={"budget": 120.0},  # tavan altı ama flapping
        risk_score=0.1, confidence=0.9, status="approved")
    test_db.add(a); test_db.commit()
    assert execute_action(a, test_db) is False


def test_execute_campaign_exception_sets_failed(test_db):
    """try-bloğunda hata olursa status=failed olmalı (proposed_state bozuk)."""
    camp = DimCampaignState(campaign_id="g_err", campaign_name="x", platform="google",
                            status="active", budget=100.0, bid_strategy="tCPA")
    a = FactActionJournal(
        action_id="err_act", platform="google", entity_type="campaign", entity_id="g_err",
        action_type="pause", current_state={"status": "active"},
        proposed_state=["bozuk"],  # list -> .get() AttributeError
        risk_score=0.1, confidence=0.9, status="approved")
    test_db.add_all([camp, a]); test_db.commit()
    assert execute_action(a, test_db) is False
    assert a.status == "failed"
    assert a.executed_at is not None


def test_rollback_requires_executed(test_db):
    """executed olmayan aksiyon geri alınamaz."""
    a = FactActionJournal(
        action_id="ro_pending", platform="google", entity_type="budget", entity_id="g_x",
        action_type="budget_increase", current_state={"budget": 100.0},
        proposed_state={"budget": 120.0}, risk_score=0.1, confidence=0.9, status="approved")
    test_db.add(a); test_db.commit()
    assert rollback_action(a, test_db) is False


def test_rollback_campaign_restores_status(test_db):
    """Kampanya pause'u geri al -> status eski haline döner."""
    camp = DimCampaignState(campaign_id="g_ro", campaign_name="x", platform="google",
                            status="active", budget=100.0, bid_strategy="tCPA")
    a = FactActionJournal(
        action_id="ro_camp", platform="google", entity_type="campaign", entity_id="g_ro",
        action_type="pause", current_state={"status": "active"},
        proposed_state={"status": "PAUSED"}, risk_score=0.1, confidence=0.9,
        status="approved", rollback_plan={"status": "active"})
    test_db.add_all([camp, a]); test_db.commit()
    assert execute_action(a, test_db) is True
    assert camp.status == "paused"
    assert rollback_action(a, test_db) is True
    assert camp.status == "active"


def test_rollback_exception_returns_false(test_db):
    """Rollback try-bloğu hata -> False (rollback_plan bozuk)."""
    camp = DimCampaignState(campaign_id="g_rerr", campaign_name="x", platform="google",
                            status="paused", budget=100.0, bid_strategy="tCPA")
    a = FactActionJournal(
        action_id="ro_err", platform="google", entity_type="campaign", entity_id="g_rerr",
        action_type="pause", current_state=["bozuk"], proposed_state={"status": "PAUSED"},
        risk_score=0.1, confidence=0.9, status="executed", rollback_plan=None)
    test_db.add_all([camp, a]); test_db.commit()
    # rollback_plan None + current_state list -> .get AttributeError -> False
    assert rollback_action(a, test_db) is False


def test_is_circuit_breaker_tripped_helper(test_db):
    """is_circuit_breaker_tripped() CLOSED durumda False döner."""
    from kads.execution.executor import is_circuit_breaker_tripped
    assert is_circuit_breaker_tripped(test_db) is False
