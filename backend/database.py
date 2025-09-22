import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends

# loaddot_env unnecessary - the environment variables are loaded by docker compose
POSTGRES_USER = os.getenv("POSTGRES_USER", "fallback_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "fallback_password")
POSTGRES_DB = os.getenv("POSTGRES_DB", "fallback_db")
DB_HOST = os.getenv("DB_HOST", "will_break_if_used")

DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:5432/{POSTGRES_DB}"

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
db_dependency: type[Annotated[Session, Depends(get_db)]] = Annotated[Session, Depends(get_db)]
