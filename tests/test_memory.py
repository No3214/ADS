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


def test_reflection_pause_lesson():
    """decision_memory: executed pause aksiyonundan ders çıkarır (pause dalı)."""
    import datetime
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from kads.data.warehouse import db as db_mod
    from kads.data.warehouse.models import FactActionJournal
    from kads.memory.decision_memory import reflect_on_past_actions

    eng = create_engine("sqlite:///:memory:")
    db_mod.Base.metadata.create_all(bind=eng)
    db = sessionmaker(bind=eng)()
    try:
        db.add(FactActionJournal(
            action_id="pause_refl", platform="meta", entity_type="campaign",
            entity_id="m1", action_type="pause", current_state={"status": "active"},
            proposed_state={"status": "PAUSED"}, expected_impact="CPA düşer",
            risk_score=0.1, confidence=0.9, status="executed",
            executed_at=datetime.datetime.utcnow()))
        db.commit()
        lessons = reflect_on_past_actions(db)
        assert any(l["action_id"] == "pause_refl" for l in lessons)
        assert any("3x Kill Rule" in l["lesson"] for l in lessons)
    finally:
        db.close()
        db_mod.Base.metadata.drop_all(bind=eng)
