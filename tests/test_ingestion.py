from kads.data.ingestion.google_ads import fetch_google_campaigns
from kads.data.ingestion.meta_ads import fetch_meta_campaigns

def test_google_campaign_ingestion():
    campaigns = fetch_google_campaigns()
    assert isinstance(campaigns, list)
    assert len(campaigns) > 0
    c = campaigns[0]
    assert "campaign_id" in c
    assert "campaign_name" in c
    assert "spend" in c
    assert "conversions" in c

def test_meta_campaign_ingestion():
    campaigns = fetch_meta_campaigns()
    assert isinstance(campaigns, list)
    assert len(campaigns) > 0
    c = campaigns[0]
    assert "campaign_id" in c
    assert "campaign_name" in c
    assert "spend" in c
    assert "conversions" in c
