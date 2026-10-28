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

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
def post_auth_login(body: LoginRequest): #parse JSON and check if email and password are present

    #look up user in the database
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
            "SELECT user_id, name, email, password FROM users WHERE email = %s;",
            (body.email,),
        )
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    
    #check user credentials
    if row is None or not bcrypt.checkpw(
        body.password.encode("utf-8"), row[3].encode("utf-8")
    ):
        raise HTTPException(
            status_code=401,
            detail={"message": "Email not found or password incorrect"}
        )

    #build the token
    payload = {
        "sub": str(row[0]),
        "email": row[2],
        "exp": datetime.now(timezone.utc) + timedelta(hours=TOKEN_TIME),
    }
    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)

    #return token
    return {"token": token}