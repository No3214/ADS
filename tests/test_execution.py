import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from kads.data.warehouse import db as db_mod
from kads.data.warehouse.models import DimCampaignState, FactActionJournal
from kads.execution.executor import execute_action, rollback_action


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

