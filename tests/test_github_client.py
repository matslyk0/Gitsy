import asyncio
import backend.github_client as github_client


def test_get_commits():
    repo_url = "https://github.com/matslyk0/Gitsy"
    commits = asyncio.run(github_client.get_commits(repo_url))
    assert commits


def test_get_commit_info():
    sha = "42e3978c91d90c51c1a7a0e154bd92fe5021783f"
    repo_url = "https://github.com/matslyk0/Gitsy"
    commit = asyncio.run(github_client.get_commit_info(repo_url, sha))
    assert commit


def test_get_issues():
    repo_url = "https://github.com/matslyk0/Gitsy"
    issues = asyncio.run(github_client.get_issues(repo_url))
    assert issues


def test_get_pulls():
    repo_url = "https://github.com/matslyk0/Gitsy"
    pulls = asyncio.run(github_client.get_pulls(repo_url, state="closed"))
    assert pulls
