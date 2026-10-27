import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_get_events_returns_all_events(client):
    response = client.get("/events")
    assert response.status_code == 200
    assert response.json() == []