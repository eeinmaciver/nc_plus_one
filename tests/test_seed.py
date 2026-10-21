import pytest
from db.seed import seed, format_user_data


def test_seed_function():
    assert seed == seed

def test_format_user_data():
    data = {
    "name": "Alice Rahman",
    "email": "alice@example.com",
    "password": "password123"
  }

    expected = [("Alice Rahman", "alice@example.com", "password123")]
    
    assert format_user_data(data) == expected