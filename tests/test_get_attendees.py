import jwt
import os

def make_token(user_id=1):
    return jwt.encode({"sub": str(user_id)}, os.environ["JWT_SECRET"], algorithm="HS256")

def auth(user_id=1):
    return {"Authorization": f"Bearer {make_token(user_id)}"}

def test_expected_response_200(client):
    response = client.get("/api/events/1/attendees", headers=auth())
    assert response.status_code == 200

def test_missing_or_invalid_token_401(client):
    response = client.get("/api/events/1/attendees")
    assert response.status_code == 401

def test_auth_user_is_not_organiser_403(client):
    response = client.get("/api/events/1/attendees", headers=auth(99))
    assert response.status_code == 403

def test_non_existant_event_returns_404(client):
    response = client.get("/api/events/99/attendees", headers=auth())
    assert response.status_code == 404