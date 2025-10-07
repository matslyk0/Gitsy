import backend.crud as crud
import redis.asyncio as redis
import asyncio
import time

# --------------------------------- Integration Tests ---------------------------------

# These two tests are linked because they share the database.
# Test 2 won't pass unless Test 1 is run first, this is intended for now.

def test_create_report_empty_db(get_test_client, get_test_db):
    test_client = get_test_client
    db = get_test_db
    repo_url = "https://github.com/matslyk0/Gitsy"

    params = {"repo_url": repo_url, "redis_host": "127.0.0.1", "redis_ttl": 10}
    test_client.get(f"/create-report/generate", params=params)

    report_id = crud.get_postgres_report_id(repo_url, db)
    assert report_id == 1

    async def test_redis(): # workaround to solve async redis mixing with sync pytest
        r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)
        try:
            redis_report = await r.hgetall("matslyk0:Gitsy")
            assert redis_report != {}

            time.sleep(params["redis_ttl"])
            redis_report = await r.hgetall("matslyk0:Gitsy")
            assert redis_report == {}
        finally:
            await r.close()

    asyncio.run(test_redis())


def test_create_report_populated_db(get_test_client):
    """When this test runs, Redis should not contain the report."""
    test_client = get_test_client
    repo_url = "https://github.com/matslyk0/Gitsy"
    params = {"repo_url": repo_url, "redis_host": "127.0.0.1", "redis_ttl": 10}

    # finds report in postgres and refreshes the redis report
    test_client.get(f"/create-report/generate", params=params)

    # all of these should pass as the GET request would regenerate the redis report
    async def test_redis(): # workaround to solve async redis mixing with sync pytest
        r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)
        try:
            redis_report = await r.hgetall("matslyk0:Gitsy")
            assert redis_report != {}

            time.sleep(params["redis_ttl"])
            redis_report = await r.hgetall("matslyk0:Gitsy")
            assert redis_report == {}
        finally:
            await r.close()

    asyncio.run(test_redis())
