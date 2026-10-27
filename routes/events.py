from fastapi import APIRouter, HTTPException
from db.connection import get_connection

router = APIRouter(prefix="/events", tags=["events"])

@router.get("")
def get_events():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
            "SELECT * FROM events ORDER BY event_id;"
        )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"events": rows}
    