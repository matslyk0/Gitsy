from pydantic import BaseModel
from typing import Dict, Union


class ReportOut(BaseModel):
    commit_frequency: Union[float, str]
    code_churn: Union[Dict[str, int], str]
    issues_close_time: float
    pulls_close_time: float

    class Config:
        # needed by Pydantic for SQLAlchemy model to JSON conversion
        from_attributes = True
