from seed import seed, get_data
from db.connection import get_connetion

conn = get_connetion

user_data = get_data("users.json")

seed(conn, user_data)