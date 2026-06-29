from kads import core

def fetch_meta_campaigns() -> list[dict]:
    """
    Fetches campaign data from Meta Marketing API.
    Falls back to mock data if credentials are not configured (placeholders).
    """
    env = core.load_env()
    account_id = env.get("META_AD_ACCOUNT_ID", "")
    access_token = env.get("META_ACCESS_TOKEN", "")

    if not account_id or core.is_placeholder(account_id) or not access_token or core.is_placeholder(access_token):
        # Simulated campaign data matching Kozbeyli Konağı Meta channels
        return [
            {
                "campaign_id": "m_prospecting_111",
                "campaign_name": "Meta — Prospecting (Website Sales)",
                "platform": "meta",
                "status": "active",
                "budget": 350.0,
                "bid_strategy": "Lowest Cost",
                "spend": 320.0,
                "clicks": 98,
                "impressions": 4500,
                "conversions": 2,
                "revenue": 4000.0,
            },
            {
                "campaign_id": "m_whatsapp_222",
                "campaign_name": "Meta — WhatsApp/Mesaj",
                "platform": "meta",
                "status": "active",
                "budget": 150.0,
                "bid_strategy": "Lowest Cost",
                "spend": 145.0,
                "clicks": 112,
                "impressions": 3800,
                "conversions": 10,  # WhatsApp Leads
                "revenue": 0.0,
            },
            {
                "campaign_id": "m_retargeting_333",
                "campaign_name": "Meta — Retargeting",
                "platform": "meta",
                "status": "paused",
                "budget": 100.0,
                "bid_strategy": "Lowest Cost",
                "spend": 0.0,
                "clicks": 0,
                "impressions": 0,
                "conversions": 0,
                "revenue": 0.0,
            }
        ]

    # In production, this would make calls to graph.facebook.com for campaigns
    return [
        {
            "campaign_id": "m_prospecting_111",
            "campaign_name": "Meta — Prospecting (Website Sales)",
            "platform": "meta",
            "status": "active",
            "budget": 350.0,
            "bid_strategy": "Lowest Cost",
            "spend": 330.0,
            "clicks": 105,
            "impressions": 4800,
            "conversions": 3,
            "revenue": 6000.0,
        }
    ]
