from kads.observability.health import audit_tracking_health
from kads import core

def test_audit_tracking_health_placeholders(monkeypatch):
    mock_env = {
        "GA4_MEASUREMENT_ID": "replace-me",
        "GTM_CONTAINER_ID": "replace-me",
        "META_PIXEL_ID": "replace-me",
        "META_ACCESS_TOKEN": "replace-me",
        "GOOGLE_ADS_CUSTOMER_ID": "replace-me"
    }
    monkeypatch.setattr(core, "load_env", lambda: mock_env)

    health = audit_tracking_health()
    assert health["score"] == 10.0
    assert health["status"] == "unhealthy"
    assert health["components"]["GA4"]["status"] == "error"

def test_audit_tracking_health_healthy(monkeypatch):
    mock_env = {
        "GA4_MEASUREMENT_ID": "G-12345",
        "GTM_CONTAINER_ID": "GTM-12345",
        "META_PIXEL_ID": "123456",
        "META_ACCESS_TOKEN": "EAAB...",
        "GOOGLE_ADS_CUSTOMER_ID": "123-456-7890"
    }
    monkeypatch.setattr(core, "load_env", lambda: mock_env)

    health = audit_tracking_health()
    assert health["score"] == 100.0
    assert health["status"] == "healthy"
    assert health["components"]["GA4"]["status"] == "healthy"
