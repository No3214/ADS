from typing import List


def detect_anomalies(campaigns: List[dict]) -> List[dict]:
    """
    Scans campaign metrics for critical operational anomalies.
    Returns a list of detected anomalies.
    """
    anomalies = []

    for c in campaigns:
        camp_id = c["campaign_id"]
        camp_name = c["campaign_name"]
        platform = c["platform"]
        spend = c["spend"]
        clicks = c["clicks"]
        impressions = c["impressions"]
        conversions = c["conversions"]
        status = c.get("status", "active")

        if status != "active":
            continue

        # 1. Conversion Bleed: High spend but exactly zero conversions
        if spend >= 1000.0 and conversions == 0:
            anomalies.append(
                {
                    "campaign_id": camp_id,
                    "campaign_name": camp_name,
                    "platform": platform,
                    "type": "conversion_bleed",
                    "details": f"Zero conversions despite high spend ({spend:.0f} TL). Possible tracking failure or booking engine downtime.",
                    "severity": "CRITICAL",
                }
            )

        # 2. CPC Spike: Clicks occurred but cost per click is abnormally high (> 150 TL)
        if clicks >= 5:
            cpc = spend / clicks
            if cpc > 150.0:
                anomalies.append(
                    {
                        "campaign_id": camp_id,
                        "campaign_name": camp_name,
                        "platform": platform,
                        "type": "cpc_spike",
                        "details": f"Abnormally high CPC detected ({cpc:.1f} TL). Threshold is 150 TL.",
                        "severity": "WARNING",
                    }
                )

        # 3. Click Drop: Zero clicks despite high impressions (broken ad assets or link mismatch)
        if impressions >= 500 and clicks == 0:
            anomalies.append(
                {
                    "campaign_id": camp_id,
                    "campaign_name": camp_name,
                    "platform": platform,
                    "type": "click_drop",
                    "details": "Zero clicks received despite over 500 impressions. Possible broken link or landing page error.",
                    "severity": "CRITICAL",
                }
            )

    return anomalies
