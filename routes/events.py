from fastapi import APIRouter, HTTPException
from db.connection import get_connection

router = APIRouter(prefix="/events", tags=["events"])

@router.get("")
def get_events():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
            "SELECT * FROM events ORDER BY event_id ASC;"
        )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"events": rows}

@router.get("/{event_id}")
def get_event_id(event_id: str):

    try:
        event_id = int(event_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="ID is not a valid integer"
        )

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
            """SELECT e.event_id, e.title, e.description, e.starts_at, e.ends_at, v.name, v.address, v.capacity, e.created_at
            FROM events e
            JOIN venues v ON e.venue_id = v.venue_id
            WHERE e.event_id = %s
            """,
            (event_id, )
        )
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    return {
        "event": 
        {"event_id": row[0],
        "title": row[1],
        "description": row[2],
        "starts_at": row[3].isoformat(),
        "ends_at": row[4].isoformat(),
        "name": row[5],
        "address": row[6],
        "capacity": row[7],
        "created_at": row[8].isoformat()}
        }