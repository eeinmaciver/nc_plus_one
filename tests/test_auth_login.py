import os
import jwt
import pytest

def test_login_success(client):
    response = client.post("/api/auth/login", json={"email": "alice@example.com", "password": "password123"})
    assert response.status_code == 200
    token = response.json()["token"]
    payload = jwt.decode(token, os.environ["JWT_SECRET"], algorithms=["HS256"])
    assert "sub" in payload

def test_signature_with_bad_secret(client):
    response = client.post("/api/auth/login", json={"email": "alice@example.com", "password": "password123"})
    token = response.json()["token"]
    # payload = jwt.decode(token, "wrong-secret-is-wrong", algorithms=["HS256"])
    # assert "sub" in payload
    with pytest.raises(jwt.InvalidSignatureError):
        jwt.decode(token, "wrong-secret-is-wrong-this-not-good", algorithms=["HS256"])
        
def test_incorrect_email(client):
    response = client.post("/api/auth/login", json={"email": "tomcruise@example.com", "password": "password123"})
    assert response.status_code == 401

def test_incorrect_password(client):
    response = client.post("/api/auth/login", json={"email": "alice@example.com", "password": "wrongpassword123"})
    assert response.status_code == 401

def test_empty_email_field(client):
    response = client.post("/api/auth/login", json={"email": "alice@example.com"})
    assert response.status_code == 400

def test_empty_password_field(client):
    response = client.post("/api/auth/login", json={"password": "password123"})
    assert response.status_code == 400