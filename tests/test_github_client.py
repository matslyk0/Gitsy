import backend.github_client as github_client


def test_get_commits():
    commits = github_client.get_commits("https://github.com/matslyk0/Gitsy")
    assert commits

def test_get_commit_info():
    sha = "42e3978c91d90c51c1a7a0e154bd92fe5021783f"
    commit = github_client.get_commit_info("https://github.com/matslyk0/Gitsy", sha)
    assert commit

def test_get_issues():
    issues = github_client.get_issues("https://github.com/matslyk0/Gitsy")
    assert issues

def test_get_pulls():
    pulls = github_client.get_pulls("https://github.com/matslyk0/Gitsy", state="closed")
    assert pulls