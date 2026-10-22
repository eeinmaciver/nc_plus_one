import psycopg

def drop_venues_table(connection):

    drop_venues = "DROP TABLE IF EXISTS venues"

    with connection.cursor() as cur:
            cur.execute(drop_venues)

    connection.commit()

def create_venues_table(connection):

    create_venues = """CREATE TABLE venues(
    venue_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT,
    capacity INTEGER
    );"""

    with connection.cursor() as cur:
        cur.execute(create_venues)

    connection.commit()

def seed_venues_table(connection, venues):

    insert_venues = """
                INSERT INTO venues
                (name, address, capacity)
                VALUES
                (%s, %s, %s)"""

    with connection.cursor() as cur:
        cur.executemany(insert_venues, [(venue["name"], venue["address"], venue["capacity"]) for venue in venues])

    connection.commit()