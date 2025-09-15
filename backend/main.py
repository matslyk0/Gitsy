import asyncio
import os
import backend.models as models
import backend.schemas as schemas
import backend.analysis_engine as analysis_engine

from fastapi import FastAPI, HTTPException, Depends
from backend.database import get_db, engine
from backend.routers import reports, pages


def create_app():
    app = FastAPI()
    # checks if the container is the dev container
    if os.getenv("DB_HOST") == "database":
        models.Base.metadata.create_all(bind=engine)

    app.include_router(reports.router)
    app.include_router(pages.router)

    return app
