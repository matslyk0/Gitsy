import os
import backend.models as models
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


class Dummy(BaseModel):
    item: str


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

    @app.get("/dummy/{dummy_id}", response_model=Dummy)
    def get_dummy(dummy_id: int, db: db_dependency):
        result = db.query(models.Dummy).filter(dummy_id == models.Dummy.id).first()
        if not result:
            raise HTTPException(status_code=404, detail=f"Item {dummy_id} not found")
        return result


    @app.get("/dummy", response_model=list[Dummy])
    def list_dummies(db: db_dependency):
        dummies = db.query(models.Dummy).all()
        return dummies


    @app.post("/dummy")
    def create_dummy(dummy: Dummy, db: db_dependency):
        db_dummy = models.Dummy(item=dummy.item)
        db.add(db_dummy)
        db.commit()
        db.refresh(db_dummy)
        return db_dummy

    return app
