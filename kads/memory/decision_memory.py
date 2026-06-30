import logging

from sqlalchemy.orm import Session

from kads.data.warehouse.models import DimCampaignState, FactActionJournal

logger = logging.getLogger("kads.memory")


def reflect_on_past_actions(db: Session) -> list[dict]:
    """
    Reflection Agent: Reviews executed actions, compares predicted impact with
    actual outcomes (simulated), and logs lessons learned.
    """
    logger.info("Starting KADS Reflection Agent...")
    executed_actions = db.query(FactActionJournal).filter_by(status="executed").all()
    lessons = []

    for action in executed_actions:
        # Simulate checking campaign performance 24 hours after execution
        camp = (
            db.query(DimCampaignState).filter_by(campaign_id=action.entity_id).first()
        )

        # Simple simulated reflection logic
        if action.action_type == "budget_increase":
            lesson = {
                "action_id": action.action_id,
                "hypothesis": f"Scaling {action.platform} budget leads to more conversions",
                "predicted_outcome": action.expected_impact,
                "actual_outcome": "CPA remained stable at 1800 TL while conversions scaled by +15%.",
                "decision_quality": 1.0,
                "lesson": "Hypothesis validated: High-performing campaigns can sustain budget increases without CPA degradation.",
                "promote_to_heuristic": True,
            }
            lessons.append(lesson)
            logger.info(
                f"Reflection complete for action {action.action_id}: Lesson extracted."
            )

        elif action.action_type == "pause":
            lesson = {
                "action_id": action.action_id,
                "hypothesis": "Pausing high-CPA campaign prevents further budget waste",
                "predicted_outcome": action.expected_impact,
                "actual_outcome": "Budget bleed stopped. Blended CPA improved from 2500 TL to 1900 TL.",
                "decision_quality": 1.0,
                "lesson": "3x Kill Rule validated: Pausing low-performing prospecting sets stabilizes overall blended ROAS.",
                "promote_to_heuristic": False,
            }
            lessons.append(lesson)
            logger.info(
                f"Reflection complete for action {action.action_id}: Lesson extracted."
            )

    return lessons
