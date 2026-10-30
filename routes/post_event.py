from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from db.connection import get_connection
from datetime import datetime
from dependencies import get_user_id

router = APIRouter(prefix="/events", tags=["events"])

class CreateEvent(BaseModel):
    title: str
    description: str
    starts_at: datetime
    ends_at: datetime
    venue_id: int

@router.post("", status_code=201)
def post_events(event: CreateEvent, user_id: int = Depends(get_user_id)):
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
            """INSERT INTO events (title, description, starts_at, ends_at, organiser_id, venue_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING event_id, title, description, starts_at, ends_at, organiser_id, venue_id, created_at;""",
            (event.title, event.description, event.starts_at, event.ends_at, user_id, event.venue_id)
        )
    
    row = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    return {"event": {
        "id": row[0],
        "title": row[1],
        "description": row[2],
        "starts_at": row[3],
        "ends_at": row[4],
        "organiser_id": row[5],
        "venue_id": row[6],
        "created_at": row[7] 
    }}