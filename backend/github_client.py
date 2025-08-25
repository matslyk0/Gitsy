import re
import os
import json
import requests
from dotenv import load_dotenv
from backend.exceptions import *

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def parse_data(data: list[dict] | dict | None) -> list[dict]:
    """Converts the data received from the GitHub API into a list[dict]

    Args:
        data (list[dict] | dict | None): The data obtained when making a GitHub API GET request.

    Returns:
        list[dict]: The data as a list of dictionaries.
    """
    if isinstance(data, list):
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


def get_paginated_data(
    url: str, extra_params: dict = None, extra_headers: dict = None
) -> list[dict]:
    """Makes a GET request to all pages at the endpoint.

    Args:
        url (str): The URL of the endpoint.
        extra_params (dict): Additional parameters to be passed to the GET request.
        extra_headers (dict): Additional headers to be passed to the GET request.

    Returns:
        list[dict]: The data as a list of dictionaries.

    Raises:
        GitHubAPIError: If the API returns a non-200 status code.
    """
    pages_remaining = True
    data = []

    params = {"per_page": 30}
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
            raise GitHubAPIError(
                f"Failed to obtain data. Error code {response.status_code}"
            )

        parsed_data = parse_data(response.json())
        data += parsed_data

        if "link" not in response.headers:
            break

        link_header = response.headers["link"]
        pages_remaining = 'rel="next"' in link_header

        if pages_remaining:
            match = re.search(r'(?<=<)(\S*)(?=>; rel="next")', link_header)
            url = match.group(1)

    return data


def parse_url(repo_url: str):
    """Parses a repository URL into the GitHub API format"""
    url = repo_url.removeprefix("https://github.com/")
    return f"https://api.github.com/repos/{url}"


def get_commits(repo_url: str) -> list[dict]:
    """Obtains the commits of a public repository

    Args:
        repo_url (str): The URL in the format https://github.com/user/repo.

    Returns:
        list[dict]: A list with a dictionary for each commit.
    """
    commits = []
    url = f"{parse_url(repo_url)}/commits"

    try:
        commits = get_paginated_data(url)
    except GitHubAPIError as e:
        print(e)
    except Exception as e:
        logging.exception(f"Something unexpected went wrong: {e}")

    return commits


def get_issues(repo_url: str, state: str = "open") -> list[dict]:
    """Obtains all issues of a repository.

    Args:
        repo_url (str): The repository URL in the format https://github.com/user/repo
        state (str): The desired state of the issue, "open", "closed", "all". Default "open".

    Returns:
        list[dict]: A list of dictionaries, with a dictionary for each issue.
    """
    issues = []
    url = f"{parse_url(repo_url)}/issues"

    try:
        issues = get_paginated_data(url, extra_params={"state": f"{state}"})
    except GitHubAPIError as e:
        print(e)
    except Exception as e:
        logging.exception(f"Something unexpected went wrong: {e}")

    return issues


def get_pulls(repo_url: str, state: str = "open") -> list[dict]:
    """Obtains all pull requests of a repository.

    Args:
        repo_url (str): The repository URL in the format https://github.com/user/repo
        state (str): The desired state of the pull request, "open", "closed", "all". Default "open".

    Returns:
        list[dict]: A list of dictionaries, with a dictionary for each pull request.
    """
    pulls = []
    url = f"{parse_url(repo_url)}/pulls"

    try:
        pulls = get_paginated_data(url, extra_params={"state": f"{state}"})
    except GitHubAPIError as e:
        print(e)
    except Exception as e:
        logging.exception(f"Something unexpected went wrong: {e}")

    return pulls


def get_commit_info(repo_url: str, sha: str) -> dict:
    """Obtains detailed information about a commit.

    Args:
        repo_url (str): The URL in the format https://github.com/user/repo
        sha (str): The SHA of the commit.

    Returns:
        dict: A dictionary containing the information about the commit.
    """
    url = f"{parse_url(repo_url)}/commits"
    headers = {
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {GITHUB_TOKEN}",
    }

    response = requests.get(f"{url}/{sha}", headers=headers)
    if response.status_code != 200:
        raise CommitInfoError(f"Failed to obtain commit info. Error code {response.status_code}")

    return response.json()