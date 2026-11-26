from fastapi import APIRouter, HTTPException
from db.connection import get_connection
from psycopg.rows import dict_row

router = APIRouter(prefix="/events", tags=["events"])

@router.get("")
def get_events():
    conn = get_connection()
    cursor = conn.cursor(row_factory=dict_row)
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
    cursor = conn.cursor(row_factory=dict_row)
    cursor.execute(
            """SELECT e.event_id, e.title, e.description, e.starts_at, e.ends_at, v.name AS venue_name, v.address, v.capacity, e.created_at
            FROM events e
            LEFT JOIN venues v ON e.venue_id = v.venue_id
            WHERE e.event_id = %s;
            """,
            (event_id,),
        )
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    return {"event": row}