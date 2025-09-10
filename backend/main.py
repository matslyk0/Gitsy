import asyncio
import os
import backend.models as models
import backend.analysis_engine as analysis_engine

from typing import Annotated
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.database import engine, SessionLocal
from fastapi import FastAPI, HTTPException, Depends


class User(BaseModel):
    email: str
    hashed_password: str


class Repository(BaseModel):
    owner: str
    name: str


class Analysis(BaseModel):
    repository_id: str
    metric1: str
    metric2: str
    created_at: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]


def create_app():
    app = FastAPI()
    if os.getenv("DB_HOST") == "database":
        models.Base.metadata.create_all(bind=engine)


    @app.get("/", response_model=str)
    def home_page():
        return "Welcome to Gitsy!"


    @app.get("/get-started", response_model=str)
    def get_started():
        return "Let's get started with Gitsy!"


    @app.get("/create-report", response_model=str)
    def create_report():
        return "Let's create a report!"


    @app.get("/create-report/{repo_url:path}")
    async def create_report(repo_url: str):
        report = await asyncio.gather(
            analysis_engine.get_commit_frequency(repo_url),
            analysis_engine.get_code_churn(repo_url),
            analysis_engine.get_issue_times(repo_url),
            analysis_engine.get_pull_times(repo_url)
        )

        return {
            "commit_frequency": round(report[0], 2),
            "code_churn": report[1],
            "issue_times": round(report[2], 2),
            "pull_times": round(report[3], 2)
        }

    return app