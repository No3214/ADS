import uuid
from datetime import datetime, timedelta
from typing import List, Dict

from kads.core.schemas import ActionSchema
from kads.decision.anomaly import detect_anomalies
from kads.decision.creative import generate_ad_variant
from kads.decision.risk_score import calculate_risk_score
from kads.decision.mmm import calculate_saturation_point
from kads.observability.health import audit_tracking_health

# Target CPA for Kozbeyli Konağı is 2000 TL
TARGET_CPA = 2000.0

class BaseAgent:
    def __init__(self, name: str):
        self.name = name

class AnalystAgent(BaseAgent):
    """Responsible for monitoring performance, ROAS, CPA, and Anomalies."""
    def __init__(self):
        super().__init__("AnalystAgent")

    def evaluate(self, campaigns: List[Dict], tracking_score: float) -> List[ActionSchema]:
        """Analist: anomali + 3x-kill kuralıyla kampanyaları değerlendirir; önerilen aksiyonları döndürür."""
        actions = []
        # Check Anomalies
        anomalies = detect_anomalies(campaigns)
        for anomaly in anomalies:
            if anomaly["severity"] == "CRITICAL":
                risk = calculate_risk_score({"action": "pause"}, tracking_score)
                action = ActionSchema(
                    action_id=f"act_{uuid.uuid4().hex[:8]}",
                    platform=anomaly["platform"],
                    entity_type="campaign",
                    entity_id=anomaly["campaign_id"],
                    action_type="pause",
                    current_state={"status": "active"},
                    proposed_state={"status": "PAUSED"},
                    expected_impact=f"EMERGENCY PAUSE: {anomaly['details']}",
                    risk_score=0.99,
                    confidence=0.99,
                    requires_approval=True,
                    approval_reason=risk.reasons + [f"Analyst Agent: Critical Anomaly {anomaly['type']}"],
                    rollback_plan={"status": "active"},
                    expires_at=datetime.utcnow() + timedelta(hours=12),
                    status="pending",
                )
                actions.append(action)

        for c in campaigns:
            spend = c["spend"]
            conversions = c["conversions"]
            cpa = spend / conversions if conversions > 0 else float("inf")
            
            # 3x Kill Rule
            if cpa >= TARGET_CPA * 3 and spend > 500.0:
                risk = calculate_risk_score({"action": "pause"}, tracking_score)
                action = ActionSchema(
                    action_id=f"act_{uuid.uuid4().hex[:8]}",
                    platform=c["platform"],
                    entity_type="campaign",
                    entity_id=c["campaign_id"],
                    action_type="pause",
                    current_state={"status": c["status"]},
                    proposed_state={"status": "PAUSED"},
                    expected_impact=f"Stop budget bleed. CPA ({cpa:.0f} TL) > 3x target.",
                    risk_score=risk.risk_score,
                    confidence=0.95,
                    requires_approval=True,
                    approval_reason=risk.reasons + ["Analyst Agent: 3x Kill Rule"],
                    rollback_plan={"status": c["status"]},
                    expires_at=datetime.utcnow() + timedelta(hours=24),
                    status="pending",
                )
                actions.append(action)
        return actions

class CreativeAgent(BaseAgent):
    """Responsible for monitoring Ad Fatigue and proposing A/B tests."""
    def __init__(self):
        super().__init__("CreativeAgent")

    def evaluate(self, campaigns: List[Dict], tracking_score: float) -> List[ActionSchema]:
        """Kreatif: düşük CTR + reklam yorgunluğu sinyaliyle A/B testi önerir."""
        actions = []
        for c in campaigns:
            spend = c["spend"]
            cpa = spend / c["conversions"] if c["conversions"] > 0 else float("inf")
            ctr = (c["clicks"] / c["impressions"]) * 100 if c["impressions"] > 0 else 0.0
            
            if 0 < ctr < 2.0 and spend > 100.0 and cpa < TARGET_CPA * 3:
                variant = generate_ad_variant(c["platform"], c["campaign_name"])
                risk = calculate_risk_score({"action": "creative_test"}, tracking_score)
                action = ActionSchema(
                    action_id=f"act_{uuid.uuid4().hex[:8]}",
                    platform=c["platform"],
                    entity_type="adgroup",
                    entity_id=f"{c['campaign_id']}_ad_1",
                    action_type="creative_test",
                    current_state={"creative": "EXISTING_AD"},
                    proposed_state={"headline": variant["headline"], "description": variant["description"]},
                    expected_impact=f"Combat Ad Fatigue (CTR {ctr:.2f}%). " + variant["rationale"],
                    risk_score=risk.risk_score,
                    confidence=0.90,
                    requires_approval=True,
                    approval_reason=risk.reasons + ["Creative Agent: Ad fatigue detected"],
                    rollback_plan={"creative": "EXISTING_AD"},
                    expires_at=datetime.utcnow() + timedelta(hours=72),
                    status="pending",
                )
                actions.append(action)
        return actions

class StrategistAgent(BaseAgent):
    """Responsible for budget allocation, saturation modeling, and cross-platform transfers."""
    def __init__(self):
        super().__init__("StrategistAgent")

    def evaluate(self, google_campaigns: List[Dict], meta_campaigns: List[Dict], tracking_score: float) -> List[ActionSchema]:
        """Stratejist: MMM doygunluğuyla ölçekleme + platformlar arası bütçe transferi önerir."""
        actions = []
        all_camps = google_campaigns + meta_campaigns
        
        # Scale high performers using MMM saturation
        for c in all_camps:
            spend = c["spend"]
            revenue = c["revenue"]
            current_budget = c["budget"]
            roas = revenue / spend if spend > 0 else 0.0
            
            if roas >= 3.0 and spend > 0:
                sat_data = calculate_saturation_point(spend, revenue)
                if sat_data["status"] == "scalable":
                    proposed_budget = sat_data["suggested_cap"]
                    # Limit max increase to +50% per day for safety
                    proposed_budget = min(proposed_budget, current_budget * 1.5)
                    if proposed_budget > current_budget:
                        risk = calculate_risk_score({"action": "budget_increase", "daily_budget_try": proposed_budget}, tracking_score)
                        action = ActionSchema(
                            action_id=f"act_{uuid.uuid4().hex[:8]}",
                            platform=c["platform"],
                            entity_type="budget",
                            entity_id=c["campaign_id"],
                            action_type="budget_increase",
                            current_state={"budget": current_budget},
                            proposed_state={"budget": proposed_budget},
                            expected_impact=f"Scale budget (MMM Scalable). ROAS: {roas:.1f}, Decay: {sat_data['roas_decay_rate']}",
                            risk_score=risk.risk_score,
                            confidence=0.85,
                            requires_approval=risk.required_action != "none" or (proposed_budget - current_budget > 50),
                            approval_reason=risk.reasons + ["Strategist Agent: MMM Scalable Check"],
                            rollback_plan={"budget": current_budget},
                            expires_at=datetime.utcnow() + timedelta(hours=24),
                            status="pending",
                        )
                        actions.append(action)

        # Cross Platform Transfer (Google High -> Meta Low)
        high_google = [c for c in google_campaigns if (c["revenue"]/c["spend"] if c["spend"]>0 else 0) >= 3.0]
        low_meta = [c for c in meta_campaigns if c["spend"] > 100.0 and (c["revenue"]/c["spend"] if c["spend"]>0 else 0) < 1.5]
        
        for hg in high_google:
            for lm in low_meta:
                transfer_amount = round(lm["budget"] * 0.1, 1)
                if transfer_amount > 0:
                    dec_budget = round(lm["budget"] - transfer_amount, 1)
                    risk_dec = calculate_risk_score({"action": "budget_decrease", "daily_budget_try": dec_budget}, tracking_score)
                    actions.append(ActionSchema(
                        action_id=f"act_{uuid.uuid4().hex[:8]}",
                        platform="meta", entity_type="budget", entity_id=lm["campaign_id"], action_type="budget_decrease",
                        current_state={"budget": lm["budget"]}, proposed_state={"budget": dec_budget},
                        expected_impact=f"Strategist Agent: Transfer -{transfer_amount} TL to Google {hg['campaign_name']}",
                        risk_score=risk_dec.risk_score, confidence=0.8, requires_approval=True,
                        approval_reason=risk_dec.reasons + ["Cross-platform transfer decrease"],
                        rollback_plan={"budget": lm["budget"]}, expires_at=datetime.utcnow() + timedelta(hours=24), status="pending"
                    ))
                    
                    inc_budget = round(hg["budget"] + transfer_amount, 1)
                    risk_inc = calculate_risk_score({"action": "budget_increase", "daily_budget_try": inc_budget}, tracking_score)
                    actions.append(ActionSchema(
                        action_id=f"act_{uuid.uuid4().hex[:8]}",
                        platform="google", entity_type="budget", entity_id=hg["campaign_id"], action_type="budget_increase",
                        current_state={"budget": hg["budget"]}, proposed_state={"budget": inc_budget},
                        expected_impact=f"Strategist Agent: Transfer +{transfer_amount} TL from Meta {lm['campaign_name']}",
                        risk_score=risk_inc.risk_score, confidence=0.8, requires_approval=True,
                        approval_reason=risk_inc.reasons + ["Cross-platform transfer increase"],
                        rollback_plan={"budget": hg["budget"]}, expires_at=datetime.utcnow() + timedelta(hours=24), status="pending"
                    ))
                    
        # Cross Platform Transfer (Meta High -> Google Low)
        high_meta = [c for c in meta_campaigns if (c["revenue"]/c["spend"] if c["spend"]>0 else 0) >= 3.0]
        low_google = [c for c in google_campaigns if c["spend"] > 100.0 and (c["revenue"]/c["spend"] if c["spend"]>0 else 0) < 1.5]
        
        for hm in high_meta:
            for lg in low_google:
                transfer_amount = round(lg["budget"] * 0.1, 1)
                if transfer_amount > 0:
                    dec_budget = round(lg["budget"] - transfer_amount, 1)
                    risk_dec = calculate_risk_score({"action": "budget_decrease", "daily_budget_try": dec_budget}, tracking_score)
                    actions.append(ActionSchema(
                        action_id=f"act_{uuid.uuid4().hex[:8]}",
                        platform="google", entity_type="budget", entity_id=lg["campaign_id"], action_type="budget_decrease",
                        current_state={"budget": lg["budget"]}, proposed_state={"budget": dec_budget},
                        expected_impact=f"Strategist Agent: Transfer -{transfer_amount} TL to Meta {hm['campaign_name']}",
                        risk_score=risk_dec.risk_score, confidence=0.8, requires_approval=True,
                        approval_reason=risk_dec.reasons + ["Cross-platform transfer decrease"],
                        rollback_plan={"budget": lg["budget"]}, expires_at=datetime.utcnow() + timedelta(hours=24), status="pending"
                    ))
                    
                    inc_budget = round(hm["budget"] + transfer_amount, 1)
                    risk_inc = calculate_risk_score({"action": "budget_increase", "daily_budget_try": inc_budget}, tracking_score)
                    actions.append(ActionSchema(
                        action_id=f"act_{uuid.uuid4().hex[:8]}",
                        platform="meta", entity_type="budget", entity_id=hm["campaign_id"], action_type="budget_increase",
                        current_state={"budget": hm["budget"]}, proposed_state={"budget": inc_budget},
                        expected_impact=f"Strategist Agent: Transfer +{transfer_amount} TL from Google {lg['campaign_name']}",
                        risk_score=risk_inc.risk_score, confidence=0.8, requires_approval=True,
                        approval_reason=risk_inc.reasons + ["Cross-platform transfer increase"],
                        rollback_plan={"budget": hm["budget"]}, expires_at=datetime.utcnow() + timedelta(hours=24), status="pending"
                    ))
                    
        return actions

def run_agent_council(
    google_campaigns: List[dict], meta_campaigns: List[dict]
) -> List[ActionSchema]:
    """
    KADS v3.0 L99 God Tier: Concurrent Multi-Agent Council
    Evaluates campaign performance snapshot via specialized agents running in parallel.
    This simulates a true Compound AI Swarm where agents process state asynchronously.
    """
    import concurrent.futures

    proposed_actions = []
    
    tracking_info = audit_tracking_health()
    tracking_score = tracking_info["score"]
    
    all_campaigns = google_campaigns + meta_campaigns

    # Initialize the Council
    analyst = AnalystAgent()
    creative = CreativeAgent()
    strategist = StrategistAgent()

    # Define execution wrappers
    def run_analyst():
        """Analist ajanı thread havuzunda çalıştırır."""
        return analyst.evaluate(all_campaigns, tracking_score)
        
    def run_creative():
        """Kreatif ajanı thread havuzunda çalıştırır."""
        return creative.evaluate(all_campaigns, tracking_score)
        
    def run_strategist():
        """Stratejist ajanı thread havuzunda çalıştırır."""
        return strategist.evaluate(google_campaigns, meta_campaigns, tracking_score)

    # Execute agents concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_analyst = executor.submit(run_analyst)
        future_creative = executor.submit(run_creative)
        future_strategist = executor.submit(run_strategist)
        
        # Gather results as they complete
        for future in concurrent.futures.as_completed([future_analyst, future_creative, future_strategist]):
            try:
                actions = future.result()
                proposed_actions.extend(actions)
            except Exception as e:
                # Fallback to avoid crashing the whole council if one agent fails
                print(f"[Council Error] Agent failed during evaluation: {e}")
    
    # Sort by risk score (highest risk / most critical first)
    proposed_actions.sort(key=lambda x: x.risk_score, reverse=True)

    # Deduplicate actions (if multiple agents propose identical changes)
    unique_actions = []
    seen = set()
    for action in proposed_actions:
        key = (action.platform, action.entity_type, action.entity_id, action.action_type)
        if key not in seen:
            seen.add(key)
            unique_actions.append(action)

    return unique_actions
