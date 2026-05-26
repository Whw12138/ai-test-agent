from fastapi.testclient import TestClient

from ai_test_agent.api import app


def test_api_analyze_endpoint():
    client = TestClient(app)
    response = client.post(
        "/analyze",
        json={"text": "## GET /health\nSuccess: 200\nResponse Keys: status"},
    )

    assert response.status_code == 200
    assert response.json()["endpoints"][0]["path"] == "/health"
