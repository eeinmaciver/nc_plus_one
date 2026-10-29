import pytest
import jwt
import os

def make_token(user_id=1):
    return jwt.encode({"sub": str(user_id)}, os.environ["JWT_SECRET"], algorithm="HS256")

def auth(user_id=1):
    return {"Authorization": f"Bearer {make_token(user_id)}"}

def test_rsvp_returns_201(client):
    response = client.post("/api/events/1/rsvp", headers=auth())
    assert response.status_code == 201

def test_event_not_found_404(client):
    response = client.post("/api/events/99/rsvp", headers=auth())
    assert response.status_code == 404

def test_user_has_already_rsvped_event_409(client):
    response = client.post("/api/events/1/rsvp", headers=auth())
    assert response.status_code == 409

def test_rsvp_without_token_returns_401(client):
    response = client.post("/api/events/1/rsvp")
    assert response.status_code == 401