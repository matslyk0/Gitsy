import redis.asyncio as redis
import backend.models as models
import backend.schemas as schemas
import backend.crud as crud
import backend.analysis_engine as analysis_engine

from backend.database import db_dependency
from fastapi import APIRouter


router = APIRouter()


@router.get("/create-report", response_model=str)
def create_report_page():
    return "Let's create a report!"


@router.get("/create-report/{repo_url:path}", response_model=schemas.ReportOut)
async def create_report(repo_url: str, db: db_dependency):
    repo_id = crud.get_repo_id(repo_url, db)
    db_has_report = repo_id is not None

    if db_has_report:
        repo_last_timestamp = await analysis_engine.get_last_updated(repo_url)

        db_report = crud.get_db_report(repo_id, db)

        r = redis.Redis(host="redis-db", port=6379, decode_responses=True)
        redis_report_id = f"reports:{db_report.report_id}"
        redis_has_report = await r.exists(redis_report_id)

        if redis_has_report:
            redis_report = r.hgetall(redis_report_id)
            redis_last_timestamp = redis_report["last_updated"]

            if redis_last_timestamp > repo_last_timestamp:
                await r.expire(redis_report_id, 3600)
                return redis_report

            # edge case of repository updating before redis report expires
            await crud.update_db_report(repo_url, db_report, db)
            await crud.update_redis_report(redis_report_id, db_report, r)
            return redis_report

        db_last_timestamp = (
            db.query(models.Reports.last_updated)
            .filter(models.Reports.repo_id == repo_id)
            .scalar()
        )
        if db_last_timestamp > repo_last_timestamp:
            await crud.create_redis_report(db_report, r)
            await r.close()
            return db_report

        await crud.update_db_report(repo_url, db_report, db)
        await crud.create_redis_report(db_report, r)
        await r.close()

        return db_report

    owner_and_repo = repo_url.removeprefix("https://github.com/")
    owner, _, repo_name = owner_and_repo.partition("/")
    repository = models.Repositories(repo_owner=owner, repo_name=repo_name)
    db_report = await crud.create_db_report(repo_url, repository)
    db.add(repository)
    db.add(db_report)
    db.commit()
    db.refresh(db_report)

    r = redis.Redis(host="redis-db", port=6379, decode_responses=True)
    await crud.create_redis_report(db_report, r)
    await r.close()

    return db_report
