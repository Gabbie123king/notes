# app/tests/conftest.py
import pytest
from sqlmodel import SQLModel, create_engine, Session
from fastapi.testclient import TestClient
from app.main import app
from app.models.note import Note
from dotenv import load_dotenv
import os

# Load test environment variables
load_dotenv(".env.test")

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=False)

@pytest.fixture(name="session")
def session_fixture():
    # create tables
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    # drop tables after test
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="client")
def client_fixture(session):
    # override dependency
    def get_session_override():
        yield session

    # Override the get_session dependency in your app
    from app.core.database import get_session
    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client