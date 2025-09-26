from datetime import datetime, timezone

from sqlalchemy.orm import relationship

from backend.database import Base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime


class Repositories(Base):
    __tablename__ = "repositories"

    repo_id = Column(Integer, primary_key=True, index=True)
    repo_owner = Column(String, index=True)
    repo_name = Column(String, index=True)

    reports = relationship("Reports", back_populates="repository")


class Reports(Base):
    __tablename__ = "reports"

    report_id = Column(Integer, primary_key=True, index=True)
    repo_id = Column(Integer, ForeignKey("repositories.repo_id"), index=True)

    commit_frequency = Column(Float, index=True)
    code_churn = Column(JSONB, index=True)
    issue_times = Column(Float, index=True)
    pull_times = Column(Float, index=True)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True
    )
    last_updated = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        index=True,
    )

    repository = relationship("Repositories", back_populates="reports")
