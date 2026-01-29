import os
import backend.models as models
from fastapi import FastAPI
from backend.database import engine
from backend.routers import reports
from fastapi.middleware.cors import CORSMiddleware


def create_app():
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # create tables only if in dev; pytest handles table creation for test
    if os.getenv("DB_HOST") == "database":
        models.Base.metadata.create_all(bind=engine)

    app.include_router(reports.router)

    return app
