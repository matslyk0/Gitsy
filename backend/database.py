import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DB_USER = os.getenv("POSTGRES_USER", "fallback_user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "fallback_password")
DB_NAME = os.getenv("POSTGRES_DB", "fallback_db")
DB_HOST = "database"

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
