from pydantic import BaseModel
from typing import Dict, Union


class ReportOut(BaseModel):
    commit_frequency: Dict
    code_churn: Dict
    issues_close_time: Dict
    pulls_close_time: Dict

    class Config:
        # needed by Pydantic for SQLAlchemy model to JSON conversion
        from_attributes = True
