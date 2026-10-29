import psycopg

def drop_rsvp_table(connection):

    drop_rsvps = "DROP TABLE IF EXISTS rsvps;"

    with connection.cursor() as cur:
            cur.execute(drop_rsvps)

    connection.commit()

def create_rsvp_table(connection):

    create_rsvps = """CREATE TABLE rsvps (
    rsvp_id SERIAL PRIMARY KEY,
    attendee_id INTEGER REFERENCES users(user_id),
    event_id INTEGER REFERENCES events(event_id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (attendee_id, event_id)
);"""

    with connection.cursor() as cur:
        cur.execute(create_rsvps)

    connection.commit()
         
def seed_rsvp_table(connection, rsvps):

    insert_rsvps = """
                INSERT INTO rsvps
                (attendee_id, event_id)
                VALUES
                (%s, %s);"""

    with connection.cursor() as cur:
        cur.executemany(insert_rsvps, [(rsvp["attendee_id"], rsvp["event_id"]) for rsvp in rsvps])

    connection.commit()