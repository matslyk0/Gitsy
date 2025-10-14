import backend.crud as crud
import redis.asyncio as redis
import asyncio
import time

# --------------------------------- Integration Tests ---------------------------------


def test_create_report_empty_db(get_test_client, db_test_session):
    """Tests if a new report is stored in postgres and redis, and if the redis report expires as expected."""
    test_client = get_test_client
    db = db_test_session

    repo_url = "https://github.com/matslyk0/Gitsy"
    params = {"repo_url": repo_url, "redis_host": "127.0.0.1", "redis_ttl": 10}

    test_client.get(f"/create-report/generate", params=params)
    postgres_report_id = crud.get_postgres_report_id(repo_url, db)
    assert postgres_report_id == 1

    async def test_redis(): # workaround to solve async redis mixing with sync pytest
        r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)
        try:
            redis_report = await crud.get_redis_report("matslyk0:Gitsy", r)
            assert redis_report["report_id"] == postgres_report_id

            time.sleep(params["redis_ttl"])
            redis_report = await crud.get_redis_report("matslyk0:Gitsy", r)
            assert redis_report == {}
        finally:
            await r.close()

    asyncio.run(test_redis())


def test_redis_regenerates_report(get_test_client, db_test_session):
    """Tests if trying to create a report that already exists regenerates it in redis."""
    test_client = get_test_client
    db = db_test_session

    repo_url = "https://github.com/matslyk0/Gitsy"
    params = {"repo_url": repo_url, "redis_host": "127.0.0.1", "redis_ttl": 10}

    test_client.get(f"/create-report/generate", params=params)
    postgres_report_id = crud.get_postgres_report_id(repo_url, db)

    # wait for redis report to expire then call the endpoint again
    time.sleep(params["redis_ttl"])
    test_client.get(f"/create-report/generate", params=params)

    async def test_redis(): # workaround to solve async redis mixing with sync pytest
        r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)
        try:
            redis_report = await crud.get_redis_report("matslyk0:Gitsy", r)
            assert redis_report["report_id"] == postgres_report_id

            time.sleep(params["redis_ttl"])
            redis_report = await crud.get_redis_report("matslyk0:Gitsy", r)
            assert redis_report == {}
        finally:
            await r.close()

    asyncio.run(test_redis())
