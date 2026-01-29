from pydantic import BaseModel, ConfigDict
from typing import Dict


class ReportOut(BaseModel):
    # needed by Pydantic for SQLAlchemy model to JSON conversion
    model_config = ConfigDict(from_attributes=True)

    commit_frequency: Dict
    code_churn: Dict
    issues_close_time: Dict
    pulls_close_time: Dict
