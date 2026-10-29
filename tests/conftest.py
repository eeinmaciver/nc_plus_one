import os
import sys

os.environ["ENV"] = 'test'

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient

from db.connection import get_connection
from seed import seed
from main import app

@pytest.fixture
def seed_db():
    seed()

@pytest.fixture
def client():
    return TestClient(app)