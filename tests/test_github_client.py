import pytest
import asyncio
import backend.github_client as github_client

from backend.exceptions import GitHubAPIError

# ------------------------------------- Unit Tests -------------------------------------


def test_parse_data_listdict() -> None:
    data = [{"key": "success"}]
    result = github_client.parse_data(data)
    assert result == [{"key": "success"}]


def test_parse_data_dict() -> None:
    data = {
        "incomplete_results": 0,
        "repository_selection": "something",
        "total_count": 100,
        "desired_data": [{"key": "success"}],
    }
    result = github_client.parse_data(data)
    assert result == [{"key": "success"}]


def test_parse_data_empty() -> None:
    data = None
    result = github_client.parse_data(data)
    assert result == []


def test_parse_url_without_target() -> None:
    repo_url = "https://github.com/matslyk0/Gitsy"
    result = github_client.parse_url(repo_url)
    assert result == "https://api.github.com/repos/matslyk0/Gitsy"


def test_parse_url_with_target() -> None:
    repo_url = "https://github.com/matslyk0/Gitsy"
    result = github_client.parse_url(repo_url, "commits")
    assert result == "https://api.github.com/repos/matslyk0/Gitsy/commits"


def test_get_owner_and_response() -> None:
    repo_url = "https://github.com/matslyk0/Gitsy"
    result = github_client.get_owner_and_reponame(repo_url)
    assert result == ("matslyk0", "Gitsy")


# --------------------------------- Integration Tests ---------------------------------


def test_get_paginated_data() -> None:
    url = "https://api.github.com/repos/matslyk0/Gitsy/commits"
    result = asyncio.run(github_client.get_paginated_data(url))
    assert result is not None


def test_get_paginated_data_fail():
    url = "https://api.github.com/repos/matslyk0/Gitsy/nonexistent"
    with pytest.raises(GitHubAPIError):
        asyncio.run(github_client.get_paginated_data(url))


def test_get_commits() -> None:
    repo_url = "https://github.com/matslyk0/Gitsy"
    commits = asyncio.run(github_client.get_commits(repo_url))
    assert commits


def test_get_commit_info() -> None:
    sha = "42e3978c91d90c51c1a7a0e154bd92fe5021783f"
    repo_url = "https://github.com/matslyk0/Gitsy"
    commit = asyncio.run(github_client.get_commit_info(repo_url, sha))
    assert commit


def test_get_issues() -> None:
    repo_url = "https://github.com/matslyk0/Gitsy"
    issues = asyncio.run(github_client.get_issues(repo_url))
    assert issues


def test_get_pulls() -> None:
    repo_url = "https://github.com/matslyk0/Gitsy"
    pulls = asyncio.run(github_client.get_pulls(repo_url))
    assert pulls
