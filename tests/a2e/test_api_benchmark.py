from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_benchmark():
    response = client.get("/benchmark")

    assert response.status_code == 200

    data = response.json()

    assert data["total_cases"] == 15
    assert data["attack_cases"] == 12
    assert data["attacks_detected"] == 12
    assert data["benign_cases"] == 3
    assert data["benign_accepted"] == 3
    assert data["false_positives"] == 0
    assert data["detection_rate"] == 1.0
    assert data["false_positive_rate"] == 0.0
