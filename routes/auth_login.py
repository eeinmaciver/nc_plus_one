import os
import bcrypt
import jwt
from fastapi import APIRouter, HTTPException
from db.connection import get_connection
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone

router = APIRouter(prefix="/auth", tags=["auth"])

JWT_SECRET = os.eniron["JWT_SECRET"]
JWT_ALGORITHM = "HS256"
TOKEN_LIFETIME_HOURS = 1

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
def post_auth_login(body: LoginRequest):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
            "SELECT user_id, name, email, password FROM users WHERE email = %s;",
            (body.email,),
        )
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row is None or not bcrypt.checkpw(
        body.password.encode("utf-8"), row[3].encode("utf-8")
    ):
        raise HTTPException(
            status_code=401,
            detail={"message": "Email not found or password incorrect"}
        )

    payload = {
        "sub": str(row[0]),
        "exp": datetime.now(timezone.utc) + timedelta(hours=TOKEN_LIFETIME_HOURS),
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return {"token": token}