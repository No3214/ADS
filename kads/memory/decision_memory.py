import logging

from sqlalchemy.orm import Session

from kads.data.warehouse.models import FactActionJournal

logger = logging.getLogger("kads.memory")


def reflect_on_past_actions(db: Session) -> list[dict]:
    """
    Reflection Agent: Reviews executed actions and logs lessons learned.

    DİKKAT: Bu fonksiyonun "actual_outcome" değerleri ŞU AN SABİT-SİMÜLEDİR
    (gerçek performans okumaz). Ölçüm (GA4/Ads conversion) canlıya geçince
    FactCampaignPerformance'tan gerçek CPA/dönüşüm okunup buraya bağlanmalı.
    O zamana kadar çıkan "ders"ler gerçek değil — heuristik'e PROMOTE etmeyin.
    """
    logger.info("Starting KADS Reflection Agent...")
    executed_actions = db.query(FactActionJournal).filter_by(status="executed").all()
    lessons = []

    for action in executed_actions:
        # NOT: gerçek performans okuması ölçüm canlıya geçince eklenecek.
        # Şimdilik aşağıdaki actual_outcome değerleri SABİT-SİMÜLEDİR.
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
