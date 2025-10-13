import os
import pytest
import backend.models as models

from fastapi.testclient import TestClient
from backend.database import get_db
from backend.main import create_app
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


@pytest.fixture(scope="session")
def create_test_engine():
    # loaddot_env unnecessary - the environment variables are loaded by docker compose
    DB_USER = os.getenv("POSTGRES_USER", "fallback_user")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "fallback_password")
    DB_NAME = os.getenv("POSTGRES_TEST_DB", "fallback_test_db")
    DATABASE_URL = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@localhost:5432/{DB_NAME}"
    )

    engine = create_engine(DATABASE_URL)

    # this gets forwarded to the test database container via the above url
    models.Base.metadata.create_all(bind=engine)

    yield engine


@pytest.fixture()
def db_test_session(create_test_engine):
    engine = create_test_engine
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture()
def get_test_client(db_test_session):
    # .dependency_overrides needs a function as an argument - can't take a fixture
    def override_get_db():
        yield db_test_session

    app = create_app()
    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)
    yield client
