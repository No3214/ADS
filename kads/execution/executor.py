import logging
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from kads.data.warehouse.models import DimCampaignState, FactActionJournal, FactTrackingHealth

logger = logging.getLogger("kads.execution")


def is_circuit_breaker_tripped(db: Session) -> bool:
    """
    Checks if the system execution circuit breaker is tripped.
    Trips if there are 2 or more failed actions in the last 24 hours.
    """
    one_day_ago = datetime.utcnow() - timedelta(days=1)
    failed_count = db.query(FactActionJournal).filter(
        FactActionJournal.status == "failed",
        FactActionJournal.executed_at >= one_day_ago
    ).count()

    if failed_count >= 2:
        logger.critical(f"CIRCUIT BREAKER TRIPPED! {failed_count} execution failures in the last 24 hours. Halting all executions.")
        
        # Log to tracking health
        health_record = db.query(FactTrackingHealth).filter_by(component="CircuitBreaker").first()
        if not health_record:
            health_record = FactTrackingHealth(component="CircuitBreaker")
        health_record.status = "error"
        health_record.score = 0.0
        health_record.timestamp = datetime.utcnow()
        health_record.details = {"failures_24h": failed_count, "status": "tripped"}
        db.add(health_record)
        db.commit()
        return True
    return False


def execute_action(action: FactActionJournal, db: Session) -> bool:
    """
    Executes an approved action. Simulates platform mutation in dry-run mode,
    updates dim_campaign_state in warehouse, and updates Action status to 'executed'.
    """
    if is_circuit_breaker_tripped(db):
        logger.error(f"Cannot execute action {action.action_id} because the execution circuit breaker is TRIPPED.")
        return False

    if action.status != "approved":
        logger.warning(
            f"Action {action.action_id} cannot be executed because status is {action.status}"
        )
        return False

    logger.info(
        f"Executing action {action.action_id}: {action.action_type} on {action.platform} {action.entity_type} {action.entity_id}"
    )

    try:
        # Simulate execution / local state mutation
        if action.entity_type == "campaign":
            camp = (
                db.query(DimCampaignState)
                .filter_by(campaign_id=action.entity_id)
                .first()
            )
            if camp:
                proposed_status = action.proposed_state.get("status")
                if proposed_status:
                    camp.status = proposed_status.lower()

        elif action.entity_type == "budget":
            camp = (
                db.query(DimCampaignState)
                .filter_by(campaign_id=action.entity_id)
                .first()
            )
            if camp:
                proposed_budget = action.proposed_state.get("budget")
                if proposed_budget is not None:
                    camp.budget = float(proposed_budget)

        action.status = "executed"
        action.executed_at = datetime.utcnow()
        db.commit()
        logger.info(f"Action {action.action_id} executed successfully.")
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to execute action {action.action_id}: {e}")
        action.status = "failed"
        action.executed_at = datetime.utcnow()  # Ensure timestamp is set for failure tracking
        db.commit()
        return False


def rollback_action(action: FactActionJournal, db: Session) -> bool:
    """
    Rolls back an executed action using its rollback_plan.
    """
    if action.status != "executed":
        logger.warning(
            f"Action {action.action_id} cannot be rolled back because status is {action.status}"
        )
        return False

    logger.info(f"Rolling back action {action.action_id}...")

    try:
        if action.entity_type == "campaign":
            camp = (
                db.query(DimCampaignState)
                .filter_by(campaign_id=action.entity_id)
                .first()
            )
            if camp:
                original_status = action.rollback_plan.get(
                    "status"
                ) or action.current_state.get("status")
                if original_status:
                    camp.status = original_status.lower()

        elif action.entity_type == "budget":
            camp = (
                db.query(DimCampaignState)
                .filter_by(campaign_id=action.entity_id)
                .first()
            )
            if camp:
                original_budget = action.rollback_plan.get(
                    "budget"
                ) or action.current_state.get("budget")
                if original_budget is not None:
                    camp.budget = float(original_budget)

        action.status = "rolled_back"
        db.commit()
        logger.info(f"Action {action.action_id} rolled back successfully.")
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to rollback action {action.action_id}: {e}")
        return False
