import asyncio
import backend.models as models
import backend.schemas as schemas
import backend.analysis_engine as analysis_engine

from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from backend.database import get_db


db_dependency = Annotated[Session, Depends(get_db)]
router = APIRouter()


async def generate_report(
    repo_url: str, repository: models.Repositories = None
) -> models.Reports:
    report_raw = await asyncio.gather(
        analysis_engine.get_commit_frequency(repo_url),
        analysis_engine.get_code_churn(repo_url),
        analysis_engine.get_issue_times(repo_url),
        analysis_engine.get_pull_times(repo_url),
    )

    report = models.Reports(
        commit_frequency=round(report_raw[0], 2),
        code_churn=report_raw[1],
        issue_times=round(report_raw[2], 2),
        pull_times=round(report_raw[3], 2),
    )

    if repository is not None:
        report.repository = repository

    return report


@router.get("/create-report", response_model=str)
def create_report_page():
    return "Let's create a report!"


@router.get("/create-report/{repo_url:path}", response_model=schemas.ReportOut)
async def create_report(repo_url: str, db: db_dependency):
    owner_and_repo = repo_url.removeprefix("https://github.com/")
    owner, _, repo_name = owner_and_repo.partition("/")
    repo_id = (
        db.query(models.Repositories.repo_id)
        .filter(
            models.Repositories.repo_owner == owner,
            models.Repositories.repo_name == repo_name,
        )
        .scalar()
    )

    if repo_id is not None:
        report = (
            db.query(models.Reports).filter(models.Reports.repo_id == repo_id).one()
        )

        repo_last_timestamp = await analysis_engine.get_last_updated(repo_url)

        # TBD WORRY ABOUT THIS LATER
        # if the report exists in redis:
        #     get the timestamp from redis
        #     if redis_last_timestamp > repo_last_timestamp:
        #         refresh the report TTL
        #         return that report as json
        #     else, the redis report is outdated:
        #         create a new report
        #         update the report in redis
        #         update the report in the db
        #         return the report
        # TBD WORRY ABOUT THIS LATER

        db_last_timestamp = (
            db.query(models.Reports.last_updated)
            .filter(models.Reports.repo_id == repo_id)
            .scalar()
        )

        if db_last_timestamp > repo_last_timestamp:
            # TBD refresh the redis TTL for existing report
            return report
        else:
            # create a new report and update the one in the db
            new_report = await generate_report(repo_url)
            report.commit_frequency = new_report.commit_frequency
            report.code_churn = new_report.code_churn
            report.issue_times = new_report.issue_times
            report.pull_times = new_report.pull_times

            db.commit()
            db.refresh(report)

            # TBD update the report in redis

            return report

    repository = models.Repositories(repo_owner=owner, repo_name=repo_name)
    report = await generate_report(repo_url, repository)

    db.add(repository)
    db.add(report)
    db.commit()
    db.refresh(report)

    return report
