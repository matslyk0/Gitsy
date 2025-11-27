import backend.crud as crud
import backend.schemas as schemas
import backend.analysis_engine as analysis_engine

from fastapi import APIRouter
from backend.database import postgres_context, redis_context

router = APIRouter()


@router.get("/create-report/generate", response_model=schemas.ReportOut)
async def create_report(repo_url: str, redis_host: str = "redis-db", ttl: int = 3600):
    repo_last_updated = await analysis_engine.get_last_updated(repo_url)

    with redis_context(host=redis_host, port=6379, decode_responses=True) as r:
        # A - check if redis has the report
        redis_report_id = crud.get_redis_report_id(repo_url)
        if await r.exists(redis_report_id):
            redis_report = await crud.get_redis_report(redis_report_id, r)

            # if redis report is stale, update redis and postgres
            if redis_report["last_updated"] < repo_last_updated:
                report = await analysis_engine.create_report(repo_url)

                with postgres_context() as session:
                    await crud.update_postgres_report(repo_url, report, session)
                    postgres_report = crud.get_postgres_report(repo_url, session)

                await crud.update_redis_report(redis_report_id, postgres_report, r, ttl)
                redis_report = await crud.get_redis_report(redis_report_id, r)

            return redis_report

        # B - check postgres if redis did not have the report
        with postgres_context() as session:
            postgres_report = crud.get_postgres_report(repo_url, session)
        if postgres_report is not None:
            # if postgres report is stale, update postgres before updating redis
            if postgres_report.last_updated < repo_last_updated:
                report = await analysis_engine.create_report(repo_url)

                with postgres_context() as session:
                    await crud.update_postgres_report(repo_url, report, session)
                    postgres_report = crud.get_postgres_report(repo_url, session)

            # update redis since it didn't have the report
            await crud.create_redis_report(postgres_report, redis_report_id, r, ttl)
            redis_report = await crud.get_redis_report(redis_report_id, r)

            return redis_report

        # C - no existing report in redis or postgres
        report = await analysis_engine.create_report(repo_url)

        with postgres_context() as session:
            await crud.create_postgres_report(repo_url, report, session)
            postgres_report = crud.get_postgres_report(repo_url, session)

        await crud.create_redis_report(postgres_report, redis_report_id, r, ttl)
        redis_report = await crud.get_redis_report(redis_report_id, r)

        return redis_report
