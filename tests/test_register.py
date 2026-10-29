import pytest
import os
import jwt

def test_auth_register_returns_201_response(client):
    response = client.post("/api/auth/login", json={"name": "john smith", "email": "john@example.com", "password": "password123"})
    assert response.status_code == 201