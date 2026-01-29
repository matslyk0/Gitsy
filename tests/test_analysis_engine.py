import asyncio
import backend.analysis_engine as analysis_engine

from datetime import datetime, timezone


def test_get_commit_frequency() -> None:  # Integration Test
    repo_url = "https://github.com/matslyk0/Gitsy"
    frequency = asyncio.run(analysis_engine.get_commit_frequency(repo_url))

    assert frequency is not None


def test_get_code_churn() -> None:  # Integration Test
    repo_url = "https://github.com/matslyk0/Gitsy"
    code_churn = asyncio.run(analysis_engine.get_code_churn(repo_url))

    assert code_churn is not None


def test_get_issues_close_time() -> None:  # Integration Test
    repo_url = "https://github.com/matslyk0/Gitsy"
    issues_close_time = asyncio.run(analysis_engine.get_issues_close_time(repo_url))

    assert issues_close_time is not None


def test_get_pulls_close_time() -> None:  # Integration Test
    repo_url = "https://github.com/matslyk0/Gitsy"
    pulls_close_time = asyncio.run(analysis_engine.get_pulls_close_time(repo_url))

    assert pulls_close_time is not None


def test_get_last_updated() -> None:  # Integration Test
    repo_url = "https://github.com/matslyk0/Gitsy"
    last_updated = asyncio.run(analysis_engine.get_last_updated(repo_url))

    assert isinstance(last_updated, datetime)


def test_create_report() -> None:  # Integration Test
    repo_url = "https://github.com/matslyk0/Gitsy"
    report = asyncio.run(analysis_engine.create_report(repo_url))

    assert report["commit_frequency"] is not None
    assert report["code_churn"] is not None
    assert report["issues_close_time"] is not None
    assert report["pulls_close_time"] is not None
