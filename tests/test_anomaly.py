from kads.decision.anomaly import detect_anomalies
from kads.decision.engine import run_agent_council


def test_detect_anomalies_conversion_bleed():
    campaigns = [
        {
            "campaign_id": "g_bleed_123",
            "campaign_name": "Google — Generic Search",
            "platform": "google",
            "status": "active",
            "spend": 1200.0,
            "clicks": 50,
            "impressions": 800,
            "conversions": 0,
            "revenue": 0.0,
            "budget": 200.0,
        }
    ]
    anomalies = detect_anomalies(campaigns)
    assert len(anomalies) == 1
    assert anomalies[0]["type"] == "conversion_bleed"
    assert anomalies[0]["severity"] == "CRITICAL"


def test_detect_anomalies_cpc_spike_and_click_drop():
    campaigns = [
        {
            "campaign_id": "m_spike_111",
            "campaign_name": "Meta — Conversions",
            "platform": "meta",
            "status": "active",
            "spend": 1000.0,
            "clicks": 5,  # CPC = 200 TL (> 150 TL)
            "impressions": 400,
            "conversions": 2,
            "revenue": 2000.0,
            "budget": 100.0,
        },
        {
            "campaign_id": "g_drop_222",
            "campaign_name": "Google — Display",
            "platform": "google",
            "status": "active",
            "spend": 50.0,
            "clicks": 0,  # zero clicks despite impressions >= 500
            "impressions": 600,
            "conversions": 0,
            "revenue": 0.0,
            "budget": 50.0,
        },
    ]
    anomalies = detect_anomalies(campaigns)
    types = [a["type"] for a in anomalies]
    assert "cpc_spike" in types
    assert "click_drop" in types


def test_agent_council_emergency_pause():
    google_campaigns = [
        {
            "campaign_id": "g_bleed_123",
            "campaign_name": "Google — Generic Search",
            "platform": "google",
            "status": "active",
            "spend": 1200.0,
            "clicks": 50,
            "impressions": 800,
            "conversions": 0,
            "revenue": 0.0,
            "budget": 200.0,
        }
    ]

    actions = run_agent_council(google_campaigns, [])
    # Should trigger conversion_bleed -> pause action
    pauses = [a for a in actions if a.action_type == "pause"]
    assert len(pauses) == 1
    assert pauses[0].risk_score == 0.99
    assert "EMERGENCY PAUSE" in pauses[0].expected_impact
