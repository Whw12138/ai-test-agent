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


def test_web_ui_homepage_loads():
    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    assert "AI Test Agent" in response.text
    assert "运行 Agent" in response.text
    assert "Bug 摘要" in response.text
    assert "测试脑图" in response.text
    assert 'fetch("/run"' in response.text
