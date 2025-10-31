from pydantic import BaseModel
from typing import Dict

class ReportOut(BaseModel):
    commit_frequency: float
    code_churn: Dict[str, int]
    issues_close_time: float
    pulls_close_time: float

    class Config:
        # needed by Pydantic for SQLAlchemy model to JSON conversion
        from_attributes = True
