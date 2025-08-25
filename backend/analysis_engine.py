import backend.github_client as github_client
from datetime import datetime, timedelta


def get_commit_frequency(repo_url: str) -> float:
    """Calculates the average number of hours between commits for a repository.

    Args:
        repo_url (str): The URL of the repository in the format
                        https://github.com/owner/repo

    Returns:
        float: The average number of hours between commits.

    Raises:
         InsufficientDataError: If the repository has less than 2 commits.
    """

    commits = []

    try:
        commits = github_client.get_commits(repo_url)
    except GitHubAPIError as e:
        print(e)
    except Exception as e:
        logging.exception(f"Something unexpected went wrong: {e}")

    total_commits = len(commits)
    if total_commits < 2:
        raise InsufficientDataError("Not enough data to perform calculation.")

    first_commit = commits[-1]
    first_timestamp = first_commit["commit"]["author"]["date"].replace("Z", "+00:00")
    first_timestamp = datetime.fromisoformat(first_timestamp)

    recent_commit = commits[0]
    recent_timestamp = recent_commit["commit"]["author"]["date"].replace("Z", "+00:00")
    recent_timestamp = datetime.fromisoformat(recent_timestamp)

    difference = recent_timestamp - first_timestamp
    total_hours = difference / timedelta(hours=1)
    return total_hours / total_commits


def get_code_churn(repo_url: str) -> dict:
    """Calculates the number of additions, deletions, the total of both, and the net additions.

    Args:
        repo_url (str): The URL of the repository in the format
                        https://github.com/owner/repo

    Returns:
        dict: A dictionary with the keys "additions", "deletions",
              "total" (sum), and "net" (difference).
    """
    total = 0
    additions = 0
    deletions = 0
    commits = github_client.get_commits(repo_url)

    for commit in commits:
        sha = commit["sha"]
        commit_info = github_client.get_commit_info(repo_url, sha)
        stats = commit_info["stats"]

        total += stats["total"]
        additions += stats["additions"]
        deletions += stats["deletions"]

    net = additions - deletions

    return {"additions": additions, "deletions": deletions, "total": total, "net": net}


def get_issue_times(repo_url: str) -> float:
    """Calculates the average number of hours for an issue to be closed.

    Args:
        repo_url (str): The URL of the repository in the format
                        https://github.com/owner/repo

    Returns:
        float: The average number of hours for an issue to be closed.

    Raises:
         InsufficientDataError: If the repository has no closed issues.
    """
    issues = github_client.get_issues(repo_url, state="closed")
    if len(issues) == 0:
        raise InsufficientDataError("Not enough data to perform calculation.")

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


def get_pull_times(repo_url: str) -> float:
    """Calculates the average number of hours for a pull request to be merged or closed.

    Args:
        repo_url (str): The URL of the repository in the format
                        https://github.com/owner/repo

    Returns:
        float: The average number of hours for a pull request to be merged or closed.

    Raises:
         InsufficientDataError: If there are no closed or merged pull requests.
    """
    pulls = github_client.get_pulls(repo_url, state="closed")
    if len(pulls) == 0:
        raise InsufficientDataError("Not enough data to perform calculation.")

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


# "https://github.com/matslyk0/Gitsy"
# "https://github.com/dyad-sh/dyad"

# print(get_commit_frequency("https://github.com/matslyk0/Gitsy"))
# print(get_code_churn("https://github.com/matslyk0/Gitsy"))
# print(get_issue_times("https://github.com/matslyk0/Gitsy"))
# print(get_pull_times("https://github.com/matslyk0/Gitsy"))

