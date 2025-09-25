import asyncio
import backend.analysis_engine as analysis_engine

from datetime import datetime, timezone

# --------------------------------- Integration Tests ---------------------------------

# analysis_engine.py functions can't be unit tested as they rely on an API call.
# Restructuring them for the sole purpose of 'true' unit tests is redundant.
# If a test here fails, you can run test_github_client.py with pytest to see if that's
#   where the problem lies.

# <<< Smoke Tests >>>


def test_get_commit_frequency() -> None:
    repo_url = "https://github.com/matslyk0/Gitsy"
    frequency = asyncio.run(analysis_engine.get_commit_frequency(repo_url))

    assert frequency is not None


def test_get_code_churn() -> None: # this one takes a while
    repo_url = "https://github.com/matslyk0/Gitsy"
    code_churn = asyncio.run(analysis_engine.get_code_churn(repo_url))

    assert code_churn is not None


def test_get_issues_close_time() -> None:
    repo_url = "https://github.com/matslyk0/Gitsy"
    issues_close_time = asyncio.run(analysis_engine.get_issues_close_time(repo_url))

    assert issues_close_time is not None


def test_get_pulls_close_time() -> None:
    repo_url = "https://github.com/matslyk0/Gitsy"
    pulls_close_time = asyncio.run(analysis_engine.get_pulls_close_time(repo_url))

    assert pulls_close_time is not None


# <<< Time Until >>>


def test_get_commit_frequency_until() -> None:
    repo_url = "https://github.com/matslyk0/Gitsy"
    time_until = datetime(2025, 6, 28, 12, 0, 0, tzinfo=timezone.utc)

    frequency = asyncio.run(
        analysis_engine.get_commit_frequency(repo_url, time_until=time_until)
    )

    assert frequency == 0.7296111111111111


def test_get_code_churn_until() -> None:
    repo_url = "https://github.com/matslyk0/Gitsy"
    time_until = datetime(2025, 6, 28, 12, 0, 0, tzinfo=timezone.utc)

    code_churn = asyncio.run(
        analysis_engine.get_code_churn(repo_url, time_until=time_until)
    )

    assert code_churn == {'additions': 89, 'deletions': 1, 'total': 90, 'net': 88}


def test_get_issues_close_time_until() -> None:
    repo_url = "https://github.com/matslyk0/Gitsy"
    time_until = datetime(2025, 7, 5, 12, 0, 0, tzinfo=timezone.utc)

    issues_close_time = asyncio.run(
        analysis_engine.get_issues_close_time(repo_url, time_until=time_until)
    )

    assert issues_close_time == 11.81888888888889


def test_get_pulls_close_time_until() -> None:
    repo_url = "https://github.com/matslyk0/Gitsy"
    time_until = datetime(2025, 7, 5, 12, 0, 0, tzinfo=timezone.utc)

    pulls_close_time = asyncio.run(
        analysis_engine.get_pulls_close_time(repo_url, time_until=time_until)
    )

    assert pulls_close_time == 0.010833333333333334


# <<< Time From and Until >>>


def test_get_commit_frequency_from_until() -> None:
    repo_url = "https://github.com/matslyk0/Gitsy"
    time_from = datetime(2024, 6, 28, 12, 0, 0, tzinfo=timezone.utc)
    time_until = datetime(2025, 6, 28, 12, 0, 0, tzinfo=timezone.utc)

    frequency = asyncio.run(
        analysis_engine.get_commit_frequency(repo_url, time_from, time_until)
    )

    assert frequency == 0.7296111111111111


def test_get_code_churn_from_until() -> None:
    repo_url = "https://github.com/matslyk0/Gitsy"
    time_from = datetime(2025, 7, 10, 13, 59, 0, tzinfo=timezone.utc)
    time_until = datetime(2025, 8, 4, 23, 59, 0, tzinfo=timezone.utc)

    code_churn = asyncio.run(
        analysis_engine.get_code_churn(repo_url, time_from, time_until)
    )

    assert code_churn == {"additions": 387, "deletions": 73, "total": 460, "net": 314}


def test_get_issues_close_time_from_until() -> None:
    repo_url = "https://github.com/matslyk0/Gitsy"
    time_from = datetime(2025, 6, 5, 12, 0, 0, tzinfo=timezone.utc)
    time_until = datetime(2025, 7, 5, 12, 0, 0, tzinfo=timezone.utc)

    issues_close_time = asyncio.run(
        analysis_engine.get_issues_close_time(repo_url, time_from, time_until)
    )

    assert issues_close_time == 11.81888888888889


def test_get_pulls_close_time_from_until() -> None:
    repo_url = "https://github.com/matslyk0/Gitsy"
    time_from = datetime(2025, 6, 5, 12, 0, 0, tzinfo=timezone.utc)
    time_until = datetime(2025, 7, 5, 12, 0, 0, tzinfo=timezone.utc)

    pulls_close_time = asyncio.run(
        analysis_engine.get_pulls_close_time(repo_url, time_from, time_until)
    )

    assert pulls_close_time == 0.010833333333333334
