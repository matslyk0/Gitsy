import os
import backend.models as models

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import engine
from backend.routers import reports, pages


def create_app():
    app = FastAPI()

    origins = ["http://localhost:5173/", # local frontend server
               "http://13.60.196.156"] # prod server

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # checks that it's not a testing environment
    if os.getenv("DB_HOST") == "database":
        models.Base.metadata.create_all(bind=engine)

    app.include_router(reports.router)
    app.include_router(pages.router)

    return app
