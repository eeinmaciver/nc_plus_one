import jwt
import os

def make_token(user_id=1):
    return jwt.encode({"sub": str(user_id)}, os.environ["JWT_SECRET"], algorithm="HS256")

def auth(user_id=1):
    return {"Authorization": f"Bearer {make_token(user_id)}"}

def test_delete_rsvp_returns_204(client, seed_db):
    response = client.delete("/api/events/5/rsvp/me", headers=auth(2))
    assert response.status_code == 204

def test_rsvp_not_found_returns_404(client):
    response = client.delete("/api/events/5/rsvp/me", headers=auth())
    assert response.status_code == 404

def test_missing_or_invalid_token_returns_401(client):
    response = client.delete("/api/events/5/rsvp/me")
    assert response.status_code == 401