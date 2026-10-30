from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from db.connection import get_connection
from datetime import datetime
from dependencies import get_user_id

router = APIRouter(prefix="/events", tags=["events"])

class UpdateEvent(BaseModel):
    title: str | None = None
    description: str | None = None
    starts_at: datetime | None = None
    ends_at: datetime | None = None
    venue_id: int | None = None

@router.patch("/{event_id}", status_code=200)
def patch_event(event: UpdateEvent, event_id: int, user_id: int = Depends(get_user_id)) -> dict:

    update = event.model_dump(exclude_unset=True)
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """SELECT organiser_id, starts_at, ends_at 
        FROM events
        WHERE event_id = %s;""",
        (event_id, )
    )

    check_row = cursor.fetchone()
    if check_row == None:
        raise HTTPException(status_code=404, detail="Event not found")
    if check_row[0] != user_id:
        raise HTTPException(status_code=403, detail="User is not event organiser")

    new_starts_at = update.get("starts_at", check_row[1])
    new_ends_at = update.get("ends_at", check_row[2])
    if new_ends_at <= new_starts_at:
        raise HTTPException(status_code=400, detail="Event end time must be after start time")

    set_fields = ", ".join(f"{column} = %s" for column in update)
    cursor.execute(
            f"""UPDATE events 
            SET {set_fields}
            WHERE event_id = %s
            RETURNING event_id, title, description, starts_at, ends_at, organiser_id, venue_id, created_at;""",
            (*update.values(), event_id)
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