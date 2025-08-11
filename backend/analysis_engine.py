import requests
import json
import re
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta


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


def get_paginated_data(url: str) -> dict:
    pages_remaining = True
    data = []
    params = {"per_page": 30}
    headers = {
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {GITHUB_TOKEN}",
    }
    success = True

    while pages_remaining:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            parsed_data = parse_data(response.json())
            data += parsed_data
        else:
            success = False
            break

        # for scenarios where there is only one page of results
        if "link" not in response.headers:
            break

        link_header = response.headers["link"]
        pages_remaining = link_header and 'rel="next"' in link_header

        if pages_remaining:
            match = re.search(r'(?<=<)(\S*)(?=>; rel="next")', link_header)
            url = match.group(1)

    return {"data": data, "success": success}


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

    info = repo_url.removeprefix("https://github.com/")
    url = f"https://api.github.com/repos/{info}/commits"

    return get_paginated_data(url)


def get_commit_frequency(repo_url: str, include_initial: bool = True) -> float:
    """
    Calculates the average hours per commit of a repository.

    Args:
        repo_url: string in the format https://github.com/owner/repo
        include_initial: flag to include the initial commit of a repository, default = True

    Returns:
        float: the hours per commit, -1.0 if there is no feasible calculation
    """

    commits_request = get_commits(repo_url)
    commits = commits_request["data"]

    if not commits_request["success"]:
        return -1.0

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


hours_between_commits = get_commit_frequency("https://github.com/dyad-sh/dyad")
print("dyad has a commit every %.2f hours!" % hours_between_commits)

"""
output = get_commits("https://github.com/matslyk0/Gitsy")
if output[1]:
    print(json.dumps(output, indent=4))
"""