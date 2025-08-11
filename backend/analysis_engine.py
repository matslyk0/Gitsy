import logging
import requests
import json
import re
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from exceptions import GithubAPIError


load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def parse_data(data) -> list[dict]:
    if type(data) is list:
        return data

    if type(data) is None:
        return []

    print(data)

    del data["incomplete_results"]
    del data["repository_selection"]
    del data["total_count"]

    namespace_key = data.keys()[0]
    data = data[namespace_key]

    return data


def get_paginated_data(url: str, extra_params: dict = None, extra_headers: dict = None) -> dict:
    pages_remaining = True
    data = []

    params = {"per_page": 100}
    if extra_params is not None:
        params = params | extra_params

    headers = {
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {GITHUB_TOKEN}",
    }
    if extra_headers is not None:
        headers = headers | extra_headers

    while pages_remaining:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code != 200:
            raise GithubAPIError(
                f"Failed to obtain data. Error code {response.status_code}"
            )

        parsed_data = parse_data(response.json())
        data += parsed_data

        # for scenarios where there is only one page of results
        if "link" not in response.headers:
            break

        # gets link, checks existence and checks if it is a 'next' link
        link_header = response.headers["link"]
        pages_remaining = link_header and 'rel="next"' in link_header

        if pages_remaining:
            match = re.search(r'(?<=<)(\S*)(?=>; rel="next")', link_header)
            url = match.group(1)

    return data


def get_commits(repo_url: str) -> dict:
    """
    Obtains the commits of a public repository

    Args:
        repo_url (str): string in the format https://github.com/user/repo

    Returns:
        dict: ("data":, "success":)
               -> first element is the list of commits;
               -> second element determines the validity of the result.
    """

    url = repo_url.removeprefix("https://github.com/")
    url = f"https://api.github.com/repos/{url}/commits"

    return get_paginated_data(url)


def get_issues(repo_url: str) -> dict:
    url = repo_url.removeprefix("https://github.com/")
    url = f"https://api.github.com/repos/{url}/issues"

    return get_paginated_data(url, extra_params={"state": "all"})


def get_commit_frequency(repo_url: str, include_initial: bool = True) -> float:
    """
    Calculates the average hours per commit of a repository.

    Args:
        repo_url: string in the format https://github.com/owner/repo
        include_initial: flag to include the initial commit of a repository, default = True

    Returns:
        float: the hours per commit, -1.0 if there is no feasible calculation
    """

    commits = get_commits(repo_url)

    if not include_initial:
        commits.pop(-1)

    total_commits = len(commits)
    if total_commits < 2:
        return -1.0

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
    total = 0
    additions = 0
    deletions = 0

    commits = get_commits(repo_url)
    url = repo_url.removeprefix("https://github.com/")
    url = f"https://api.github.com/repos/{url}/commits"

    headers = {
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {GITHUB_TOKEN}",
    }

    for commit in commits:
        sha = commit["sha"]
        response = requests.get(f"{url}/{sha}", headers=headers)
        stats = response.json()["stats"]

        total += stats["total"]
        additions += stats["additions"]
        deletions += stats["deletions"]

    net = additions - deletions

    return {"additions": additions, "deletions": deletions, "total": total, "net": net}


def get_issue_times(repo_url: str) -> float:
    issues = get_issues(repo_url)
    total_time = 0

    for issue in issues:
        if issue["closed_at"] is not None:
            created_at = issue["created_at"].replace("Z", "+00:00")
            created_at = datetime.fromisoformat(created_at)

            closed_at = issue["closed_at"].replace("Z", "+00:00")
            closed_at = datetime.fromisoformat(closed_at)

            difference = closed_at - created_at
            total_hours = difference / timedelta(hours=1)
            total_time += total_hours

    if total_time == 0:
        return -1.0

    return total_time / len(issues)


def test_commits(repo_url: str) -> None:
    try:
        commits = get_commits(repo_url)
        print(json.dumps(commits, indent=4))
    except GithubAPIError as e:
        print(e)
    except Exception as e:
        logging.exception(f"Something went wrong: {e}")


def test_commit_frequency(repo_url: str) -> None:
    user_and_repo = repo_url.removeprefix("https://github.com/")
    user, separator, repo = user_and_repo.partition("/")
    try:
        hours_between_commits = get_commit_frequency(repo_url)
        print(
            f"{repo} has a commit every {hours_between_commits:.2f} hours!"
        )
    except GithubAPIError as e:
        print(e)
    except Exception as e:
        logging.exception(f"Something went wrong: {e}")


def test_code_churn(repo_url: str) -> None:
    try:
        print(get_code_churn(repo_url))
    except GithubAPIError as e:
        print(e)
    except Exception as e:
        logging.exception(f"Something went wrong: {e}")


def test_issue_times(repo_url: str) -> None:
    user_and_repo = repo_url.removeprefix("https://github.com/")
    user, separator, repo = user_and_repo.partition("/")
    try:
        issue_close_time = get_issue_times(repo_url)
        print(f"{repo} closes an issue every {issue_close_time:.2f} hours!")
    except GithubAPIError as e:
        print(e)
    except Exception as e:
        logging.exception(f"Something went wrong: {e}")


# test_commit_frequency("https://github.com/matslyk0/Gitsy")
# test_commits("https://github.com/matslyk0/Gitsy")
# test_code_churn("https://github.com/dyad-sh/dyad")
test_issue_times("https://github.com/matslyk0/Gitsy")
