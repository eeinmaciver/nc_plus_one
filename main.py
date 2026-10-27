from db.connection import get_connection
from db.get_data import get_data
from db.user_seed import drop_user_table, create_user_table, seed_user_table
from db.venue_seed import drop_venues_table, create_venues_table, seed_venues_table
from db.event_seed import drop_events_table, create_events_table, seed_events_table
from db.rsvp_seed import drop_rsvp_table, create_rsvp_table, seed_rsvp_table

from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from routes.events import router as events_router
from routes.auth_login import router as auth_router

app = FastAPI(title="NC Plus One", debug=True)
app.include_router(events_router, prefix="/api")
app.include_router(auth_router, prefix="/api")

@app.exception_handler(HTTPException)
def handle_http_exception(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

def main():
    user_data = get_data("users.json")
    venue_data = get_data("venues.json")
    event_data = get_data("events.json")
    rsvp_data = get_data("rsvps.json")

    conn = get_connection()

    drop_rsvp_table(conn)
    drop_events_table(conn)
    drop_venues_table(conn)
    drop_user_table(conn)

    create_user_table(conn)
    create_venues_table(conn)
    create_events_table(conn)
    create_rsvp_table(conn)

    seed_user_table(conn, user_data)
    seed_venues_table(conn, venue_data)
    seed_events_table(conn, event_data)
    seed_rsvp_table(conn, rsvp_data)
    
    conn.close()

if __name__ == "__main__":
    main()