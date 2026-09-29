from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)

authorized = {
    "tool": "ticket_api",
    "operation": "read",
    "resource": "ticket:1001",
    "parameters": {},
    "context": {},
    "actor": "agent-1",
}

matching = {
    **authorized,
}

drifted = {
    **authorized,
    "resource": "ticket:1002",
}


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_verify_matching_action():
    response = client.post(
        "/verify",
        json={
            "authorized": authorized,
            "executed": matching,
        },
    )

    assert response.status_code == 200
    assert response.json()["allowed"] is True
    assert response.json()["verdict"] == "MATCH"


def test_verify_resource_drift():
    response = client.post(
        "/verify",
        json={
            "authorized": authorized,
            "executed": drifted,
        },
    )

    assert response.status_code == 200
    assert response.json()["allowed"] is False
    assert response.json()["verdict"] == "RESOURCE_MISMATCH"
