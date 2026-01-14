import json
import redis.asyncio as redis
import backend.helpers as helpers
import backend.analysis_helpers as analysis_helpers
from sqlalchemy import update
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from backend.models import Repositories, Reports

# <<< postgres operations >>>


async def create_postgres_report(repo_url: str, report: dict, session: Session) -> None:
    """Adds the repository to postgres, creates a report and stores it postgres, then
        returns the report id.

    Args:
        repo_url (str): The URL of the repository in the format
                        https://github.com/owner/repo
        session (Session): The database session to talk to postgres.
        report:

    Returns:
        int: The id of the report in postgres.
    """

    repo_owner, repo_name = helpers.get_owner_and_repo(repo_url)
    stmt_repo = (
        insert(Repositories)
        .values(repo_owner=repo_owner, repo_name=repo_name)
        .on_conflict_do_update(
            index_elements=[Repositories.repo_owner, Repositories.repo_name],
            set_={
                "repo_owner": repo_owner
            },  # dummy update so repo_id is always returned
        )
        .returning(Repositories.repo_id)
    )
    repo_id = session.execute(stmt_repo).scalar()

    stmt_report = (
        insert(Reports)
        .values(repo_id=repo_id, **report)
        .on_conflict_do_update(index_elements=[Reports.repo_id], set_=report)
        .returning(Reports.report_id)
    )
    session.execute(stmt_report).scalar()
    session.commit()


def get_postgres_report(repo_url: str, session: Session) -> Reports | None:
    owner, repo_name = helpers.get_owner_and_repo(repo_url)

    repo_id = (
        session.query(Repositories.repo_id)
        .filter(Repositories.repo_owner == owner, Repositories.repo_name == repo_name)
        .scalar()
    )

    report_id = (
        session.query(Reports.report_id).filter(Reports.repo_id == repo_id).scalar()
    )

    postgres_report = (
        session.query(Reports).filter(Reports.report_id == report_id).one_or_none()
    )

    return postgres_report


async def update_postgres_report(repo_url: str, report: dict, session: Session) -> None:
    """Updates the report in the database."""
    postgres_report = get_postgres_report(repo_url, session)
    stmt = (
        update(Reports)
        .where(Reports.report_id == postgres_report.report_id)
        .values(**report)
    )

    session.execute(stmt)
    session.commit()
    session.refresh(postgres_report)  # so the timestamps can be passed to Redis


# <<< redis operations >>>


async def create_redis_report(
    postgres_report: Reports, redis_report_id: str, r: redis.Redis, ttl: int
) -> None:
    serialised_commit_frequency = json.dumps(postgres_report.commit_frequency)
    serialised_code_churn = json.dumps(postgres_report.code_churn)
    serialised_issues_close_time = json.dumps(postgres_report.issues_close_time)
    serialised_pulls_close_time = json.dumps(postgres_report.pulls_close_time)

    iso_created_at = postgres_report.created_at.isoformat()
    iso_last_updated = postgres_report.last_updated.isoformat()

    await r.hset(
        redis_report_id,
        mapping={
            "report_id": postgres_report.report_id,
            "repo_id": postgres_report.repo_id,
            "commit_frequency": serialised_commit_frequency,
            "code_churn": serialised_code_churn,
            "issues_close_time": serialised_issues_close_time,
            "pulls_close_time": serialised_pulls_close_time,
            "created_at": iso_created_at,
            "last_updated": iso_last_updated,
        },
    )

    await r.expire(redis_report_id, ttl)


async def get_redis_report(redis_report_id: str, r: redis.Redis) -> dict | None:
    """Returns the redis report with correct data types"""
    redis_report = await r.hgetall(redis_report_id)

    if redis_report == {}:
        return redis_report

    parsed_report = {
        "report_id": int(redis_report["report_id"]),
        "repo_id": int(redis_report["repo_id"]),
        "commit_frequency": json.loads(redis_report["commit_frequency"]),
        "code_churn": json.loads(redis_report["code_churn"]),
        "issues_close_time": json.loads(redis_report["issues_close_time"]),
        "pulls_close_time": json.loads(redis_report["pulls_close_time"]),
        "created_at": analysis_helpers.parse_timestamp(redis_report["created_at"]),
        "last_updated": analysis_helpers.parse_timestamp(redis_report["last_updated"]),
    }

    return parsed_report


async def update_redis_report(
    redis_report_id: str, postgres_report: Reports, r: redis.Redis, ttl: int
) -> None:
    serialised_commit_frequency = json.dumps(postgres_report.commit_frequency)
    serialised_code_churn = json.dumps(postgres_report.code_churn)
    serialised_issues_close_time = json.dumps(postgres_report.issues_close_time)
    serialised_pulls_close_time = json.dumps(postgres_report.pulls_close_time)

    iso_last_updated = postgres_report.last_updated.isoformat()

    mapping = {
        "commit_frequency": serialised_commit_frequency,
        "code_churn": serialised_code_churn,
        "issues_close_time": serialised_issues_close_time,
        "pulls_close_time": serialised_pulls_close_time,
        "last_updated": iso_last_updated,
    }
    await r.hset(redis_report_id, mapping=mapping)
    await r.expire(redis_report_id, ttl)


# TODO: move or get rid of this
def get_redis_report_id(repo_url) -> str:
    owner, repo_name = helpers.get_owner_and_repo(repo_url)
    return f"{owner}:{repo_name}"
