import uuid
from datetime import datetime, timedelta
from typing import List
from kads.core.schemas import ActionSchema
from kads.decision.risk_score import calculate_risk_score
from kads.observability.health import audit_tracking_health

def run_agent_council(google_campaigns: List[dict], meta_campaigns: List[dict]) -> List[ActionSchema]:
    """
    Evaluates campaign performance snapshot and tracking health.
    Proposes budget adjustments or pausing campaigns.
    """
    proposed_actions = []
    
    # Audit tracking health
    tracking_info = audit_tracking_health()
    tracking_score = tracking_info["score"]

    # Target CPA for Kozbeyli Konağı is 2000 TL
    TARGET_CPA = 2000.0

    all_campaigns = google_campaigns + meta_campaigns

    for c in all_campaigns:
        camp_id = c["campaign_id"]
        camp_name = c["campaign_name"]
        platform = c["platform"]
        spend = c["spend"]
        conversions = c["conversions"]
        revenue = c["revenue"]
        current_budget = c["budget"]

        # Calculate ROAS and CPA
        roas = revenue / spend if spend > 0 else 0.0
        cpa = spend / conversions if conversions > 0 else float('inf')

        # Heuristic 1: High ROAS -> Budget Increase
        if roas >= 3.0 and spend > 0:
            proposed_budget = round(current_budget * 1.2, 1)  # +20%
            action_data = {
                "action": "budget_increase",
                "daily_budget_try": proposed_budget
            }
            risk = calculate_risk_score(action_data, tracking_score)
            
            action = ActionSchema(
                action_id=f"act_{uuid.uuid4().hex[:8]}",
                platform=platform,
                entity_type="budget",
                entity_id=camp_id,
                action_type="budget_increase",
                current_state={"budget": current_budget},
                proposed_state={"budget": proposed_budget},
                expected_impact=f"Scale budget by +20% due to high ROAS ({roas:.1f})",
                risk_score=risk.risk_score,
                confidence=0.85,
                requires_approval=risk.required_action != "none" or (proposed_budget - current_budget > 50),
                approval_reason=risk.reasons + ["Manual budget increase threshold check"],
                rollback_plan={"budget": current_budget},
                expires_at=datetime.utcnow() + timedelta(hours=24),
                status="pending"
            )
            proposed_actions.append(action)

        # Heuristic 2: CPA > 3x Target CPA -> Pause Campaign (3x Kill Rule)
        elif cpa >= TARGET_CPA * 3 and spend > 500.0:
            action_data = {
                "action": "pause"
            }
            risk = calculate_risk_score(action_data, tracking_score)
            
            action = ActionSchema(
                action_id=f"act_{uuid.uuid4().hex[:8]}",
                platform=platform,
                entity_type="campaign",
                entity_id=camp_id,
                action_type="pause",
                current_state={"status": c["status"]},
                proposed_state={"status": "PAUSED"},
                expected_impact=f"Stop budget bleed. CPA ({cpa:.0f} TL) is 3x higher than target ({TARGET_CPA} TL)",
                risk_score=risk.risk_score,
                confidence=0.95,
                requires_approval=True,  # Pausing active campaign always needs approval
                approval_reason=risk.reasons + ["3x Kill Rule triggered: CPA exceeds target"],
                rollback_plan={"status": c["status"]},
                expires_at=datetime.utcnow() + timedelta(hours=24),
                status="pending"
            )
            proposed_actions.append(action)

    return proposed_actions
