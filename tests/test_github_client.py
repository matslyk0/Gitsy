import pytest
import asyncio
import backend.github_client as github_client
from backend.exceptions import GitHubAPIError


def test_get_paginated_data() -> None:  # Integration Test
    url = "https://api.github.com/repos/matslyk0/Gitsy/commits"
    result = asyncio.run(github_client.get_paginated_data(url))
    assert result is not None


def test_get_paginated_data_fail() -> None:  # Integration Test
    url = "https://api.github.com/repos/matslyk0/Gitsy/nonexistent"
    with pytest.raises(GitHubAPIError):
        asyncio.run(github_client.get_paginated_data(url))


def test_get_commits() -> None:  # Integration Test
    repo_url = "https://github.com/matslyk0/Gitsy"
    commits = asyncio.run(github_client.get_commits(repo_url))
    assert commits


def test_get_issues() -> None:  # Integration Test
    repo_url = "https://github.com/matslyk0/Gitsy"
    issues = asyncio.run(github_client.get_issues(repo_url))
    assert issues


def test_get_pulls() -> None:  # Integration Test
    repo_url = "https://github.com/matslyk0/Gitsy"
    pulls = asyncio.run(github_client.get_pulls(repo_url))
    assert pulls


def test_get_contributor_history() -> None:  # Integration Test
    repo_url = "https://github.com/matslyk0/Gitsy"
    contributor_history = asyncio.run(github_client.get_contributor_history(repo_url))
    assert contributor_history
