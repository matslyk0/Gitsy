from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Annotated

import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


class UsersBase(BaseModel):
    email: str
    hashed_password: str


class RepositoriesBase(BaseModel):
    owner: str
    name: str


class AnalysisBase(BaseModel):
    repository_id: str
    metric1: str
    metric2: str
    created_at: str


class DummyBase(BaseModel):
    test: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/dummy/{dummy_id}")
def list_dummies(dummy_id: int, db: db_dependency):
    result = db.query(models.Dummy).filter(dummy_id == models.Dummy.id).first()
    if not result:
        raise HTTPException(status_code=404, detail=f"Item {dummy_id} not found")
    return result


@app.post("/dummy")
def create_dummy(dummy: DummyBase, db: db_dependency):
    db_dummy = models.Dummy(test=dummy.test)
    db.add(db_dummy)
    db.commit()
    db.refresh(db_dummy)
    return db_dummy
