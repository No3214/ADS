import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from kads.api.main import app
from kads.data.warehouse import db as db_mod
from kads.data.warehouse.db import get_db
from kads.data.warehouse.models import FactActionJournal

client = TestClient(app)


@pytest.fixture(autouse=True)
def mock_db_session(monkeypatch):
    test_engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    db_mod.Base.metadata.create_all(bind=test_engine)
    TestingSession = sessionmaker(bind=test_engine)

    def override_get_db():
        session = TestingSession()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    monkeypatch.setattr(db_mod, "SessionLocal", TestingSession)

    yield

    app.dependency_overrides.clear()
    db_mod.Base.metadata.drop_all(bind=test_engine)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "online"
    assert "tracking_health" in json_data


def test_approvals_list_and_lifecycle():
    session = db_mod.SessionLocal()
    action = FactActionJournal(
        action_id="act_abc",
        platform="google",
        entity_type="campaign",
        entity_id="g_111",
        action_type="pause",
        current_state={"status": "ENABLED"},
        proposed_state={"status": "PAUSED"},
        risk_score=0.3,
        confidence=0.9,
        requires_approval=True,
    )
    session.add(action)
    session.commit()
    session.close()

    resp = client.get("/approvals")
    assert resp.status_code == 200
    approvals = resp.json()
    assert len(approvals) == 1
    assert approvals[0]["action_id"] == "act_abc"
    assert approvals[0]["status"] == "pending"

    resp_approve = client.post("/actions/act_abc/approve")
    assert resp_approve.status_code == 200
    assert resp_approve.json()["status"] == "approved"

    session = db_mod.SessionLocal()
    action_in_db = (
        session.query(FactActionJournal).filter_by(action_id="act_abc").first()
    )
    assert action_in_db.status == "approved"
    session.close()


def _seed_pending(action_id="act_seed"):
    session = db_mod.SessionLocal()
    session.add(FactActionJournal(
        action_id=action_id, platform="meta", entity_type="budget", entity_id="m_1",
        action_type="update_budget", current_state={"budget": 100.0},
        proposed_state={"budget": 120.0}, risk_score=0.2, confidence=0.9,
        requires_approval=True, status="pending"))
    session.commit(); session.close()


def test_approve_nonexistent_404():
    assert client.post("/actions/yok_boyle/approve").status_code == 404


def test_reject_nonexistent_404():
    assert client.post("/actions/yok_boyle/reject").status_code == 404


def test_reject_happy_path():
    _seed_pending("act_rej")
    r = client.post("/actions/act_rej/reject")
    assert r.status_code == 200 and r.json()["status"] == "rejected"


def test_approve_already_processed_400():
    _seed_pending("act_twice")
    assert client.post("/actions/act_twice/approve").status_code == 200
    # ikinci kez -> 400 (zaten approved)
    r = client.post("/actions/act_twice/approve")
    assert r.status_code == 400 and "already" in r.json()["detail"]


def test_reject_already_processed_400():
    _seed_pending("act_rej2")
    client.post("/actions/act_rej2/reject")
    r = client.post("/actions/act_rej2/reject")
    assert r.status_code == 400
