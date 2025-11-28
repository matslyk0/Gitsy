import time
import asyncio
import backend.crud as crud
import backend.analysis_engine as analysis_engine

from backend.database import redis_context
from backend.models import Reports
from datetime import datetime, timezone

# --------------------------------- Integration Tests ---------------------------------


def test_create_and_get_postgres_report(db_test_session):
    """Tests if crud.create_postgres_report and crud.get_postgres_report works.

    Args:
        db_test_session: a session with the testing database.

    Returns:
        Nothing.

    Raises:
        AssertionError: if the test fails.
    """
    repo_url = "https://github.com/matslyk0/Gitsy"
    report = asyncio.run(analysis_engine.create_report(repo_url))

    session = db_test_session
    asyncio.run(crud.create_postgres_report(repo_url, report, session))
    postgres_report = crud.get_postgres_report(repo_url, session)

    assert isinstance(postgres_report, Reports)


def test_update_postgres_report(db_test_session) -> None:
    """Tests if crud.update_postgres_report works.

    Args:
        db_test_session: a session with the testing database.

    Returns:
        Nothing.

    Raises:
        AssertionError: if the test fails.
    """
    example_report = {
        "commit_frequency": {
            "status_code": 200,
            "data": 30.1,
            "error_name": None,
            "error_message": None,
        }
    }

    postgres_report = Reports(**example_report)
    session = db_test_session
    session.add(postgres_report)
    session.commit()
    session.refresh(postgres_report)

    modified_report = {
        "commit_frequency": {
            "status_code": 200,
            "data": 11.22,
            "error_name": None,
            "error_message": None,
        }
    }

    repo_url = "https://github.com/matslyk0/Gitsy"
    asyncio.run(crud.update_postgres_report(repo_url, modified_report, session))
    postgres_report = crud.get_postgres_report(repo_url, session)
    assert postgres_report.commit_frequency == modified_report["commit_frequency"]


def test_create_and_get_redis_report() -> None:
    """Tests if crud.create_redis_report and crud.get_redis_report works.

    Returns:
        Nothing.

    Raises:
        AssertionError: if the test fails.
    """
    async def redis_test():  # sync/async workaround until async pytest is implemented

        # simulating a complete postgres report
        postgres_report = Reports(
            report_id=999,
            repo_id=999,
            commit_frequency={
                "status_code": 200,
                "data": 4.1111,
                "error_name": None,
                "error_message": None,
            },
            code_churn={
                "status_code": 200,
                "data": {"additions": 89, "deletions": 1, "total": 90, "net": 88},
                "error_name": None,
                "error_message": None,
            },
            issues_close_time={
                "status_code": 200,
                "data": 5.11111,
                "error_name": None,
                "error_message": None,
            },
            pulls_close_time={
                "status_code": 200,
                "data": 6.1111111111,
                "error_name": None,
                "error_message": None,
            },
            created_at=datetime.now(timezone.utc),
            last_updated=datetime.now(timezone.utc),
        )

        host = "redis-test-db"
        async with redis_context(host=host, port=6379, decode_responses=True) as r:
            redis_report_id = "admin:test"
            await crud.create_redis_report(postgres_report, redis_report_id, r, ttl=10)
            redis_report = await crud.get_redis_report(redis_report_id, r)

            assert redis_report != {}
            assert redis_report["report_id"] == postgres_report.report_id
            assert redis_report["repo_id"] == postgres_report.repo_id
            assert redis_report["commit_frequency"] == postgres_report.commit_frequency
            assert redis_report["code_churn"] == postgres_report.code_churn
            assert (
                redis_report["issues_close_time"] == postgres_report.issues_close_time
            )
            assert redis_report["pulls_close_time"] == postgres_report.pulls_close_time
            assert redis_report["created_at"] == postgres_report.created_at
            assert redis_report["last_updated"] == postgres_report.last_updated

            time.sleep(11)
            redis_report = await crud.get_redis_report(redis_report_id, r)
            assert redis_report == {}

    asyncio.run(redis_test())


def test_update_redis_report() -> None:
    """Tests if crud.update_redis_report works.

    Returns:
        Nothing.

    Raises:
        AssertionError: if the test fails.

    """
    postgres_report = Reports(
        report_id=999,
        repo_id=999,
        commit_frequency={
            "status_code": 200,
            "data": 4.1111,
            "error_name": None,
            "error_message": None,
        },
        code_churn={
            "status_code": 200,
            "data": {"additions": 89, "deletions": 1, "total": 90, "net": 88},
            "error_name": None,
            "error_message": None,
        },
        issues_close_time={
            "status_code": 200,
            "data": 5.11111,
            "error_name": None,
            "error_message": None,
        },
        pulls_close_time={
            "status_code": 200,
            "data": 6.1111111111,
            "error_name": None,
            "error_message": None,
        },
        created_at=datetime.now(timezone.utc),
        last_updated=datetime.now(timezone.utc),
    )

    async def redis_test():  # sync/async workaround until async pytest is implemented
        host = "redis-test-db"
        async with redis_context(host=host, port=6379, decode_responses=True) as r:
            await crud.create_redis_report(postgres_report, "admin:test", r, ttl=10)

            postgres_report.commit_frequency["data"] = 494
            await crud.update_redis_report("admin:test", postgres_report, r, ttl=10)
            redis_report = await crud.get_redis_report("admin:test", r)

            assert redis_report != {}
            assert redis_report["commit_frequency"]["data"] == 494
            time.sleep(11)
            redis_report = await crud.get_redis_report("admin:test", r)
            assert redis_report == {}
    asyncio.run(redis_test())
