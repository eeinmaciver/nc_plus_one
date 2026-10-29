import os
import bcrypt
import jwt
import psycopg
from fastapi import APIRouter, HTTPException
from db.connection import get_connection
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

#create router that starts with /auth
router = APIRouter(prefix="/auth", tags=["auth"])

class RegisterRequest(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None

@router.post("/register", status_code=201)
def post_auth_register(body: RegisterRequest):

    if not body.name or not body.email or not body.password:
        raise HTTPException(
            status_code=400,
            detail="Email and password are required"
        )

    hashed = bcrypt.hashpw(body.password.encode(), bcrypt.gensalt()).decode()

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
                """INSERT INTO users
                (name, email, password)
                VALUES
                (%s, %s, %s)
                RETURNING user_id, name, email, created_at""",
                (body.name, body.email, hashed),
            )
    except psycopg.errors.UniqueViolation:
        conn.rollback()
        raise HTTPException(status_code=409, detail="Email already registered")
    
    row = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    return {
        "user": {
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "created_at": row[3]
        }
    }