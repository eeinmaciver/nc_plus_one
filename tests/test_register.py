import pytest

def test_auth_register_returns_201_response(client):
    response = client.post("/api/auth/login", json={"name": "alice wilde", "email": "alice@example.com", "password": "password123"})
    assert response.status_code == 201