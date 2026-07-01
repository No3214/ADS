import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from kads.data.warehouse import db as db_mod
from kads.data.warehouse.models import (DimCampaignState,
                                        FactAdPerformanceHourly)
from kads.scheduler.jobs import job_p0_health_check
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
