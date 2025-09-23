import re
import os
import httpx
import logging

from urllib.parse import urlencode
from dotenv import load_dotenv
from backend.exceptions import GitHubAPIError, CommitInfoError

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def parse_data(data: list[dict] | dict | None) -> list[dict]:
    """Converts the data received from the GitHub API into a list[dict]

    Args:
        data (list[dict] | dict | None): The data obtained from GitHub API.

    Returns:
        list[dict]: The data as a list of dictionaries.
    """
    if isinstance(data, list):
        return data

    if type(data) is None:
        return []

    del data["incomplete_results"]
    del data["repository_selection"]
    del data["total_count"]

    namespace_key = data.keys()[0]
    data = data[namespace_key]

    return data


async def get_paginated_data(
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
    query_string = urlencode(params)
    url = f"{url}?{query_string}"

    headers = {
        "User-Agent": "Gitsy/0.1",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {GITHUB_TOKEN}",
    }
    if extra_headers is not None:
        headers = headers | extra_headers

    while pages_remaining:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
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


async def get_commits(repo_url: str) -> list[dict]:
    """Obtains the commits of a public repository

    Args:
        repo_url (str): The URL in the format https://github.com/user/repo.

    Returns:
        list[dict]: A list with a dictionary for each commit.
    """
    commits = []
    url = f"{parse_url(repo_url)}/commits"

    try:
        commits = await get_paginated_data(url)
    except GitHubAPIError as e:
        print(e)
    except Exception as e:
        logging.exception(f"Something unexpected went wrong: {e}")

    return commits


async def get_issues(repo_url: str, state: str = "closed") -> list[dict]:
    """Obtains all issues of a repository.

    Args:
        repo_url (str): The repository URL in the format https://github.com/user/repo
        state (str): The desired state of the issue, "open", "closed", "all".
            Default is "closed".

    Returns:
        list[dict]: A list of dictionaries, with a dictionary for each issue.
    """
    issues = []
    url = f"{parse_url(repo_url)}/issues"

    try:
        issues = await get_paginated_data(url, extra_params={"state": f"{state}"})
    except GitHubAPIError as e:
        print(e)
    except Exception as e:
        logging.exception(f"Something unexpected went wrong: {e}")

    return issues


async def get_pulls(repo_url: str, state: str = "closed") -> list[dict]:
    """Obtains all pull requests of a repository.

    Args:
        repo_url (str): The repository URL in the format https://github.com/user/repo
        state (str): The desired state of the pull request, "open", "closed", "all".
            Default is "closed".

    Returns:
        list[dict]: A list of dictionaries, with a dictionary for each pull request.
    """
    pulls = []
    url = f"{parse_url(repo_url)}/pulls"

    try:
        pulls = await get_paginated_data(url, extra_params={"state": f"{state}"})
    except GitHubAPIError as e:
        print(e)
    except Exception as e:
        logging.exception(f"Something unexpected went wrong: {e}")

    return pulls


async def get_commit_info(repo_url: str, sha: str) -> dict:
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
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{url}/{sha}", headers=headers)
    if response.status_code != 200:
        raise CommitInfoError(
            f"Failed to obtain commit info. Error code {response.status_code}"
        )

    return response.json()


# print(len(asyncio.run(get_commits("https://github.com/matslyk0/Gitsy"))))
