from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from kads.data.warehouse.db import Base
from kads.data.warehouse.models import (DimCampaignState, FactActionJournal,
                                        FactAdPerformanceHourly)


@pytest.fixture(scope="function")
def test_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


def test_campaign_state_lifecycle(test_db):
    # Create campaign state
    camp = DimCampaignState(
        campaign_id="g_123",
        campaign_name="Google Search Brand",
        platform="google",
        status="active",
        budget=150.0,
        bid_strategy="tCPA",
    )
    test_db.add(camp)
    test_db.commit()

    # Query back
    queried = test_db.query(DimCampaignState).filter_by(campaign_id="g_123").first()
    assert queried is not None
    assert queried.campaign_name == "Google Search Brand"
    assert queried.budget == 150.0


def test_hourly_performance_relation(test_db):
    camp = DimCampaignState(
        campaign_id="g_123",
        campaign_name="Google Search Brand",
        platform="google",
        status="active",
        budget=150.0,
        bid_strategy="tCPA",
    )
    test_db.add(camp)
    test_db.commit()

    perf = FactAdPerformanceHourly(
        campaign_id="g_123",
        timestamp=datetime.utcnow(),
        spend=45.2,
        clicks=12,
        impressions=120,
        conversions=1,
        revenue=120.0,
    )
    test_db.add(perf)
    test_db.commit()

    queried = (
        test_db.query(FactAdPerformanceHourly).filter_by(campaign_id="g_123").first()
    )
    assert queried is not None
    assert queried.spend == 45.2
    assert queried.clicks == 12


def test_action_journal_json_fields(test_db):
    journal = FactActionJournal(
        action_id="act_999",
        platform="meta",
        entity_type="budget",
        entity_id="m_123",
        action_type="budget_increase",
        current_state={"budget": 100},
        proposed_state={"budget": 120},
        risk_score=0.2,
        confidence=0.9,
        requires_approval=True,
        approval_reason=["budget increase above 15%"],
        rollback_plan={"budget": 100},
    )
    test_db.add(journal)
    test_db.commit()

    queried = test_db.query(FactActionJournal).filter_by(action_id="act_999").first()
    assert queried is not None
    assert queried.current_state["budget"] == 100
    assert queried.proposed_state["budget"] == 120
    assert queried.approval_reason == ["budget increase above 15%"]
