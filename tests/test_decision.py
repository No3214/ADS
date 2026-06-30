from kads.core.schemas import ActionSchema
from kads.decision.engine import run_agent_council


def test_agent_council_budget_increase():
    google_campaigns = [
        {
            "campaign_id": "g_brand_123",
            "campaign_name": "Google — Marka Search",
            "platform": "google",
            "status": "active",
            "budget": 148.0,
            "bid_strategy": "tCPA",
            "spend": 120.5,
            "clicks": 45,
            "impressions": 320,
            "conversions": 3,
            "revenue": 6000.0,
        }
    ]
    meta_campaigns = []

    actions = run_agent_council(google_campaigns, meta_campaigns)
    assert len(actions) == 1
    action = actions[0]
    assert isinstance(action, ActionSchema)
    assert action.action_type == "budget_increase"
    assert action.proposed_state["budget"] == 180.8


def test_agent_council_cpa_kill_rule():
    google_campaigns = []
    meta_campaigns = [
        {
            "campaign_id": "m_prospecting_111",
            "campaign_name": "Meta — Prospecting (Website Sales)",
            "platform": "meta",
            "status": "active",
            "budget": 350.0,
            "bid_strategy": "Lowest Cost",
            "spend": 900.0,
            "clicks": 98,
            "impressions": 4500,
            "conversions": 0,
            "revenue": 0.0,
        }
    ]

    actions = run_agent_council(google_campaigns, meta_campaigns)
    assert len(actions) == 1
    action = actions[0]
    assert isinstance(action, ActionSchema)
    assert action.action_type == "pause"
    assert action.requires_approval is True
    assert "Analyst Agent: 3x Kill Rule" in action.approval_reason[-1]


def test_agent_council_ad_fatigue_creative():
    google_campaigns = [
        {
            "campaign_id": "g_fatigue_123",
            "campaign_name": "Google — Marka Search",
            "platform": "google",
            "status": "active",
            "budget": 148.0,
            "bid_strategy": "tCPA",
            "spend": 120.0,
            "clicks": 15,
            "impressions": 1000,  # CTR = 1.5% (< 2.0%)
            "conversions": 1,
            "revenue": 120.0,
        }
    ]
    meta_campaigns = []

    actions = run_agent_council(google_campaigns, meta_campaigns)
    assert len(actions) == 1
    action = actions[0]
    assert isinstance(action, ActionSchema)
    assert action.action_type == "creative_test"
    assert "headline" in action.proposed_state
    assert "description" in action.proposed_state
    assert action.requires_approval is True
