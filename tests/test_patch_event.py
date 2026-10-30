import jwt
import os

def make_token(user_id=1):
    return jwt.encode({"sub": str(user_id)}, os.environ["JWT_SECRET"], algorithm="HS256")

def auth(user_id=1):
    return {"Authorization": f"Bearer {make_token(user_id)}"}

event_update = {"description": "Updated description, now with live music!", "starts_at": "2027-08-16T19:00:00Z", "ends_at": "2027-08-16T23:00:00Z"}

def test_patch_event_repsonse_returns_200(client):
    response = client.patch("/api/events/1", json=event_update, headers=auth())
    assert response.status_code == 200

def test_missing_or_invalid_token_returns_401(client):
    response = client.patch("/api/events/1", json=event_update)
    assert response.status_code == 401

def test_auth_user_is_not_organiser_returns_403(client):
    response = client.patch("/api/events/1", json=event_update, headers=auth(99))
    assert response.status_code == 403

def test_event_not_found_returns_404(client):
    response = client.patch("/api/events/99", json=event_update, headers=auth())
    assert response.status_code == 404

def test_invalid_date_format_returns_400(client):
    response = client.patch("/api/events/1", json={"starts_at": "not-a-date"}, headers=auth())
    assert response.status_code == 400

def test_event_start_is_before_event_end_400(client):
    response = client.patch("/api/events/1", json={"starts_at": "2027-08-16T23:00:00Z", "ends_at": "2027-08-16T19:00:00Z"}, headers=auth())
    assert response.status_code == 400