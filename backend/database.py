import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends

# the environment variables are loaded by docker compose in the backend container
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
DB_HOST = "database" # the postgres container name - same name for prod and dev

DATABASE_URL = (
    f"postgresql+psycopg2://{POSTGRES_USER}:"
    f"{POSTGRES_PASSWORD}@{DB_HOST}:5432/{POSTGRES_DB}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# type alias needed so importing in another file doesn't cause IDE to flag an error
db_dependency: type[Annotated[Session, Depends(get_db)]] = Annotated[
    Session, Depends(get_db)
]
