import re
import os
import time
import httpx
import asyncio
import backend.helpers as helpers

from urllib.parse import urlencode
from backend.exceptions import GitHubAPIError, GitHubTimeOutError

# for script-only testing
# from dotenv import load_dotenv
# load_dotenv()
# import asyncio
# import json

# loaded in docker compose - dev/test: from .env, CI/prod: from GitHub Secrets
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

semaphore = asyncio.Semaphore(4)


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
        GitHubAPIError: If the request to GitHub failed.
    """
    pages_remaining = True
    data = []

    params = {"per_page": 100}
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
        async with semaphore:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(url, headers=headers)
        if response.status_code != 200:
            raise GitHubAPIError()

        parsed_data = helpers.parse_data(response.json())
        data += parsed_data
        if "link" not in response.headers:
            break

        link_header = response.headers["link"]
        pages_remaining = 'rel="next"' in link_header

        if pages_remaining:
            match = re.search(r'(?<=<)(\S*)(?=>; rel="next")', link_header)
            url = match.group(1)

    return data


async def get_commits(repo_url: str) -> list[dict]:
    """Obtains the commits of a public repository

    Args:
        repo_url (str): The URL in the format https://github.com/user/repo.

    Returns:
        list[dict]: A list with a dictionary for each commit.

    Raises:
        GitHubAPIError: If the request to GitHub failed.
    """
    commits = []
    url = helpers.parse_url(repo_url, "commits")

    commits = await get_paginated_data(url)

    return commits


async def get_issues(
    repo_url: str, state: str = "closed", sort: str = "created"
) -> list[dict]:
    """Obtains all issues of a repository.

    Args:
        repo_url (str): The repository URL in the format https://github.com/user/repo
        state (str): The state of issues: "open", "closed", "all". Default is "closed".
        sort (str): The sorting of issues: "created", "updated", "comments". Default is
            "created".

    Returns:
        list[dict]: A list of dictionaries, with a dictionary for each issue.

    Raises:
        GitHubAPIError: If the request to GitHub failed.
    """
    issues = []
    url = helpers.parse_url(repo_url, "issues")

    issues = await get_paginated_data(url, extra_params={"state": state, "sort": sort})

    return issues


async def get_pulls(
    repo_url: str, state: str = "closed", sort: str = "created"
) -> list[dict]:
    """Obtains all pull requests of a repository.

    Args:
        repo_url (str): The repository URL in the format https://github.com/user/repo
        state (str): The state of PRs, "open", "closed", "all". Default is "closed".
        sort (str): The sorting of PRs: "created", "updated", "popularity",
            "long-running". Default is "created".

    Returns:
        list[dict]: A list of dictionaries, with a dictionary for each pull request.

    Raises:
        GitHubAPIError: If the request to GitHub failed.
    """
    pulls = []
    url = helpers.parse_url(repo_url, "pulls")

    pulls = await get_paginated_data(url, extra_params={"state": state, "sort": sort})

    return pulls


async def get_contributor_history(repo_url: str) -> list[dict]:
    """Obtains a repository's full contributor history.

    Args:
        repo_url (str): The URL in the format https://github.com/user/repo

    Returns:
        list[dict]: A list of dictionaries for each contributor.

    Raises:
        GitHubTimeOutError: If GitHub didn't calculate the metric in time.
        GitHubAPIError: If the request to GitHub failed.
    """
    headers = {
        "User-Agent": "Gitsy/0.1",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {GITHUB_TOKEN}",
    }
    url = helpers.parse_url(repo_url, "stats/contributors")

    # wait 5s, 10s, 20s, ... , 160s before giving up - total 315s for GitHub to finish
    count = 1
    while count <= 32:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)

        if response.status_code == 202:
            time.sleep(count * 5)
            count *= 2
        else:
            break

    match response.status_code:
        case 200:
            return response.json()
        case 202:
            raise GitHubTimeOutError()
        case _:
            raise GitHubAPIError()
