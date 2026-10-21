import json
from connection import get_connection
import psycopg

def get_data(file_name):
    with open(f"db/data/{file_name}") as file:
        return json.load(file)

def seed(conn, users):

    drop_user_table = "DROP TABLE IF EXISTS users"

    create_user_table = """CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);"""

    insert_users = """
                INSERT INTO users
                (name, email, password)
                VALUES
                (%s, %s, %s)"""

    with conn.cursor() as cur:
        cur.execute(drop_user_table)
        cur.execute(create_user_table)
        cur.executemany(insert_users, [(user["name"], user["email"], user["password"]) for user in users])

    conn.commit()
    conn.close()

if __name__ == "__main__":
    seed()