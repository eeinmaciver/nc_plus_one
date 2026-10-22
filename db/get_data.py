import json

def get_data(file_name):
    with open(f"db/data/{file_name}") as file:
        return json.load(file)