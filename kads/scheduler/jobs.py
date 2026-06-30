import logging
from datetime import datetime

from kads.data.ingestion.google_ads import fetch_google_campaigns
from kads.data.ingestion.meta_ads import fetch_meta_campaigns
from kads.data.warehouse.db import SessionLocal
from kads.data.warehouse.models import (DimCampaignState, FactActionJournal,
                                        FactAdPerformanceHourly,
                                        FactTrackingHealth)

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
            camp = (
                db.query(DimCampaignState)
                .filter_by(campaign_id=gc["campaign_id"])
                .first()
            )
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
                revenue=gc["revenue"],
            )
            db.add(perf)

        # Ingest Meta campaigns
        meta_camps = fetch_meta_campaigns()
        for mc in meta_camps:
            camp = (
                db.query(DimCampaignState)
                .filter_by(campaign_id=mc["campaign_id"])
                .first()
            )
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
                revenue=mc["revenue"],
            )
            db.add(perf)

        # Audit tracking health (simulated)
        health = FactTrackingHealth(
            component="CAPI",
            status="healthy",
            score=98.5,
            details={"match_quality": "good"},
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
    - Fetches latest campaign data from both platforms.
    - Runs Agent Council (Decision Engine) to produce proposed actions.
    - Persists new pending actions into the warehouse for dashboard review.
    """
    from kads.decision.engine import run_agent_council

    logger.info("Executing P1 Optimization Job...")
    db = SessionLocal()
    try:
        google_camps = fetch_google_campaigns()
        meta_camps = fetch_meta_campaigns()

        proposed_actions = run_agent_council(google_camps, meta_camps)
        new_count = 0

        for action in proposed_actions:
            # Skip if an identical pending action already exists (avoid duplicates across runs)
            existing = (
                db.query(FactActionJournal)
                .filter_by(
                    entity_id=action.entity_id,
                    action_type=action.action_type,
                    status="pending",
                )
                .first()
            )
            if existing:
                continue

            record = FactActionJournal(
                action_id=action.action_id,
                platform=action.platform,
                entity_type=action.entity_type,
                entity_id=action.entity_id,
                action_type=action.action_type,
                current_state=action.current_state,
                proposed_state=action.proposed_state,
                expected_impact=action.expected_impact,
                risk_score=action.risk_score,
                confidence=action.confidence,
                requires_approval=action.requires_approval,
                approval_reason=action.approval_reason,
                rollback_plan=action.rollback_plan,
                status=action.status,
            )
            db.add(record)
            new_count += 1

        db.commit()
        logger.info(
            f"P1 Optimization Job completed. {new_count} new actions proposed, {len(proposed_actions) - new_count} duplicates skipped."
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Error executing P1 Optimization: {e}")
    finally:
        db.close()


def job_reflection():
    """
    Reflection & Learning (Daily 02:00):
    - Calls Memory module to review executed actions and extract lessons.
    - Logs lessons for future heuristic improvement.
    """
    from kads.memory.decision_memory import reflect_on_past_actions

    logger.info("Executing Reflection Job...")
    db = SessionLocal()
    try:
        lessons = reflect_on_past_actions(db)
        for lesson in lessons:
            logger.info(
                f"Lesson [{lesson['action_id']}]: {lesson['lesson']} (quality: {lesson['decision_quality']})"
            )
        logger.info(f"Reflection Job completed. {len(lessons)} lessons extracted.")
    except Exception as e:
        logger.error(f"Error executing Reflection Job: {e}")
    finally:
        db.close()
