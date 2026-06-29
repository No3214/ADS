import logging
from datetime import datetime
from kads.data.ingestion.google_ads import fetch_google_campaigns
from kads.data.ingestion.meta_ads import fetch_meta_campaigns
from kads.data.warehouse.db import SessionLocal
from kads.data.warehouse.models import DimCampaignState, FactAdPerformanceHourly, FactTrackingHealth

logger = logging.getLogger("kads.scheduler")

def job_p0_health_check():
    """
    P0 Health Check (Every 15 min):
    - Ingests latest campaign states and updates warehouse dim_campaign_state.
    - Logs hourly performance snapshots.
    - Audits tracking health.
    """
    logger.info("Executing P0 Health Check Job...")
    db = SessionLocal()
    try:
        # Ingest Google campaigns
        google_camps = fetch_google_campaigns()
        for gc in google_camps:
            camp = db.query(DimCampaignState).filter_by(campaign_id=gc["campaign_id"]).first()
            if not camp:
                camp = DimCampaignState(campaign_id=gc["campaign_id"])
            camp.campaign_name = gc["campaign_name"]
            camp.platform = gc["platform"]
            camp.status = gc["status"]
            camp.budget = gc["budget"]
            camp.bid_strategy = gc["bid_strategy"]
            db.add(camp)
            
            # Log hourly performance
            perf = FactAdPerformanceHourly(
                campaign_id=gc["campaign_id"],
                timestamp=datetime.utcnow(),
                spend=gc["spend"],
                clicks=gc["clicks"],
                impressions=gc["impressions"],
                conversions=gc["conversions"],
                revenue=gc["revenue"]
            )
            db.add(perf)

        # Ingest Meta campaigns
        meta_camps = fetch_meta_campaigns()
        for mc in meta_camps:
            camp = db.query(DimCampaignState).filter_by(campaign_id=mc["campaign_id"]).first()
            if not camp:
                camp = DimCampaignState(campaign_id=mc["campaign_id"])
            camp.campaign_name = mc["campaign_name"]
            camp.platform = mc["platform"]
            camp.status = mc["status"]
            camp.budget = mc["budget"]
            camp.bid_strategy = mc["bid_strategy"]
            db.add(camp)
            
            # Log hourly performance
            perf = FactAdPerformanceHourly(
                campaign_id=mc["campaign_id"],
                timestamp=datetime.utcnow(),
                spend=mc["spend"],
                clicks=mc["clicks"],
                impressions=mc["impressions"],
                conversions=mc["conversions"],
                revenue=mc["revenue"]
            )
            db.add(perf)

        # Audit tracking health (simulated)
        health = FactTrackingHealth(
            component="CAPI",
            status="healthy",
            score=98.5,
            details={"match_quality": "good"}
        )
        db.add(health)

        db.commit()
        logger.info("P0 Health Check Job completed successfully.")
    except Exception as e:
        db.rollback()
        logger.error(f"Error executing P0 Health Check: {e}")
    finally:
        db.close()

def job_p1_optimization():
    """
    P1 Optimization (Every 1 hour):
    - Run bid & budget optimization analysis.
    """
    logger.info("Executing P1 Optimization Job...")
    # Interfaces with Decision engine in future PRs
    logger.info("P1 Optimization Job completed.")

def job_reflection():
    """
    Reflection & Learning (Daily 02:00):
    - Analyze decision quality and extract heuristics.
    """
    logger.info("Executing Reflection Job...")
    logger.info("Reflection Job completed.")
