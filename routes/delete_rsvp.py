from fastapi import APIRouter, Depends, HTTPException, Response, status
from db.connection import get_connection
from dependencies import get_user_id

router = APIRouter(prefix="/events", tags=["events"])

@router.delete("/{event_id}/rsvp/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_rsvp(event_id: int, user_id: int = Depends(get_user_id)):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """DELETE FROM rsvps
        WHERE event_id = %s AND attendee_id = %s
        RETURNING rsvp_id;""",
        (event_id, user_id),
    )

    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail=("RSVP not found"))

    conn.commit()
    cursor.close()
    conn.close()

    return Response(status_code=status.HTTP_204_NO_CONTENT)