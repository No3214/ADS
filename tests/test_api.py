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
