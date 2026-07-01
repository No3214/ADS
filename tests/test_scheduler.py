import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from kads.data.warehouse import db as db_mod
from kads.data.warehouse.models import (DimCampaignState,
                                        FactActionJournal,
                                        FactAdPerformanceHourly)
from kads.scheduler.jobs import job_p0_health_check, job_p1_optimization, job_reflection
from kads.scheduler.worker import start_worker


@pytest.fixture(autouse=True)
def mock_warehouse_db(monkeypatch):
    test_engine = create_engine("sqlite:///:memory:")
    # Ensure models are loaded so metadata has the tables registered
    db_mod.Base.metadata.create_all(bind=test_engine)
    TestingSession = sessionmaker(bind=test_engine)

    monkeypatch.setattr(db_mod, "engine", test_engine)
    monkeypatch.setattr(db_mod, "SessionLocal", TestingSession)
    monkeypatch.setattr("kads.scheduler.jobs.SessionLocal", TestingSession)

    yield

    db_mod.Base.metadata.drop_all(bind=test_engine)


def test_p0_health_check_job():
    job_p0_health_check()

    session = db_mod.SessionLocal()
    campaigns = session.query(DimCampaignState).all()
    assert len(campaigns) > 0

    perf = session.query(FactAdPerformanceHourly).all()
    assert len(perf) > 0
    session.close()


def test_start_worker_non_blocking():
    sched = start_worker(blocking=False)
    assert sched is not None
    assert sched.running
    sched.shutdown()


def test_p1_optimization_idempotent():
    """P1: aksiyon üretir + ikinci çalıştırmada duplicate eklemez."""
    job_p1_optimization()
    s1 = db_mod.SessionLocal()
    n1 = s1.query(FactActionJournal).filter_by(status="pending").count()
    s1.close()
    job_p1_optimization()  # tekrar
    s2 = db_mod.SessionLocal()
    n2 = s2.query(FactActionJournal).filter_by(status="pending").count()
    s2.close()
    assert n2 == n1, "duplicate pending aksiyon eklendi"


def test_reflection_job_extracts_lessons():
    """Reflection: executed aksiyondan ders çıkarır, hata vermez."""
    import datetime
    s0 = db_mod.SessionLocal()
    s0.add(FactActionJournal(
        action_id="ex_refl", platform="google", entity_type="budget", entity_id="g_refl",
        action_type="budget_increase", current_state={"budget": 100.0},
        proposed_state={"budget": 150.0}, expected_impact="+dönüşüm",
        risk_score=0.1, confidence=0.9, status="executed",
        executed_at=datetime.datetime.utcnow()))
    s0.commit(); s0.close()
    job_reflection()  # exception fırlatmamalı
