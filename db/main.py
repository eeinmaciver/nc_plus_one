from seed import seed, get_data
from connection import get_connection

user_data = get_data("users.json")

conn = get_connection()

seed(conn, user_data)

conn.close()