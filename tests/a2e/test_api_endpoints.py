from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_verify():
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
    assert response.json()["allowed"] is True
    assert response.json()["verdict"] == "MATCH"


def test_scenarios():
    response = client.get("/scenarios")

    assert response.status_code == 200

    scenarios = response.json()

    assert len(scenarios) == 4
    assert all(
        scenario["expected_allowed"] is False
        for scenario in scenarios
    )
