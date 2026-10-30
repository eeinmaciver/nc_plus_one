from fastapi import APIRouter, Depends
from db.connection import get_connection
from dependencies import get_user_id

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/me/events", status_code=200)
def get_user_rsvps(user_id: int = Depends(get_user_id)):
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    """SELECT rsvps.attendee_id, events.event_id, events.title, events.starts_at, rsvps.created_at,
    RANK() OVER (ORDER BY events.starts_at) AS event_rank,
    COUNT(*) OVER () AS total_rsvps
    FROM rsvps
    JOIN events ON events.event_id = rsvps.event_id
    WHERE rsvps.attendee_id = %s
    ORDER BY events.starts_at;""",
    (user_id, )
    )
    
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return {"events": [{"id": r[1], "title": r[2], "starts_at": r[3], "rsvp_date": r[4], "event_rank": r[5], "total_rsvps": r[6]} for r in rows]}
