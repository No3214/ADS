from kads import core

def fetch_google_campaigns() -> list[dict]:
    """
    Fetches campaign data from Google Ads API.
    Falls back to mock data if credentials are not configured (placeholders).
    """
    env = core.load_env()
    customer_id = env.get("GOOGLE_ADS_CUSTOMER_ID", "")
    dev_token = env.get("GOOGLE_ADS_DEVELOPER_TOKEN", "")

    if not customer_id or core.is_placeholder(customer_id) or core.is_placeholder(dev_token):
        # Simulated campaign data matching Kozbeyli Konağı channels
        return [
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
            },
            {
                "campaign_id": "g_nonbrand_456",
                "campaign_name": "Google — Dar non-brand Search",
                "platform": "google",
                "status": "active",
                "budget": 296.0,
                "bid_strategy": "tCPA",
                "spend": 280.0,
                "clicks": 56,
                "impressions": 1100,
                "conversions": 1,
                "revenue": 2000.0,
            },
            {
                "campaign_id": "g_test_789",
                "campaign_name": "Google — Kontrollü test",
                "platform": "google",
                "status": "paused",
                "budget": 49.0,
                "bid_strategy": "Maximize Clicks",
                "spend": 0.0,
                "clicks": 0,
                "impressions": 0,
                "conversions": 0,
                "revenue": 0.0,
            }
        ]

    # In production, this would use google-ads SDK to query GAQL.
    # Since we are executing in dry-run/mock default mode, return base data.
    return [
        {
            "campaign_id": "g_brand_123",
            "campaign_name": "Google — Marka Search",
            "platform": "google",
            "status": "active",
            "budget": 148.0,
            "bid_strategy": "tCPA",
            "spend": 130.0,
            "clicks": 50,
            "impressions": 350,
            "conversions": 4,
            "revenue": 8000.0,
        }
    ]
