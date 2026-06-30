from datetime import datetime

import pytest
from pydantic import ValidationError

from kads.core.schemas import ActionSchema, CampaignStateSchema, RiskSchema


def test_risk_schema_validation():
    # Valid model
    risk = RiskSchema(
        risk_score=0.34,
        risk_level="medium",
        reasons=["budget impact above normal"],
        required_action="human_approval",
    )
    assert risk.risk_score == 0.34
    assert risk.risk_level == "medium"
    assert risk.required_action == "human_approval"

    # Invalid score (ge=0.0, le=1.0)
    with pytest.raises(ValidationError):
        RiskSchema(risk_score=1.5, risk_level="high", required_action="block")

    with pytest.raises(ValidationError):
        RiskSchema(risk_score=-0.1, risk_level="high", required_action="block")

    # Invalid risk level
    with pytest.raises(ValidationError):
        RiskSchema(risk_score=0.5, risk_level="super-high", required_action="block")


def test_action_schema_validation():
    # Valid model
    action = ActionSchema(
        action_id="act_123",
        platform="google",
        entity_type="campaign",
        entity_id="12345",
        action_type="pause",
        expected_impact="Stop budget bleed",
        risk_score=0.1,
        confidence=0.9,
        requires_approval=True,
    )
    assert action.action_id == "act_123"
    assert action.status == "pending"
    assert isinstance(action.created_at, datetime)

    # Invalid platform
    with pytest.raises(ValidationError):
        ActionSchema(
            action_id="act_123",
            platform="invalid_platform",
            entity_type="campaign",
            entity_id="12345",
            action_type="pause",
            expected_impact="Stop budget bleed",
            risk_score=0.1,
            confidence=0.9,
        )


def test_campaign_state_schema_validation():
    # Valid model
    state = CampaignStateSchema(
        campaign_id="12345",
        campaign_name="Foça Summer Promo",
        platform="google",
        status="active",
        budget=100.0,
        bid_strategy="tCPA",
        metrics={"conversions": 10, "spend": 500},
    )
    assert state.campaign_id == "12345"
    assert state.metrics["conversions"] == 10
