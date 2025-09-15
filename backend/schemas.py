from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import JSONB
from typing import Dict
from datetime import datetime

class Repository(BaseModel):
    repo_id: int
    repo_owner: str
    repo_name: str

    class Config:
        # needed by Pydantic for SQLAlchemy model to JSON conversion
        from_attributes = True


class Report(BaseModel):
    report_id: int
    repo_id: int

    commit_frequency: float
    code_churn: Dict[str, int]
    issue_times: float
    pull_times: float

    created_at: datetime
    last_updated: datetime


class ReportOut(BaseModel):
    commit_frequency: float
    code_churn: Dict[str, int]
    issue_times: float
    pull_times: float

    class Config:
        # needed by Pydantic for SQLAlchemy model to JSON conversion
        from_attributes = True