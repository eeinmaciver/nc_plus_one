from connection import get_connection
from get_data import get_data
from user_seed import drop_user_table, create_user_table, seed_user_table
from venue_seed import drop_venues_table, create_venues_table, seed_venues_table
from event_seed import drop_events_table, create_events_table, seed_events_table
#from rsvp_seed import drop_rsvps_table, create_rsvps_table, seed_rsvps_table 

def main():
    user_data = get_data("users.json")
    venue_data = get_data("venues.json")
    event_data = get_data("events.json")
    #rsvp_data = get_data("rsvps.json")

    conn = get_connection()

    try:
        drop_events_table(conn)
        drop_venues_table(conn)
        drop_user_table(conn)

        create_user_table(conn)
        create_venues_table(conn)
        create_events_table(conn)

        seed_user_table(conn, user_data)
        seed_venues_table(conn, venue_data)
        seed_events_table(conn, event_data)
        
        # drop_rsvps_table
        # create_rsvps_table
        # seed_rsvps_table 
    finally:
        conn.close()

if __name__ == "__main__":
    main()