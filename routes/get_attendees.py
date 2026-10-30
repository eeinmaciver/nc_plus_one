from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from db.connection import get_connection
from datetime import datetime
from dependencies import get_user_id

router = APIRouter(prefix="/events", tags=["events"])

@router.get("/{event_id}/attendees", status_code=200)
def get_event_attendees(event_id, user_id: int = Depends(get_user_id)):
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    """SELECT organiser_id
    FROM events
    WHERE event_id = %s;""",
    (event_id, )
    )

    check_row = cursor.fetchone()
    if check_row == None:
        raise HTTPException(status_code=404, detail="Event not found")
    if check_row[0] != user_id:
        raise HTTPException(status_code=403, detail="User is not event organiser")

    cursor.execute(
    """SELECT users.user_id, users.name, users.email
    FROM rsvps
    JOIN users ON users.user_id = rsvps.attendee_id
    WHERE rsvps.event_id = %s
    ORDER BY rsvps.created_at;""",
    (event_id,),
    )
    
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return {"attendees": [{"user_id": r[0], "name": r[1], "email": r[2]} for r in rows]}