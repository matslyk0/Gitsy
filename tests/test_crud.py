import backend.crud as crud
import backend.models as models
import redis.asyncio as redis
import asyncio
import json
import time

from datetime import datetime, timezone

# --------------------------------- Integration Tests ---------------------------------

def test_create_postgres_report(db_test_session) -> None:
    repo_url = "https://github.com/matslyk0/Gitsy"
    db = db_test_session
    report_id = asyncio.run(crud.create_postgres_report(repo_url, db))
    assert isinstance(report_id, int)


def test_get_postgres_report_id(db_test_session) -> None:
    repo_url = "https://github.com/matslyk0/Gitsy"
    db = db_test_session
    report_id = asyncio.run(crud.create_postgres_report(repo_url, db))
    report_id_from_func = crud.get_postgres_report_id(repo_url, db)

    assert report_id_from_func == report_id


def test_get_postgres_report(db_test_session) -> None:
    repo_url = "https://github.com/matslyk0/Gitsy"
    db = db_test_session
    report_id = asyncio.run(crud.create_postgres_report(repo_url, db))
    db_report = crud.get_postgres_report(report_id, db)
    assert db_report.report_id == report_id


def test_update_postgres_report(db_test_session) -> None:
    # make a mock database report
    db = db_test_session
    report = models.Reports(
        commit_frequency=0,
        code_churn={},
        issues_close_time=0,
        pulls_close_time=0
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    repo_url = "https://github.com/matslyk0/Gitsy"
    asyncio.run(crud.update_postgres_report(repo_url, report, db))

    assert report.commit_frequency != 0
    assert report.code_churn != {}
    assert report.issues_close_time != 0
    assert report.pulls_close_time != 0


def test_create_redis_report() -> None:
    async def test(): # workaround since async redis complicates things with sync pytest
        db_report = models.Reports(
            report_id=999,
            repo_id=999,
            commit_frequency=4.1111,
            code_churn={'additions': 89, 'deletions': 1, 'total': 90, 'net': 88},
            issues_close_time=5.11111,
            pulls_close_time=6.1111111111,
            created_at=datetime.now(timezone.utc),
            last_updated=datetime.now(timezone.utc)
        )

        r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)
        redis_report_id = "admin:test"
        await crud.create_redis_report(db_report, redis_report_id, r, ttl=10)
        redis_report = await crud.get_redis_report("admin:test", r)

        try:
            assert redis_report != {}
            assert int(redis_report["report_id"]) == db_report.report_id
            assert int(redis_report["repo_id"]) == db_report.repo_id
            assert float(redis_report["commit_frequency"]) == db_report.commit_frequency
            assert redis_report["code_churn"] == db_report.code_churn
            assert float(redis_report["issues_close_time"]) == db_report.issues_close_time
            assert float(redis_report["pulls_close_time"]) == db_report.pulls_close_time
            assert redis_report["created_at"] == db_report.created_at
            assert redis_report["last_updated"] == db_report.last_updated
            time.sleep(10)
            redis_report = await r.hgetall(f"reports:{db_report.report_id}")
            assert redis_report == {}
        finally:
            await r.close()

    asyncio.run(test())


def test_update_redis_report() -> None:
    async def test(): # workaround since async redis complicates things with sync pytest
        db_report = models.Reports(
            report_id=999,
            repo_id=999,
            commit_frequency=4.1111,
            code_churn={'additions': 89, 'deletions': 1, 'total': 90, 'net': 88},
            issues_close_time=5.11111,
            pulls_close_time=6.1111111111,
            created_at=datetime.now(timezone.utc),
            last_updated=datetime.now(timezone.utc)
        )

        r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)
        redis_report_id = "admin:test"
        await crud.create_redis_report(db_report, redis_report_id, r, ttl=100)

        db_report.commit_frequency = 4.44444
        db_report.code_churn = {'additions': 10, 'deletions': 10, 'total': 20, 'net': 0}
        db_report.issues_close_time = 300000
        db_report.pulls_close_time = 40000000
        db_report.last_updated = datetime.now(timezone.utc)

        await crud.update_redis_report(redis_report_id, db_report, r, ttl=10)
        redis_report = await r.hgetall(redis_report_id)

        try:
            assert redis_report != {}
            assert float(redis_report["commit_frequency"]) == db_report.commit_frequency
            assert json.loads(redis_report["code_churn"]) == db_report.code_churn
            assert float(redis_report["issues_close_time"]) == db_report.issues_close_time
            assert float(redis_report["pulls_close_time"]) == db_report.pulls_close_time
            assert redis_report["last_updated"] == db_report.last_updated.isoformat()
            time.sleep(15)
            redis_report = await r.hgetall(f"reports:{db_report.report_id}")
            assert redis_report == {}
        finally:
            await r.close()

    asyncio.run(test())

