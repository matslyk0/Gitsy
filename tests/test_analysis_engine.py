import json
import logging
import backend.analysis_engine as analysis_engine
import backend.github_client
from backend.exceptions import GitHubAPIError, InsufficientDataError, CommitInfoError


def test_commit_frequency() -> None:
    repo_url = "https://github.com/matslyk0/Gitsy"
    frequency = 0

    try:
        frequency = analysis_engine.get_commit_frequency(repo_url)
    except InsufficientDataError as e:
        print(e)
    except Exception as e:
        logging.exception(f"Something unexpected went wrong: {e}")

    # This only checks if a calculation has happened,
    # this does not check the accuracy of the calculation,
    # that is to be implemented when analysis_engine is improved.
    assert frequency


def test_code_churn() -> None:
    repo_url = "https://github.com/matslyk0/Gitsy"
    code_churn = {}

    try:
        code_churn = analysis_engine.get_code_churn(repo_url)
    except CommitInfoError as e:
        print(e)
    except Exception as e:
        logging.exception(f"Something unexpected went wrong: {e}")

    assert code_churn


def test_issue_times() -> None:
    repo_url = "https://github.com/matslyk0/Gitsy"
    issue_close_time = 0

    try:
        issue_close_time = analysis_engine.get_issue_times(repo_url)
    except InsufficientDataError as e:
        print(e)
    except Exception as e:
        logging.exception(f"Something unexpected went wrong: {e}")

    assert issue_close_time


def test_pull_times() -> None:
    repo_url = "https://github.com/matslyk0/Gitsy"
    pull_close_time = 0

    try:
        pull_close_time = analysis_engine.get_pull_times(repo_url)
    except InsufficientDataError as e:
        print(e)
    except Exception as e:
        logging.exception(f"Something went wrong: {e}")

    assert pull_close_time
