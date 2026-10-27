import psycopg
import bcrypt

def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def drop_user_table(connection):

    drop_users = "DROP TABLE IF EXISTS users"

    with connection.cursor() as cur:
            cur.execute(drop_users)

    connection.commit()

def create_user_table(connection):

    create_user_table = """CREATE TABLE users (
        user_id SERIAL PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        name VARCHAR(255) NOT NULL,
        created_at TIMESTAMPTZ DEFAULT NOW()
    );"""

    with connection.cursor() as cur:
        cur.execute(create_user_table)

    connection.commit()
         
def seed_user_table(connection, users):

    insert_users = """
                INSERT INTO users
                (name, email, password)
                VALUES
                (%s, %s, %s)"""

    with connection.cursor() as cur:
        cur.executemany(insert_users, [(user["name"], user["email"], hash_password(user["password"])) for user in users])

    connection.commit()