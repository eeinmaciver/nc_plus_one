import psycopg

def drop_events_table(connection):

    drop_events = "DROP TABLE IF EXISTS events"

    with connection.cursor() as cur:
            cur.execute(drop_events)

    connection.commit()

def create_events_table(connection):

    create_events = """CREATE TABLE events (
    event_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    starts_at TIMESTAMPTZ NOT NULL,
    ends_at TIMESTAMPTZ NOT NULL,
    organiser_id INTEGER REFERENCES users(user_id),
    venue_id INTEGER REFERENCES venues(venue_id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);"""

    with connection.cursor() as cur:
        cur.execute(create_events)

    connection.commit()
         
def seed_events_table(connection, events):

    insert_events = """
                INSERT INTO events
                (title, description, starts_at, ends_at, organiser_id, venue_id)
                VALUES
                (%s, %s, %s, %s, %s, %s)"""

    with connection.cursor() as cur:
        cur.executemany(insert_events, [(event["title"], event["description"], event["starts_at"], event["ends_at"], event["organiser_id"], event["venue_id"]) for event in events])

    connection.commit()