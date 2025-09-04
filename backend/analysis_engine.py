import json
import httpx
import asyncio
import backend.github_client as github_client
import backend.analysis_helpers as analysis_helpers

from zoneinfo import ZoneInfo
from datetime import datetime, timedelta


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
         InsufficientDataError: If the repository has less than 2 commits.
    """
    commits = await github_client.get_commits(repo_url)

    if len(commits) < 2:
        raise InsufficientDataError("Not enough data to perform calculation.")

    if time_from:
        keys = ["commit", "author", "date"]
        first_timestamp = analysis_helpers.get_first_timestamp(time_from, commits, keys)
    else:
        first_timestamp = commits[-1]["commit"]["author"]["date"]
        first_timestamp = analysis_helpers.parse_timestamp(first_timestamp)

    if time_until:
        keys = ["commit", "author", "date"]
        latest_timestamp = analysis_helpers.get_latest_timestamp(time_until, commits, keys)
    else:
        latest_timestamp = commits[0]["commit"]["author"]["date"]
        latest_timestamp = analysis_helpers.parse_timestamp(latest_timestamp)

    difference = latest_timestamp - first_timestamp
    total_hours = difference / timedelta(hours=1)
    return total_hours / len(commits)


async def get_code_churn(
    repo_url: str, time_from: datetime = None, time_until: datetime = None
) -> dict:
    """Calculates the number of additions, deletions, the total of both, and the net additions.

    Args:
        repo_url (str): The URL of the repository in the format
                        https://github.com/owner/repo
        time_from (datetime): The time to start looking from.
        time_until (datetime): The time to start looking until.

    Returns:
        dict: A dictionary with the keys "additions", "deletions",
              "total" (sum), and "net" (difference).

    Raises:
         InsufficientDataError: If the repository has no commits.
    """
    commits = await github_client.get_commits(repo_url)
    if len(commits) == 0:
        raise InsufficientDataError("Not enough data to perform calculation.")

    total = 0
    additions = 0
    deletions = 0

    keys = ["commit", "author", "date"]
    if time_from:
        commits = analysis_helpers.trim_prior_entries(time_from, commits, keys)
    if time_until:
        commits = analysis_helpers.trim_leading_entries(time_until, commits, keys)

    for commit in commits:
        sha = commit["sha"]
        commit_info = github_client.get_commit_info(repo_url, sha)
        stats = commit_info["stats"]

        total += stats["total"]
        additions += stats["additions"]
        deletions += stats["deletions"]

    net = additions - deletions

    return {"additions": additions, "deletions": deletions, "total": total, "net": net}


async def get_issue_times(
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
         InsufficientDataError: If the repository has no closed issues.
    """
    issues = await github_client.get_issues(repo_url)
    if len(issues) == 0:
        raise InsufficientDataError("Not enough data to perform calculation.")

    total_time = 0

    if time_from:
        issues = analysis_helpers.trim_prior_entries(time_from, issues, ["created_at"])
    if time_until:
        issues = analysis_helpers.trim_leading_entries(time_until, issues, ["closed_at"])

    for issue in issues:
        created_at = issue["created_at"].replace("Z", "+00:00")
        created_at = datetime.fromisoformat(created_at)

        closed_at = issue["closed_at"].replace("Z", "+00:00")
        closed_at = datetime.fromisoformat(closed_at)

        difference = closed_at - created_at
        total_hours = difference / timedelta(hours=1)
        total_time += total_hours

    return total_time / len(issues)


async def get_pull_times(
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
         InsufficientDataError: If there are no closed or merged pull requests.
    """
    pulls = await github_client.get_pulls(repo_url)
    if len(pulls) == 0:
        raise InsufficientDataError("Not enough data to perform calculation.")

    total_time = 0

    if time_from:
        pulls = analysis_helpers.trim_prior_entries(time_from, pulls, ["created_at"])
    if time_until:
        pulls = analysis_helpers.trim_leading_entries(time_until, pulls, ["closed_at"])

    for pull in pulls:
        created_at = pull["created_at"].replace("Z", "+00:00")
        created_at = datetime.fromisoformat(created_at)

        closed_at = pull["closed_at"].replace("Z", "+00:00")
        closed_at = datetime.fromisoformat(closed_at)

        difference = closed_at - created_at
        total_hours = difference / timedelta(hours=1)
        total_time += total_hours

    return total_time / len(pulls)


timestamp = datetime.strptime("2025-08-04 23:59", "%Y-%m-%d %H:%M")
timestamp = timestamp.replace(tzinfo=ZoneInfo("UTC"))
result = asyncio.run(get_pull_times("https://github.com/matslyk0/Gitsy", time_until=timestamp))
print(result)
"""

result = asyncio.run(github_client.get_pulls("https://github.com/matslyk0/Gitsy", state="closed"))
print(json.dumps(result, indent=4))
"""
