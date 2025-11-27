import os
import redis.asyncio as redis

from sqlalchemy import create_engine
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker, declarative_base

# the environment variables are loaded by docker compose in the backend container
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("DB_HOST")

DATABASE_URL = (
    f"postgresql+psycopg2://{POSTGRES_USER}:"
    f"{POSTGRES_PASSWORD}@{DB_HOST}:5432/{POSTGRES_DB}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


@contextmanager
def postgres_context():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@contextmanager
def redis_context(host: str, port: int, decode_responses: bool):
    r = redis.Redis(host=host, port=port, decode_responses=decode_responses)
    try:
        yield r
    finally:
        r.close()
