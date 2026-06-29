import sys
import os
import uuid
from datetime import datetime
from kads.data.warehouse import db
from kads.data.warehouse.models import FactActionJournal, DimCampaignState

def seed_data():
    session = db.SessionLocal()

    # Ensure tables exist
    db.Base.metadata.create_all(bind=db.engine)

    # Clean existing data
    session.query(FactActionJournal).delete()
    session.query(DimCampaignState).delete()

    # Insert mock campaigns
    camp1 = DimCampaignState(
        campaign_id="g_brand_001",
        campaign_name="Google Search Brand",
        platform="google",
        status="enabled",
        budget=150.0,
        bid_strategy="tCPA"
    )
    camp2 = DimCampaignState(
        campaign_id="m_prospecting_002",
        campaign_name="Meta Prospecting",
        platform="meta",
        status="enabled",
        budget=450.0,
        bid_strategy="Lowest Cost"
    )
    session.add_all([camp1, camp2])
    
    # Insert mock actions
    action1 = FactActionJournal(
        action_id=f"act_{uuid.uuid4().hex[:8]}",
        platform="google",
        entity_type="budget",
        entity_id="g_brand_001",
        action_type="budget_increase",
        current_state={"budget": 150.0},
        proposed_state={"budget": 180.0},
        expected_impact="High ROAS detected (4.5x). Scaling budget by +20% to maximize conversions.",
        risk_score=0.15,
        confidence=0.88,
        requires_approval=True,
        approval_reason=["Bütçe artırımı eşiği aşıldı"],
        status="pending",
        rollback_plan={"budget": 150.0}
    )

    action2 = FactActionJournal(
        action_id=f"act_{uuid.uuid4().hex[:8]}",
        platform="meta",
        entity_type="campaign",
        entity_id="m_prospecting_002",
        action_type="pause",
        current_state={"status": "enabled"},
        proposed_state={"status": "paused"},
        expected_impact="3x Kill Rule Triggered: CPA > 6000 TL. Pausing campaign to stop budget bleed.",
        risk_score=0.45,
        confidence=0.95,
        requires_approval=True,
        approval_reason=["3x Kill Rule: CPA exceeds target threshold", "Campaign status mutation"],
        status="pending",
        rollback_plan={"status": "enabled"}
    )
    
    action3 = FactActionJournal(
        action_id=f"act_{uuid.uuid4().hex[:8]}",
        platform="google",
        entity_type="adgroup",
        entity_id="g_brand_001_ad_1",
        action_type="creative_test",
        current_state={"creative": "EXISTING_AD"},
        proposed_state={
            "headline": "Kozbeyli Konağı: 600 Yıllık Tarih Sizi Bekliyor",
            "description": "Doğa manzaralı odalarımız, yöresel Ege kahvaltımız ve tarihi atmosferimizle hizmetinizdeyiz. Hemen rezervasyon yapın."
        },
        expected_impact="Combat Ad Fatigue (CTR 1.20%). Generated new variant focusing on 'Tarihi Konak' and 'Ege Kahvaltısı' angles.",
        risk_score=0.10,
        confidence=0.90,
        requires_approval=True,
        approval_reason=["Ad fatigue detected, requires A/B test approval"],
        status="pending",
        rollback_plan={"creative": "EXISTING_AD"}
    )
    
    session.add_all([action1, action2, action3])
    session.commit()
    print("Seeded database with 2 mock campaigns and 3 pending actions.")
    session.close()

if __name__ == "__main__":
    seed_data()
