import os
import backend.models as models

from fastapi import FastAPI
from backend.database import engine
from backend.routers import reports, pages


def create_app():
    app = FastAPI()
    # checks if the container is the dev container
    if os.getenv("DB_HOST") == "database":
        models.Base.metadata.create_all(bind=engine)

    app.include_router(reports.router)
    app.include_router(pages.router)

    return app
