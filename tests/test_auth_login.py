import os
import jwt

def test_login_success(client):
    response = client.post("/api/auth/login", json={"email": "alice@example.com", "password": "password123"})
    assert response.status_code == 200
    token = response.json()["token"]
    payload = jwt.decode(token, os.environ["JWT_SECRET"], algorithms=["HS256"])
    assert "sub" in payload

def test_email_not_found(client):
    response = client.post("/api/auth/login", json={"email": "tomcruise@example.com", "password": "password123"})
    assert response.status_code == 401

def test_incorrest_password(client):
    response = client.post("/api/auth/login", json={"email": "alice@example.com", "password": "wrongpassword123"})
    assert response.status_code == 401

def test_empty_email_field(client):
    response = client.post("/api/auth/login", json={"email": None, "password": "password123"})
    assert response.status_code == 400