import json
import logging
import backend.github_client

def test_commits(repo_url: str) -> None:
    """Tests get_commits from github_client.py"""
    try:
        commits = get_commits(repo_url)
        print(json.dumps(commits, indent=4))
    except GithubAPIError as e:
        print(e)
    except Exception as e:
        logging.exception(f"Something unexpected went wrong: {e}")


def test_commit_frequency(repo_url: str) -> None:
    user_and_repo = repo_url.removeprefix("https://github.com/")
    user, separator, repo = user_and_repo.partition("/")
    try:
        hours_between_commits = get_commit_frequency(repo_url)
        print(
            f"{repo} has a commit every {hours_between_commits:.2f} hours!"
        )
    except (GithubAPIError, InsufficientDataError) as e:
        print(e)
    except Exception as e:
        logging.exception(f"Something unexpected went wrong: {e}")


def test_code_churn(repo_url: str) -> None:
    try:
        print(get_code_churn(repo_url))
    except GithubAPIError as e:
        print(e)
    except Exception as e:
        logging.exception(f"Something unexpected went wrong: {e}")


def test_issue_times(repo_url: str) -> None:
    user_and_repo = repo_url.removeprefix("https://github.com/")
    user, separator, repo = user_and_repo.partition("/")
    try:
        issue_close_time = get_issue_times(repo_url)
        print(f"{repo} closes an issue every {issue_close_time:.2f} hours!")
    except (GithubAPIError, InsufficientDataError) as e:
        print(e)
    except Exception as e:
        logging.exception(f"Something unexpected went wrong: {e}")


def test_pull_times(repo_url: str) -> None:
    user_and_repo = repo_url.removeprefix("https://github.com/")
    user, separator, repo = user_and_repo.partition("/")
    try:
        pull_close_time = get_pull_times(repo_url)
        print(f"{repo} merges a pull request every {pull_close_time:.4f} hours!")
    except (GithubAPIError, InsufficientDataError) as e:
        print(e)
    except Exception as e:
        logging.exception(f"Something went wrong: {e}")
