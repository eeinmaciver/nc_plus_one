import psycopg
from fastapi import APIRouter, Depends, HTTPException
from db.connection import get_connection
from dependencies import get_user_id

router = APIRouter(prefix="/events", tags=["rsvp"])

@router.post("/{event_id}/rsvp", status_code=201)
def create_user_rsvp(event_id: int, user_id:int = Depends(get_user_id)):
    conn = get_connection()

    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM events WHERE event_id = %s;", (event_id,))
        if cursor.fetchone() is None:
            raise HTTPException(status_code=404, detail="Event not found")

        try:
            cursor.execute(
                """INSERT INTO rsvps (attendee_id, event_id)
                VALUES (%s, %s)
                RETURNING rsvp_id, attendee_id, event_id, created_at;""",
                (user_id, event_id),
            )
        except psycopg.errors.UniqueViolation:
            conn.rollback()
            raise HTTPException(status_code=409, detail="User has already RSVPed")

        row = cursor.fetchone()
        conn.commit()
        cursor.close()
    finally:
        conn.close()

    return {"rsvp": {
        "id": row[0],
        "attendee_id": row[1],
        "event_id": row[2],
        "created_at": row[3]
    }}