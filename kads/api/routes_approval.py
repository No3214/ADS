from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from kads.data.warehouse.db import get_db
from kads.data.warehouse.models import FactActionJournal

router = APIRouter(tags=["Approvals"])


@router.get("/approvals")
def list_pending_approvals(db: Session = Depends(get_db)):
    """
    Returns all pending optimization actions that require human approval.
    """
    actions = db.query(FactActionJournal).filter_by(status="pending").all()
    return [
        {
            "action_id": a.action_id,
            "created_at": a.created_at,
            "platform": a.platform,
            "entity_type": a.entity_type,
            "entity_id": a.entity_id,
            "action_type": a.action_type,
            "current_state": a.current_state,
            "proposed_state": a.proposed_state,
            "expected_impact": a.expected_impact,
            "risk_score": a.risk_score,
            "confidence": a.confidence,
            "requires_approval": a.requires_approval,
            "approval_reason": a.approval_reason,
            "rollback_plan": a.rollback_plan,
            "status": a.status,
        }
        for a in actions
    ]


@router.post("/actions/{action_id}/approve")
def approve_action(action_id: str, db: Session = Depends(get_db)):
    """
    Approves a pending action.
    """
    action = db.query(FactActionJournal).filter_by(action_id=action_id).first()
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")
    if action.status != "pending":
        raise HTTPException(
            status_code=400, detail=f"Action is already {action.status}"
        )

    action.status = "approved"
    db.commit()
    return {"message": "Action approved", "action_id": action_id, "status": "approved"}


@router.post("/actions/{action_id}/reject")
def reject_action(action_id: str, db: Session = Depends(get_db)):
    """
    Rejects a pending action.
    """
    action = db.query(FactActionJournal).filter_by(action_id=action_id).first()
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")
    if action.status != "pending":
        raise HTTPException(
            status_code=400, detail=f"Action is already {action.status}"
        )

    action.status = "rejected"
    db.commit()
    return {"message": "Action rejected", "action_id": action_id, "status": "rejected"}
