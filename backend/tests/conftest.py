import os
import shutil
import sys
from pathlib import Path

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).parent.parent))

from app.database import Base, engine
from app.main import app


@pytest.fixture(autouse=True)
def test_db():
    os.environ["TESTING"] = "1"

    db_path = os.path.abspath("test.db")

    if os.path.exists(db_path):
        try:
            os.chmod(db_path, 0o666)  # NOTE: gives proper read/write permissions
            os.remove(db_path)
        except OSError:
            pass

    parent_dir = os.path.dirname(db_path)
    os.makedirs(parent_dir, exist_ok=True)
    os.chmod(parent_dir, 0o777)

    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except OSError:
            pass


@pytest.fixture
def client(test_db):
    upload_dir = "uploads"
    if os.path.exists(upload_dir):
        shutil.rmtree(upload_dir)
    os.makedirs(upload_dir, mode=0o777, exist_ok=True)

    client = TestClient(app)
    yield client

    if os.path.exists(upload_dir):
        shutil.rmtree(upload_dir)


@pytest_asyncio.fixture(scope="function")
async def async_client(client):
    yield client
