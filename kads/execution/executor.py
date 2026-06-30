import logging
from datetime import datetime

from sqlalchemy.orm import Session

from kads.data.warehouse.models import DimCampaignState, FactActionJournal

logger = logging.getLogger("kads.execution")


def execute_action(action: FactActionJournal, db: Session) -> bool:
    """
    Executes an approved action. Simulates platform mutation in dry-run mode,
    updates dim_campaign_state in warehouse, and updates Action status to 'executed'.
    """
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
