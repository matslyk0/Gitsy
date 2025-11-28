from datetime import datetime, timezone

from sqlalchemy.orm import relationship

from backend.database import Base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, UniqueConstraint


class Repositories(Base):
    __tablename__ = "repositories"
    __table_args__ = (
        UniqueConstraint("repo_owner", "repo_name"),
    )

    repo_id = Column(Integer, primary_key=True, index=True)
    repo_owner = Column(String, index=True)
    repo_name = Column(String, index=True)

    reports = relationship("Reports", back_populates="repository")


class Reports(Base):
    __tablename__ = "reports"
    __table_args__ = (
        UniqueConstraint("repo_id"),
    )

    report_id = Column(Integer, primary_key=True, index=True)
    repo_id = Column(Integer, ForeignKey("repositories.repo_id"), index=True)

    commit_frequency = Column(JSONB, index=True)
    code_churn = Column(JSONB, index=True)
    issues_close_time = Column(JSONB, index=True)
    pulls_close_time = Column(JSONB, index=True)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )
    last_updated = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        index=True,
    )

    repository = relationship("Repositories", back_populates="reports")
