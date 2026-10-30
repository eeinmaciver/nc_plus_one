import jwt
import os

def make_token(user_id=1):
    return jwt.encode({"sub": str(user_id)}, os.environ["JWT_SECRET"], algorithm="HS256")

def auth(user_id=1):
    return {"Authorization": f"Bearer {make_token(user_id)}"}

def test_expected_response_200(client):
    response = client.get("/api/organisers/1/stats", headers=auth())
    assert response.status_code == 200

def test_organiser_not_found_returns_404(client):
    response = client.get("/api/organisers/99/stats", headers=auth())
    assert response.status_code == 404