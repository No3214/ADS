import logging
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from enum import Enum

from kads.data.warehouse.models import DimCampaignState, FactActionJournal, FactTrackingHealth

logger = logging.getLogger("kads.execution")


class CircuitBreakerState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half-open"

def get_circuit_breaker_state(db: Session) -> CircuitBreakerState:
    """
    Evaluates the system execution circuit breaker state.
    - OPEN: >= 2 failures in the last 24h, and last failure is < 1h ago.
    - HALF_OPEN: >= 2 failures in the last 24h, but last failure is >= 1h ago.
    - CLOSED: < 2 failures in the last 24h.
    """
    one_day_ago = datetime.utcnow() - timedelta(days=1)
    failures = db.query(FactActionJournal).filter(
        FactActionJournal.status == "failed",
        FactActionJournal.executed_at >= one_day_ago
    ).order_by(FactActionJournal.executed_at.desc()).all()

    failed_count = len(failures)

    if failed_count >= 2:
        last_failure_time = failures[0].executed_at
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        
        if last_failure_time and last_failure_time >= one_hour_ago:
            state = CircuitBreakerState.OPEN
            logger.critical(f"CIRCUIT BREAKER TRIPPED (OPEN)! {failed_count} failures in 24h. Last failure at {last_failure_time}")
        else:
            state = CircuitBreakerState.HALF_OPEN
            logger.warning(f"CIRCUIT BREAKER HALF-OPEN. {failed_count} failures, but last was > 1h ago. Allowing restricted execution.")
        
        # Log to tracking health
        health_record = db.query(FactTrackingHealth).filter_by(component="CircuitBreaker").first()
        if not health_record:
            health_record = FactTrackingHealth(component="CircuitBreaker")
        health_record.status = state.value
        health_record.score = 0.5 if state == CircuitBreakerState.HALF_OPEN else 0.0
        health_record.timestamp = datetime.utcnow()
        health_record.details = {"failures_24h": failed_count, "state": state.value}
        db.add(health_record)
        db.commit()
        return state
        
    return CircuitBreakerState.CLOSED

def is_circuit_breaker_tripped(db: Session) -> bool:
    """Geriye-uyumluluk: devre kesici OPEN durumundaysa True (aksiyon yürütme durur)."""
    return get_circuit_breaker_state(db) == CircuitBreakerState.OPEN


def execute_action(action: FactActionJournal, db: Session) -> bool:
    """
    Executes an approved action. Simulates platform mutation in dry-run mode,
    updates dim_campaign_state in warehouse, and updates Action status to 'executed'.
    """
    cb_state = get_circuit_breaker_state(db)
    if cb_state == CircuitBreakerState.OPEN:
        logger.error(f"Cannot execute action {action.action_id} because the execution circuit breaker is OPEN.")
        return False
        
    if cb_state == CircuitBreakerState.HALF_OPEN:
        # In Half-Open state, we restrict budget increases or dangerous mutations.
        if action.entity_type == "budget" or action.action_type not in ["pause"]:
            logger.error(f"Cannot execute {action.action_type} on {action.entity_type} {action.action_id} in HALF-OPEN state. Restricted to low-risk ops.")
            return False

    if action.status != "approved":
        logger.warning(
            f"Action {action.action_id} cannot be executed because status is {action.status}"
        )
        return False

    # GUARDRAIL (defense-in-depth): bütçe-tavanı + flapping. Executor simülasyon olsa da
    # warehouse aynası tavanı aşmamalı; gerçek yürütme eklenince koruma zaten yerinde olur.
    if action.entity_type == "budget":
        from kads.core.security import load_security_config
        _cfg = load_security_config()
        _cap = _cfg["google_daily_try"] if (action.platform or "").lower() == "google" else _cfg["meta_daily_try"]
        _proposed = (action.proposed_state or {}).get("budget")
        try:
            if _proposed is not None and float(_proposed) > float(_cap):
                logger.error(f"Guardrail: günlük bütçe tavanı aşıldı ({_proposed} > {_cap} TL, {action.platform}). {action.action_id} ENGELLENDİ.")
                return False
        except (TypeError, ValueError):
            logger.error(f"Guardrail: geçersiz proposed budget {_proposed!r}. {action.action_id} ENGELLENDİ.")
            return False
        _since = datetime.utcnow() - timedelta(hours=24)
        _recent = (
            db.query(FactActionJournal)
            .filter(
                FactActionJournal.entity_id == action.entity_id,
                FactActionJournal.action_type.in_(["budget_increase", "budget_decrease"]),
                FactActionJournal.status == "executed",
                FactActionJournal.executed_at >= _since,
            )
            .count()
        )
        if _recent >= 3:
            logger.error(f"Guardrail: flapping — {action.entity_id} 24s'de {_recent} bütçe değişimi. {action.action_id} ENGELLENDİ.")
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
