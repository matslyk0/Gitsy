import backend.crud as crud
import backend.models as models
import redis.asyncio as redis
import asyncio
import json
import time

from datetime import datetime, timezone

# --------------------------------- Integration Tests ---------------------------------

# The first 4 tests are 'interconnected' in a way, as they share the same database.
# Ideally they wouldn't be and all tests would be isolated thanks to rollbacks etc..

def test_create_db_report(get_test_db) -> None:
    repo_url = "https://github.com/matslyk0/Gitsy"
    db = get_test_db
    report_id = asyncio.run(crud.create_db_report(repo_url, db))
    print(f"\nCreateDBReport: {report_id}", flush=True)
    assert isinstance(report_id, int)


def test_get_report_id(get_test_db) -> None:
    repo_url = "https://github.com/matslyk0/Gitsy"
    db = get_test_db
    report_id_from_func = crud.get_report_id(repo_url, db)

    assert report_id_from_func == 1


def test_read_db_report(get_test_db) -> None:
    repo_url = "https://github.com/matslyk0/Gitsy"
    db = get_test_db
    report_id = crud.get_report_id(repo_url, db)

    db_report = crud.read_db_report(report_id, db)

    assert db_report.report_id == report_id


def test_update_db_report(get_test_db) -> None:
    db = get_test_db
    report = models.Reports(
        commit_frequency=0,
        code_churn={},
        issue_times=0,
        pull_times=0
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    repo_url = "https://github.com/matslyk0/Gitsy"
    asyncio.run(crud.update_db_report(repo_url, report, db))
    assert report.commit_frequency != 0
    assert report.code_churn != {}
    assert report.issue_times != 0
    assert report.pull_times != 0


def test_create_redis_report() -> None:
    async def test(): # workaround since async redis complicates things with sync pytest
        db_report = models.Reports(
            report_id=999,
            repo_id=999,
            commit_frequency=4.1111,
            code_churn={'additions': 89, 'deletions': 1, 'total': 90, 'net': 88},
            issue_times=5.11111,
            pull_times=6.1111111111,
            created_at=datetime.now(timezone.utc),
            last_updated=datetime.now(timezone.utc)
        )

        r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)
        redis_report_id = await crud.create_redis_report(db_report, r, ttl=10)
        redis_report = await r.hgetall(redis_report_id)

        try:
            assert redis_report != {}
            assert int(redis_report["repo_id"]) == db_report.repo_id
            assert float(redis_report["commit_frequency"]) == db_report.commit_frequency
            assert json.loads(redis_report["code_churn"]) == db_report.code_churn
            assert float(redis_report["issue_times"]) == db_report.issue_times
            assert float(redis_report["pull_times"]) == db_report.pull_times
            assert redis_report["created_at"] == db_report.created_at.isoformat()
            assert redis_report["last_updated"] == db_report.last_updated.isoformat()
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
            issue_times=5.11111,
            pull_times=6.1111111111,
            created_at=datetime.now(timezone.utc),
            last_updated=datetime.now(timezone.utc)
        )

        r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)
        redis_report_id = await crud.create_redis_report(db_report, r, ttl=100)

        db_report.commit_frequency = 4.44444
        db_report.code_churn = {'additions': 10, 'deletions': 10, 'total': 20, 'net': 0}
        db_report.issue_times = 300000
        db_report.pull_times = 40000000
        db_report.last_updated = datetime.now(timezone.utc)

        await crud.update_redis_report(redis_report_id, db_report, r, ttl=10)
        redis_report = await r.hgetall(redis_report_id)

        try:
            assert redis_report != {}
            assert float(redis_report["commit_frequency"]) == db_report.commit_frequency
            assert json.loads(redis_report["code_churn"]) == db_report.code_churn
            assert float(redis_report["issue_times"]) == db_report.issue_times
            assert float(redis_report["pull_times"]) == db_report.pull_times
            assert redis_report["last_updated"] == db_report.last_updated.isoformat()
            time.sleep(15)
            redis_report = await r.hgetall(f"reports:{db_report.report_id}")
            assert redis_report == {}
        finally:
            await r.close()

    asyncio.run(test())

