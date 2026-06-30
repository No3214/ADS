import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from kads.data.warehouse import db as db_mod
from kads.data.warehouse.models import DimCampaignState, FactActionJournal
from kads.memory.decision_memory import reflect_on_past_actions


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


def test_reflection_on_budget_increase(test_db):
    camp = DimCampaignState(
        campaign_id="g_123",
        campaign_name="Google Search Brand",
        platform="google",
        status="active",
        budget=180.0,
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
        status="executed",
        rollback_plan={"budget": 150.0},
    )
    test_db.add(action)
    test_db.commit()

    lessons = reflect_on_past_actions(test_db)
    assert len(lessons) == 1
    assert lessons[0]["action_id"] == "act_123"
    assert lessons[0]["promote_to_heuristic"] is True
    assert "Hypothesis validated" in lessons[0]["lesson"]
