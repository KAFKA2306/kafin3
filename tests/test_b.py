import pytest
from fastapi.testclient import TestClient
from src.backend.main import app

client = TestClient(app)

def test_analyze_endpoint():
    response = client.post("/analyze", json={"query": "GAFA Stock Performance YTD"})
    assert response.status_code == 200
    data = response.json()
    assert "performance" in data
    assert "message" in data
    assert isinstance(data["performance"], dict)
    assert len(data["performance"]) == 4  # GAFA stocks

def test_invalid_query():
    response = client.post("/analyze", json={"query": ""})
    assert response.status_code == 400

# 他のテストケースを追加...
