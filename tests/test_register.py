import pytest
import os
import jwt

def test_auth_register_returns_201_response(client):
    response = client.post("/api/auth/register", json={"name": "john smith", "email": "john@example.com", "password": "password123"})
    assert response.status_code == 201

def test_auth_register_does_not_return_password_in_response(client):
    response = client.post("/api/auth/register", json={"name": "kevin davies", "email": "kevdav@example.com", "password": "password123"})
    json = response.json()
    assert "password" not in json["user"]

def test_auth_register_returns_400_for_empty_fields(client):
    response = client.post("/api/auth/register", json={})
    assert response.status_code == 400

def test_auth_register_returns_409_for_email_already_in_use(client):
    response = client.post("/api/auth/register", json={"name": "john smith", "email": "john@example.com", "password": "password123"})
    assert response.status_code == 409