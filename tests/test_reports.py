import time
import asyncio
import backend.crud as crud
import redis.asyncio as redis

from backend.database import redis_context

# --------------------------------- Integration Tests ---------------------------------


def test_main_endpoint_returns_report(get_test_client):
    """Checks that the endpoint returns the report once finished.

    Args:
        get_test_client (TestClient): FastAPI TestClient that simulates HTTP requests.

    Returns:
        Nothing.

    Raises:
        AssertionError: if the test fails.
    """
    test_client = get_test_client
    repo_url = "https://github.com/matslyk0/Gitsy"
    params = {"repo_url": repo_url, "redis_host": "redis-test-db"}

    response = test_client.get(f"/create-report/generate", params=params)
    assert response != {}

    async def clear_redis(): # sync/async workaround until async pytest is implemented
        host = "redis-test-db"
        async with redis_context(host=host, port=6379, decode_responses=True) as r:
            await r.flushdb()
            assert await r.dbsize() == 0
    asyncio.run(clear_redis())


def test_postgres_report_creation(get_test_client, db_test_session):
    """Tests if the endpoint successfully creates a report in postgres.
        The test client creates and tears down its own database sessions - another one
        is needed here to access the database.

    Args:
        get_test_client (TestClient): FastAPI TestClient that simulates HTTP requests.
        db_test_session (Session): Session with the testing database.

    Returns:
        Nothing.

    Raises:
        AssertionError: if the test fails.
    """
    test_client = get_test_client
    repo_url = "https://github.com/matslyk0/Gitsy"
    params = {"repo_url": repo_url, "redis_host": "redis-test-db"}

    test_client.get(f"/create-report/generate", params=params)

    session = db_test_session
    postgres_report = crud.get_postgres_report(repo_url, session)
    assert postgres_report is not None

    async def clear_redis(): # sync/async workaround until async pytest is implemented
        host = "redis-test-db"
        async with redis_context(host=host, port=6379, decode_responses=True) as r:
            await r.flushdb()
            assert await r.dbsize() == 0
    asyncio.run(clear_redis())


def test_redis_report_creation(get_test_client):
    """Tests if the endpoint successfully creates a report in redis, and if the report
        expires in redis.

    Args:
        get_test_client (TestClient): FastAPI TestClient that simulates HTTP requests.

    Returns:
        Nothing.

    Raises:
        AssertionError: if the test fails.
    """

    test_client = get_test_client
    repo_url = "https://github.com/matslyk0/Gitsy"
    params = {"repo_url": repo_url, "redis_host": "redis-test-db", "ttl": 10}

    test_client.get(f"/create-report/generate", params=params)

    async def redis_test(): # sync/async workaround until async pytest is implemented
        host = "redis-test-db"
        async with redis_context(host=host, port=6379, decode_responses=True) as r:
            redis_report = await crud.get_redis_report("matslyk0:Gitsy", r)
            assert redis_report != {}

            time.sleep(params["ttl"]+1)
            redis_report = await crud.get_redis_report("matslyk0:Gitsy", r)
            assert redis_report == {}
    asyncio.run(redis_test())


def test_redis_report_regeneration(get_test_client):
    """Tests if trying to recreate an existing report regenerates an expired redis
        report.

    Args:
        get_test_client (TestClient): FastAPI TestClient that simulates HTTP requests.

    Returns:
        Nothing.

    Raises:
        AssertionError: if the test fails.
    """
    test_client = get_test_client
    repo_url = "https://github.com/matslyk0/Gitsy"
    params = {"repo_url": repo_url, "redis_host": "redis-test-db", "ttl": 10}

    test_client.get(f"/create-report/generate", params=params)
    time.sleep(params["ttl"]+1) # wait for redis report to expire
    test_client.get(f"/create-report/generate", params=params)

    async def redis_test(): # sync/async workaround until async pytest is implemented
        host = "redis-test-db"
        async with redis_context(host=host, port=6379, decode_responses=True) as r:
            redis_report = await crud.get_redis_report("matslyk0:Gitsy", r)
            assert redis_report != {}
    asyncio.run(redis_test())
