from connection import get_connection
from get_data import get_data
from user_seed import drop_user_table, create_user_table, seed_user_table
from venue_seed import drop_venues_table, create_venues_table, seed_venues_table
from event_seed import drop_events_table, create_events_table, seed_events_table
from rsvp_seed import drop_rsvp_table, create_rsvp_table, seed_rsvp_table

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