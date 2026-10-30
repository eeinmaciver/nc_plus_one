from fastapi import APIRouter, HTTPException, Depends
from db.connection import get_connection
from dependencies import get_user_id

router = APIRouter(prefix="/organisers", tags=["organisers"])

@router.get("/{organiser_id}/stats", status_code=200)
def get_organiser_stats(organiser_id: int , user_id: int = Depends(get_user_id)):
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    """WITH event_attendance AS (
    SELECT events.event_id, events.organiser_id,
    COUNT(rsvps.rsvp_id) AS attendee_count
    FROM events
    LEFT JOIN rsvps ON rsvps.event_id = events.event_id
    GROUP BY events.event_id, events.organiser_id),
    organiser_totals AS (
    SELECT users.user_id AS organiser_id, users.name,
    COUNT(event_attendance.event_id) AS total_events,
    ROUND(AVG(event_attendance.attendee_count), 1) AS avg_attendance,
    MAX(event_attendance.attendee_count) AS best_attended
    FROM users
    JOIN event_attendance ON event_attendance.organiser_id = users.user_id
    GROUP BY users.user_id, users.name
    ),
    ranked AS (
    SELECT *, RANK() OVER (ORDER BY total_events DESC) AS organiser_rank
    FROM organiser_totals)
    SELECT organiser_id, name, total_events, avg_attendance, best_attended, organiser_rank
    FROM ranked
    WHERE organiser_id = %s;""",
    (organiser_id, )
    )
    
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Organiser ID not found")

    return {"stats": {"organiser_id": row[0], "name": row[1], "total_events": row[2], "avg_attendance": float(row[3]), "best_attended_count": row[4], "organiser_rank": row[5]}}