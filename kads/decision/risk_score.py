from typing import Any, Dict, List

from kads.core.schemas import RiskSchema


def calculate_risk_score(action: dict, tracking_score: float = 100.0) -> RiskSchema:
    """
    Calculates a risk score between 0.0 and 1.0 based on proposed action parameters
    and tracking health. Returns a validated RiskSchema.
    """
    score = 0.0
    reasons = []

    # 1. Budget Impact
    daily_budget = action.get("daily_budget_try")
    if daily_budget is not None:
        try:
            budget_val = float(daily_budget)
            if budget_val > 400:
                score += 0.25
                reasons.append("High daily budget impact (> 400 TL)")
            elif budget_val > 200:
                score += 0.15
                reasons.append("Medium daily budget impact (> 200 TL)")
        except (ValueError, TypeError):
            score += 0.3
            reasons.append("Invalid or unparseable budget value")

    # 2. Tracking uncertainty
    if tracking_score < 80.0:
        score += 0.3
        reasons.append(f"Low tracking health score ({tracking_score})")
    elif tracking_score < 95.0:
        score += 0.1
        reasons.append(f"Suboptimal tracking health score ({tracking_score})")

    # 3. Novelty (e.g. creating new campaigns)
    action_type = action.get("action_type") or action.get("action")
    if action_type in ("create_campaign", "create_adset", "create_ad"):
        score += 0.2
        reasons.append(f"Entity creation action: {action_type}")

    # 4. Volatility / Status changes
    if action_type in ("enable", "resume", "activate", "unpause"):
        score += 0.15
        reasons.append("Activating a paused campaign/entity")

    # Clamp score between 0.0 and 1.0
    score = min(1.0, max(0.0, score))

    # Risk level classification
    if score >= 0.75:
        level = "critical"
        req_action = "block"
    elif score >= 0.5:
        level = "high"
        req_action = "human_approval"
    elif score >= 0.2:
        level = "medium"
        req_action = "human_approval"
    else:
        level = "low"
        req_action = "none"

    return RiskSchema(
        risk_score=round(score, 2),
        risk_level=level,
        reasons=reasons,
        required_action=req_action,
    )
