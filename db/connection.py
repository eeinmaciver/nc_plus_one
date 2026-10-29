import psycopg
import os
from dotenv import load_dotenv

def get_connection():

    env = os.getenv("ENV", "development")
    load_dotenv(f".env.{env}", override=True)

    if not os.getenv("PGDATABASE"):
        raise RuntimeError("PGDATABASE NOT SET")

    connection = psycopg.connect(
        host=os.getenv("PGHOST", "localhost"),
        port=os.getenv("PGPORT", "5432"),
        dbname=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD")
    )

    return connection