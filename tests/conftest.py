import os
import pytest
import backend.models as models

from dotenv import load_dotenv
from fastapi.testclient import TestClient
from backend.main import create_app, get_db
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine, Column, ForeignKey, Integer, String

load_dotenv()

@pytest.fixture(scope="session")
def setup_test_db():
    DB_USER = os.getenv("POSTGRES_USER", "fallback_user")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "fallback_password")
    DB_NAME = os.getenv("POSTGRES_TEST_DB", "fallback_test_db")
    DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@localhost:5432/{DB_NAME}"

    engine = create_engine(DATABASE_URL)

    # this gets forwarded to the test-database container via the above url
    models.Base.metadata.create_all(bind=engine)

    yield engine

    models.Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session_for_test(setup_test_db):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=setup_test_db)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client_with_overrides(db_session_for_test):
    # fastapi can't take a fixture for a dependency override, this acts as a bridge
    def get_test_db():
        yield db_session_for_test

    app = create_app()
    app.dependency_overrides[get_db] = get_test_db
    client = TestClient(app)
    yield client
