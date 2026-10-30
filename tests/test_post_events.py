import jwt
import os

def make_token(user_id=1):
    return jwt.encode({"sub": str(user_id)}, os.environ["JWT_SECRET"], algorithm="HS256")

def auth(user_id=1):
    return {"Authorization": f"Bearer {make_token(user_id)}"}

def new_event(**overrides):
    event = {
        "title": "Python Meetup",
        "description": "An evening of lightning talks",
        "starts_at": "2026-12-01T18:30:00+00:00",
        "ends_at": "2026-12-01T21:00:00+00:00",
        "venue_id": 1,
    }
    event.update(overrides)
    return event

def test_create_event_returns_201_response(client):
    response = client.post("/api/events", json=new_event(), headers=auth())
    assert response.status_code == 201

def test_missing_or_invalid_token_returns_401(client):
    response = client.post("/api/events", json=new_event())
    assert response.status_code == 401

def test_missing_field_returns_400_response(client):
    event = new_event()
    del event["title"]
    response = client.post("/api/events", json=event, headers=auth())
    assert response.status_code == 400

def test_invalid_date_returns_400_response(client):
    response = client.post("/api/events", json=new_event(starts_at="7 minutes past 12"), headers=auth())
    assert response.status_code == 400