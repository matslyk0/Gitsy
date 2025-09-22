import asyncio
import logging
import backend.analysis_engine as analysis_engine

from zoneinfo import ZoneInfo
from datetime import datetime
from backend.exceptions import InsufficientDataError, CommitInfoError


def test_commit_frequency() -> None:
    repo_url = "https://github.com/matslyk0/Gitsy"
    frequency = 0

    timestamp = datetime.strptime("2025-06-28 12:00", "%Y-%m-%d %H:%M")
    timestamp = timestamp.replace(tzinfo=ZoneInfo("UTC"))

    try:
        frequency = asyncio.run(analysis_engine.get_commit_frequency(repo_url, time_until=timestamp))
    except InsufficientDataError as e:
        print(e)
    except Exception as e:
        logging.exception(f"Something unexpected went wrong: {e}")

    assert frequency == 0.7296111111111111


def test_code_churn() -> None:
    repo_url = "https://github.com/matslyk0/Gitsy"
    code_churn = {}

    time_from = datetime.strptime("2025-07-10 13:59", "%Y-%m-%d %H:%M")
    time_from = time_from.replace(tzinfo=ZoneInfo("UTC"))

    time_until = datetime.strptime("2025-08-04 23:59", "%Y-%m-%d %H:%M")
    time_until = time_until.replace(tzinfo=ZoneInfo("UTC"))

    try:
        code_churn = asyncio.run(analysis_engine.get_code_churn(repo_url, time_from, time_until))
    except CommitInfoError as e:
        print(e)
    except Exception as e:
        logging.exception(f"Something unexpected went wrong: {e}")

    assert code_churn == {'additions': 387,
                          'deletions': 73,
                          'total': 460,
                          'net': 314}


def test_issue_times() -> None:
    repo_url = "https://github.com/matslyk0/Gitsy"
    issue_close_time = 0

    timestamp = datetime.strptime("2025-08-04 23:59", "%Y-%m-%d %H:%M")
    timestamp = timestamp.replace(tzinfo=ZoneInfo("UTC"))

    try:
        issue_close_time = asyncio.run(analysis_engine.get_issue_times(repo_url, time_until=timestamp))
    except InsufficientDataError as e:
        print(e)
    except Exception as e:
        logging.exception(f"Something unexpected went wrong: {e}")

    assert issue_close_time == 279.3007407407407


def test_pull_times() -> None:
    repo_url = "https://github.com/matslyk0/Gitsy"
    pull_close_time = 0

    timestamp = datetime.strptime("2025-08-04 23:59", "%Y-%m-%d %H:%M")
    timestamp = timestamp.replace(tzinfo=ZoneInfo("UTC"))

    try:
        pull_close_time = asyncio.run(analysis_engine.get_pull_times(repo_url, time_until=timestamp))
    except InsufficientDataError as e:
        print(e)
    except Exception as e:
        logging.exception(f"Something went wrong: {e}")

    assert pull_close_time == 0.015208333333333334
