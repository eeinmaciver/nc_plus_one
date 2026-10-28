import os
import bcrypt
import jwt
from fastapi import APIRouter, HTTPException
from db.connection import get_connection
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

#load env into os.environ, set signing algorithm & token time
load_dotenv(".env.development")
SECRET = os.environ["JWT_SECRET"]
ALGORITHM = "HS256"
TOKEN_TIME = 1

#create router that starts with /auth
router = APIRouter(prefix="/auth", tags=["auth"])

class RegisterRequest(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None

@router.post("/register")
def post_auth_register(body: RegisterRequest): #parse JSON and check if email and password are present

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
            """INSERT INTO users
            (name, email, password)
            VALUES
            (%s, %s, %s)""",
            (body.name, body.email, body.password),
        )
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    return {
        "user": {
            "id": row[0],
            "name": row[3],
            "email": row[1],
            "created_at": row[4]
        }
    }