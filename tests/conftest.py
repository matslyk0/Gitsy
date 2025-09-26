import os
import pytest
import backend.models as models

from fastapi.testclient import TestClient
from backend.database import get_db
from backend.main import create_app
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


@pytest.fixture(scope="session")
def setup_test_db():
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

    models.Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def get_test_db(setup_test_db):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=setup_test_db)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def get_test_client(get_test_db):
    # .dependency_overrides can't accept a fixture as an argument, hence the workaround
    def get_test_db_override():
        yield get_test_db

    app = create_app()
    app.dependency_overrides[get_db] = get_test_db_override

    client = TestClient(app)
    yield client
