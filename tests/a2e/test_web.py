from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_homepage():
    response = client.get("/")

    assert response.status_code == 200
    assert "A2E Verifier" in response.text


def test_css():
    response = client.get("/static/style.css")

    assert response.status_code == 200
    assert "body" in response.text


def test_javascript():
    response = client.get("/static/app.js")

    assert response.status_code == 200
    assert "verifyAction" in response.text
