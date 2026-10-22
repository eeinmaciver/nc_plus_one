from user_seed import drop_user_table, create_user_table, seed_user_table
from connection import get_connection
from get_data import get_data
from venue_seed import drop_venues_table, create_venues_table, seed_venues_table

def main():
    user_data = get_data("users.json")
    venue_data = get_data("venues.json")
    conn = get_connection()

    try:
        drop_user_table(conn)
        create_user_table(conn)
        seed_user_table(conn, user_data)

        drop_venues_table(conn)
        create_venues_table(conn)
        seed_venues_table(conn, venue_data)
    finally:
        conn.close()

if __name__ == "__main__":
    main()