import redis.asyncio as redis
import backend.schemas as schemas
import backend.crud as crud
import backend.analysis_engine as analysis_engine

from backend.database import db_dependency
from fastapi import APIRouter


router = APIRouter()


@router.get("/create-report/generate", response_model=schemas.ReportOut)
async def create_report(
    db: db_dependency,
    repo_url: str,
    redis_host: str = "redis-db", # redis container name
    redis_ttl: int = 3600, # 1hr time to live
):
    repo_last_timestamp = await analysis_engine.get_last_updated(repo_url)

    # check redis first
    redis_report_id = crud.get_redis_report_id(repo_url)
    r = redis.Redis(host=redis_host, port=6379, decode_responses=True)
    if await r.exists(redis_report_id):
        redis_report = await crud.get_redis_report(redis_report_id, r)

        # need to update postgres and redis if the redis report is outdated
        redis_last_timestamp = redis_report["last_updated"]
        if redis_last_timestamp < repo_last_timestamp:
            postgres_report = crud.get_postgres_report(redis_report["report_id"], db)
            await crud.update_postgres_report(repo_url, postgres_report, db)
            await crud.update_redis_report(redis_report_id, postgres_report, r, redis_ttl)

        await r.close()
        return redis_report


    # check postgres if redis didn't have the report
    postgres_report_id = crud.get_postgres_report_id(repo_url, db)
    if postgres_report_id is not None:
        postgres_report = crud.get_postgres_report(postgres_report_id, db)

        # need to update postgres if the postgres report is outdated
        postgres_last_timestamp = postgres_report.last_updated
        if postgres_last_timestamp < repo_last_timestamp:
            await crud.update_postgres_report(repo_url, postgres_report, db)

        # create new redis report and return
        await crud.create_redis_report(postgres_report, redis_report_id, r, redis_ttl)
        redis_report = await crud.get_redis_report(redis_report_id, r)
        await r.close()
        return redis_report

    # otherwise, the repository doesn't exist in the database yet
    postgres_report_id = await crud.create_postgres_report(repo_url, db)
    postgres_report = crud.get_postgres_report(postgres_report_id, db)

    r = redis.Redis(host=redis_host, port=6379, decode_responses=True)
    await crud.create_redis_report(postgres_report, redis_report_id, r, redis_ttl)
    redis_report = await crud.get_redis_report(redis_report_id, r)
    await r.close()

    return redis_report
