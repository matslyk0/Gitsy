import json
import redis.asyncio as redis
import backend.models as models
import backend.schemas as schemas
import backend.crud as crud
import backend.analysis_engine as analysis_engine
import backend.analysis_helpers as analysis_helpers

from backend.database import db_dependency
from fastapi import APIRouter


router = APIRouter()


@router.get("/create-report/generate", response_model=schemas.ReportOut)
async def create_report(
    db: db_dependency,
    repo_url: str,
    redis_host: str = "redis-db",
    redis_ttl: int = 3600,
):
    report_id = crud.get_report_id(repo_url, db)
    db_has_report = report_id is not None

    if db_has_report:
        repo_last_timestamp = await analysis_engine.get_last_updated(repo_url)

        db_report = crud.read_db_report(report_id, db)

        r = redis.Redis(host=redis_host, port=6379, decode_responses=True)
        redis_report_id = f"reports:{db_report.report_id}"
        redis_has_report = await r.exists(redis_report_id)

        if redis_has_report:
            redis_report = await r.hgetall(redis_report_id)
            redis_report["code_churn"] = json.loads(redis_report["code_churn"])
            redis_last_timestamp_raw = redis_report["last_updated"]
            redis_last_timestamp = analysis_helpers.parse_timestamp(
                redis_last_timestamp_raw
            )

            if redis_last_timestamp > repo_last_timestamp:
                await r.expire(redis_report_id, redis_ttl)
                return redis_report

            # edge case of repository updating before redis report expires
            await crud.update_db_report(repo_url, db_report, db)
            await crud.update_redis_report(redis_report_id, db_report, r, redis_ttl)
            return redis_report

        db_last_timestamp = (
            db.query(models.Reports.last_updated)
            .filter(models.Reports.report_id == report_id)
            .scalar()
        )
        if db_last_timestamp > repo_last_timestamp:
            await crud.create_redis_report(db_report, r, redis_ttl)
            await r.close()
            return db_report

        await crud.update_db_report(repo_url, db_report, db)
        await crud.create_redis_report(db_report, r, redis_ttl)
        await r.close()

        return db_report
    else: # there is no report in db
        report_id = await crud.create_db_report(repo_url, db)
        db_report = crud.read_db_report(report_id, db)

        r = redis.Redis(host=redis_host, port=6379, decode_responses=True)
        await crud.create_redis_report(db_report, r, redis_ttl)
        await r.close()

        return db_report
