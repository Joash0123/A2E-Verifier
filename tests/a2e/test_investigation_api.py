from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_verify_returns_investigation_for_drift():
    response = client.post(
        "/verify",
        json={
            "authorized": {
                "tool": "ticket_api",
                "operation": "read",
                "resource": "ticket:1001",
                "parameters": {},
                "context": {},
                "actor": "agent-1",
            },
            "executed": {
                "tool": "ticket_api",
                "operation": "read",
                "resource": "ticket:2002",
                "parameters": {},
                "context": {},
                "actor": "agent-1",
            },
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["allowed"] is False
    assert data["verdict"] == "RESOURCE_MISMATCH"
    assert data["investigation"]["category"] == "RESOURCE_DRIFT"
    assert data["investigation"]["evidence"]
    assert data["investigation"]["remediation"]


def test_verify_returns_no_drift_for_match():
    action = {
        "tool": "ticket_api",
        "operation": "read",
        "resource": "ticket:1001",
        "parameters": {},
        "context": {},
        "actor": "agent-1",
    }

    response = client.post(
        "/verify",
        json={
            "authorized": action,
            "executed": action,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["allowed"] is True
    assert data["verdict"] == "MATCH"
    assert data["investigation"]["category"] == "NO_DRIFT"
