import asyncio
import backend.github_client as github_client
import backend.analysis_helpers as analysis_helpers

from datetime import datetime, timedelta
from backend.exceptions import (
    InsufficientCommitsError,
    InsufficientPullsError,
    InsufficientIssuesError,
    RepoTooLargeError,
)

# for script-only testing
# import json
# import time


async def get_commit_frequency(
    repo_url: str, time_from: datetime = None, time_until: datetime = None
) -> float:
    """Calculates the average number of hours between commits for a repository.

    Args:
        repo_url (str): The URL of the repository in the format
                        https://github.com/owner/repo
        time_from (datetime): The time to start looking from.
        time_until (datetime): The time to start looking until.

    Returns:
        float: The average number of hours between commits.

    Raises:
         GitHubAPIError: If the request to GitHub failed.
         InsufficientCommitsError: If the repository has less than 2 commits.
    """
    commits = await github_client.get_commits(repo_url)

    total_commits = len(commits)
    if total_commits < 2:
        raise InsufficientCommitsError()

    if time_from:
        keys = ["commit", "author", "date"]
        first_timestamp, commits_diff = analysis_helpers.get_first_timestamp(
            time_from, commits, keys
        )
        total_commits -= commits_diff
    else:
        first_timestamp = commits[-1]["commit"]["author"]["date"]
        first_timestamp = analysis_helpers.parse_timestamp(first_timestamp)

    if time_until:
        keys = ["commit", "author", "date"]
        latest_timestamp, commits_diff = analysis_helpers.get_latest_timestamp(
            time_until, commits, keys
        )
        total_commits -= commits_diff
    else:
        latest_timestamp = commits[0]["commit"]["author"]["date"]
        latest_timestamp = analysis_helpers.parse_timestamp(latest_timestamp)

    difference = latest_timestamp - first_timestamp
    total_hours = difference / timedelta(hours=1)
    return total_hours / total_commits


async def get_code_churn(repo_url: str) -> dict:
    """Calculates the number of additions, deletions, the total of both,
        and the net additions. Omits merge commits and empty commits.

    Args:
        repo_url (str): The URL of the repository in the format
                        https://github.com/owner/repo

    Returns:
        dict: A dictionary with the keys "additions", "deletions",
              "total" (sum), and "net" (difference).

    Raises:
        GitHubAPIError: If the request to GitHub failed.
        GitHubTimeOutError: If GitHub didn't calculate the metric in time.
        RepoTooLargeError: If the repository has 10,000 commits or more.
    """
    contributor_history = await github_client.get_contributor_history(repo_url)

    additions = 0
    deletions = 0
    commits = 0

    for contributor in contributor_history:
        weeks = contributor["weeks"]
        for week in weeks:
            additions += week["a"]
            deletions += week["d"]
            commits += week["c"]

    total = additions + deletions
    net = additions - deletions

    # the contributors endpoint still returns status 200 even if the repo is too large
    if commits >= 10000:
        raise RepoTooLargeError()

    return {"additions": additions, "deletions": deletions, "total": total, "net": net}


async def get_issues_close_time(
    repo_url: str, time_from: datetime = None, time_until: datetime = None
) -> float:
    """Calculates the average number of hours for an issue to be closed.

    Args:
        repo_url (str): The URL of the repository in the format
                        https://github.com/owner/repo
        time_from (datetime): The time to start looking from.
        time_until (datetime): The time to start looking until.

    Returns:
        float: The average number of hours for an issue to be closed.

    Raises:
         GitHubAPIError: If the request to GitHub failed.
         InsufficientIssuesError: If the repository has no closed issues.
    """
    issues = await github_client.get_issues(repo_url)
    if len(issues) == 0:
        raise InsufficientIssuesError()

    if time_from or time_until:
        # need to sort by "closed_at" before trimming, issues are sorted by "created_at"
        issues = sorted(issues, key=lambda _: _["closed_at"], reverse=True)
        keys = ["closed_at"]

        if time_from:
            # fyi: GitHub's API can't filter by "closed_at", nor can it filter "up to"
            issues = analysis_helpers.trim_prior_entries(time_from, issues, keys)
        if time_until:
            issues = analysis_helpers.trim_leading_entries(time_until, issues, keys)

    total_time = 0
    for issue in issues:
        created_at = issue["created_at"].replace("Z", "+00:00")
        created_at = datetime.fromisoformat(created_at)

        closed_at = issue["closed_at"].replace("Z", "+00:00")
        closed_at = datetime.fromisoformat(closed_at)

        difference = closed_at - created_at
        total_hours = difference / timedelta(hours=1)
        total_time += total_hours

    return total_time / len(issues)


async def get_pulls_close_time(
    repo_url: str, time_from: datetime = None, time_until: datetime = None
) -> float:
    """Calculates the average number of hours for a pull request to be merged or closed.

    Args:
        repo_url (str): The URL of the repository in the format
                        https://github.com/owner/repo
        time_from (datetime): The time to start looking from.
        time_until (datetime): The time to start looking until.

    Returns:
        float: The average number of hours for a pull request to be merged or closed.

    Raises:
        GitHubAPIError: If the request to GitHub failed.
        InsufficientPullsError: If there are no closed or merged pull requests.
    """
    pulls = await github_client.get_pulls(repo_url)
    if len(pulls) == 0:
        raise InsufficientPullsError()

    if time_from or time_until:
        # need to sort by "closed_at" before trimming, pulls are sorted by "created_at"
        pulls = sorted(pulls, key=lambda _: _["closed_at"], reverse=True)
        keys = ["closed_at"]
        if time_from:
            pulls = analysis_helpers.trim_prior_entries(time_from, pulls, keys)
        if time_until:
            pulls = analysis_helpers.trim_leading_entries(time_until, pulls, keys)

    total_time = 0
    for pull in pulls:
        created_at = pull["created_at"].replace("Z", "+00:00")
        created_at = datetime.fromisoformat(created_at)

        closed_at = pull["closed_at"].replace("Z", "+00:00")
        closed_at = datetime.fromisoformat(closed_at)

        difference = closed_at - created_at
        total_hours = difference / timedelta(hours=1)
        total_time += total_hours

    return total_time / len(pulls)


async def get_last_updated(repo_url: str) -> datetime:
    """Rudimentary function that checks the last time a repo was updated."""
    commits = await github_client.get_commits(repo_url)
    latest_commit = commits[0]
    latest_timestamp = latest_commit["commit"]["author"]["date"]
    return analysis_helpers.parse_timestamp(latest_timestamp)


async def create_report(repo_url: str) -> dict:
    """Calls all analysis functions and formats results into a dict report."""
    raw_report = await asyncio.gather(
        get_commit_frequency(repo_url),
        get_code_churn(repo_url),
        get_issues_close_time(repo_url),
        get_pulls_close_time(repo_url),
        return_exceptions=True,
    )

    parsed_metrics = []
    for raw_metric in raw_report:
        if isinstance(raw_metric, Exception):
            parsed_metric = {
                "status_code": raw_metric.status_code,
                "data": None,
                "error_name": type(raw_metric).__name__,
                "error_message:": raw_metric.error_message,
            }
        else:
            parsed_metric = {
                "status_code": 200,
                "data": raw_metric,
                "error_name": None,
                "error_message": None,
            }
        parsed_metrics.append(parsed_metric)

    parsed_report = {
        "commit_frequency": parsed_metrics[0],
        "code_churn": parsed_metrics[1],
        "issues_close_time": parsed_metrics[2],
        "pulls_close_time": parsed_metrics[3],
    }

    return parsed_report
