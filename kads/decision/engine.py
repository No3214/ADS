import uuid
from datetime import datetime, timedelta
from typing import List

from kads.core.schemas import ActionSchema
from kads.decision.anomaly import detect_anomalies
from kads.decision.creative import generate_ad_variant
from kads.decision.risk_score import calculate_risk_score
from kads.observability.health import audit_tracking_health


def run_agent_council(
    google_campaigns: List[dict], meta_campaigns: List[dict]
) -> List[ActionSchema]:
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
        cpa = spend / conversions if conversions > 0 else float("inf")

        # Heuristic 1: High ROAS -> Budget Increase
        if roas >= 3.0 and spend > 0:
            proposed_budget = round(current_budget * 1.2, 1)  # +20%
            action_data = {
                "action": "budget_increase",
                "daily_budget_try": proposed_budget,
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
                requires_approval=risk.required_action != "none"
                or (proposed_budget - current_budget > 50),
                approval_reason=risk.reasons
                + ["Manual budget increase threshold check"],
                rollback_plan={"budget": current_budget},
                expires_at=datetime.utcnow() + timedelta(hours=24),
                status="pending",
            )
            proposed_actions.append(action)

        # Heuristic 2: CPA > 3x Target CPA -> Pause Campaign (3x Kill Rule)
        elif cpa >= TARGET_CPA * 3 and spend > 500.0:
            action_data = {"action": "pause"}
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
                approval_reason=risk.reasons
                + ["3x Kill Rule triggered: CPA exceeds target"],
                rollback_plan={"status": c["status"]},
                expires_at=datetime.utcnow() + timedelta(hours=24),
                status="pending",
            )
            proposed_actions.append(action)

        # Heuristic 3: Ad Fatigue -> Generate Creative (A/B Test)
        # Low CTR but campaign is active and has spend.
        ctr = (c["clicks"] / c["impressions"]) * 100 if c["impressions"] > 0 else 0.0
        if 0 < ctr < 2.0 and spend > 100.0 and cpa < TARGET_CPA * 3:
            variant = generate_ad_variant(platform, camp_name)
            action_data = {"action": "creative_test"}
            risk = calculate_risk_score(action_data, tracking_score)

            action = ActionSchema(
                action_id=f"act_{uuid.uuid4().hex[:8]}",
                platform=platform,
                entity_type="adgroup",
                entity_id=f"{camp_id}_ad_1",
                action_type="creative_test",
                current_state={"creative": "EXISTING_AD"},
                proposed_state={
                    "headline": variant["headline"],
                    "description": variant["description"],
                },
                expected_impact=f"Combat Ad Fatigue (CTR {ctr:.2f}%). "
                + variant["rationale"],
                risk_score=risk.risk_score,
                confidence=0.90,
                requires_approval=True,  # Creative changes ALWAYS require approval
                approval_reason=risk.reasons
                + ["Ad fatigue detected, requires A/B test approval"],
                rollback_plan={"creative": "EXISTING_AD"},
                expires_at=datetime.utcnow() + timedelta(hours=72),
                status="pending",
            )
            proposed_actions.append(action)

    # Heuristic 4: Anomaly Detection -> Propose Emergency Pauses
    anomalies = detect_anomalies(all_campaigns)
    for anomaly in anomalies:
        camp_id = anomaly["campaign_id"]
        platform = anomaly["platform"]
        severity = anomaly["severity"]

        # Propose emergency pausing if it is a critical anomaly
        if severity == "CRITICAL":
            action_data = {"action": "pause"}
            # Unhealthy tracking health score increases risk to absolute maximum (0.99)
            risk = calculate_risk_score(action_data, tracking_score)

            action = ActionSchema(
                action_id=f"act_{uuid.uuid4().hex[:8]}",
                platform=platform,
                entity_type="campaign",
                entity_id=camp_id,
                action_type="pause",
                current_state={"status": "active"},
                proposed_state={"status": "PAUSED"},
                expected_impact=f"EMERGENCY PAUSE: {anomaly['details']}",
                risk_score=0.99,  # Absolute critical alert
                confidence=0.99,
                requires_approval=True,
                approval_reason=risk.reasons
                + [f"Operational Anomaly detected: {anomaly['type']}"],
                rollback_plan={"status": "active"},
                expires_at=datetime.utcnow() + timedelta(hours=12),
                status="pending",
            )
            proposed_actions.append(action)

    # Heuristic 5: Cross-Platform Budget Transfer
    # Automatically transfer 10% budget from low-performing campaigns (< 1.5 ROAS)
    # on one platform to high-performing campaigns (>= 3.0 ROAS) on the other.
    high_google = [
        c
        for c in google_campaigns
        if (c["revenue"] / c["spend"] if c["spend"] > 0 else 0) >= 3.0
    ]
    low_meta = [
        c
        for c in meta_campaigns
        if c["spend"] > 100.0
        and (c["revenue"] / c["spend"] if c["spend"] > 0 else 0) < 1.5
    ]

    for hg in high_google:
        for lm in low_meta:
            transfer_amount = round(lm["budget"] * 0.1, 1)
            if transfer_amount > 0:
                # Propose decrease for Meta
                dec_budget = round(lm["budget"] - transfer_amount, 1)
                dec_action_data = {
                    "action": "budget_decrease",
                    "daily_budget_try": dec_budget,
                }
                dec_risk = calculate_risk_score(dec_action_data, tracking_score)
                dec_action = ActionSchema(
                    action_id=f"act_{uuid.uuid4().hex[:8]}",
                    platform="meta",
                    entity_type="budget",
                    entity_id=lm["campaign_id"],
                    action_type="budget_decrease",
                    current_state={"budget": lm["budget"]},
                    proposed_state={"budget": dec_budget},
                    expected_impact=f"Reduce budget by -10% (-{transfer_amount} TL) to transfer to high-performing Google campaign ({hg['campaign_name']})",
                    risk_score=dec_risk.risk_score,
                    confidence=0.80,
                    requires_approval=True,
                    approval_reason=dec_risk.reasons
                    + ["Cross-platform budget transfer re-allocation"],
                    rollback_plan={"budget": lm["budget"]},
                    expires_at=datetime.utcnow() + timedelta(hours=24),
                    status="pending",
                )
                proposed_actions.append(dec_action)

                # Propose increase for Google
                inc_budget = round(hg["budget"] + transfer_amount, 1)
                inc_action_data = {
                    "action": "budget_increase",
                    "daily_budget_try": inc_budget,
                }
                inc_risk = calculate_risk_score(inc_action_data, tracking_score)
                inc_action = ActionSchema(
                    action_id=f"act_{uuid.uuid4().hex[:8]}",
                    platform="google",
                    entity_type="budget",
                    entity_id=hg["campaign_id"],
                    action_type="budget_increase",
                    current_state={"budget": hg["budget"]},
                    proposed_state={"budget": inc_budget},
                    expected_impact=f"Increase budget by +{transfer_amount} TL transferred from low-performing Meta campaign ({lm['campaign_name']})",
                    risk_score=inc_risk.risk_score,
                    confidence=0.80,
                    requires_approval=True,
                    approval_reason=inc_risk.reasons
                    + ["Cross-platform budget transfer allocation"],
                    rollback_plan={"budget": hg["budget"]},
                    expires_at=datetime.utcnow() + timedelta(hours=24),
                    status="pending",
                )
                proposed_actions.append(inc_action)

    # Do the same for high Meta -> low Google
    high_meta = [
        c
        for c in meta_campaigns
        if (c["revenue"] / c["spend"] if c["spend"] > 0 else 0) >= 3.0
    ]
    low_google = [
        c
        for c in google_campaigns
        if c["spend"] > 100.0
        and (c["revenue"] / c["spend"] if c["spend"] > 0 else 0) < 1.5
    ]

    for hm in high_meta:
        for lg in low_google:
            transfer_amount = round(lg["budget"] * 0.1, 1)
            if transfer_amount > 0:
                # Propose decrease for Google
                dec_budget = round(lg["budget"] - transfer_amount, 1)
                dec_action_data = {
                    "action": "budget_decrease",
                    "daily_budget_try": dec_budget,
                }
                dec_risk = calculate_risk_score(dec_action_data, tracking_score)
                dec_action = ActionSchema(
                    action_id=f"act_{uuid.uuid4().hex[:8]}",
                    platform="google",
                    entity_type="budget",
                    entity_id=lg["campaign_id"],
                    action_type="budget_decrease",
                    current_state={"budget": lg["budget"]},
                    proposed_state={"budget": dec_budget},
                    expected_impact=f"Reduce budget by -10% (-{transfer_amount} TL) to transfer to high-performing Meta campaign ({hm['campaign_name']})",
                    risk_score=dec_risk.risk_score,
                    confidence=0.80,
                    requires_approval=True,
                    approval_reason=dec_risk.reasons
                    + ["Cross-platform budget transfer re-allocation"],
                    rollback_plan={"budget": lg["budget"]},
                    expires_at=datetime.utcnow() + timedelta(hours=24),
                    status="pending",
                )
                proposed_actions.append(dec_action)

                # Propose increase for Meta
                inc_budget = round(hm["budget"] + transfer_amount, 1)
                inc_action_data = {
                    "action": "budget_increase",
                    "daily_budget_try": inc_budget,
                }
                inc_risk = calculate_risk_score(inc_action_data, tracking_score)
                inc_action = ActionSchema(
                    action_id=f"act_{uuid.uuid4().hex[:8]}",
                    platform="meta",
                    entity_type="budget",
                    entity_id=hm["campaign_id"],
                    action_type="budget_increase",
                    current_state={"budget": hm["budget"]},
                    proposed_state={"budget": inc_budget},
                    expected_impact=f"Increase budget by +{transfer_amount} TL transferred from low-performing Google campaign ({lg['campaign_name']})",
                    risk_score=inc_risk.risk_score,
                    confidence=0.80,
                    requires_approval=True,
                    approval_reason=inc_risk.reasons
                    + ["Cross-platform budget transfer allocation"],
                    rollback_plan={"budget": hm["budget"]},
                    expires_at=datetime.utcnow() + timedelta(hours=24),
                    status="pending",
                )
                proposed_actions.append(inc_action)

    # Sort proposed_actions by risk_score descending to keep the most critical alert in case of duplicates
    proposed_actions.sort(key=lambda x: x.risk_score, reverse=True)

    unique_actions = []
    seen = set()
    for action in proposed_actions:
        key = (
            action.platform,
            action.entity_type,
            action.entity_id,
            action.action_type,
        )
        if key not in seen:
            seen.add(key)
            unique_actions.append(action)

    return unique_actions
