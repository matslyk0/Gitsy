import backend.github_client as github_client


def test_get_commits():
    commits = []

    try:
        commits = github_client.get_commits("https://github.com/matslyk0/Gitsy")
    except GitHubAPIError as e:
        print(e)
    except Exception as e:
        logging.exception(f"Something unexpected went wrong: {e}")

    assert commits

def test_get_commit_info():
    commit = []
    sha = "42e3978c91d90c51c1a7a0e154bd92fe5021783f"

    try:
        commit = github_client.get_commit_info("https://github.com/matslyk0/Gitsy", sha)
    except GitHubAPIError as e:
        print(e)
    except Exception as e:
        logging.exception(f"Something unexpected went wrong: {e}")

    assert commit

def test_get_issues():
    issues = []

    try:
        issues = github_client.get_issues("https://github.com/matslyk0/Gitsy")
    except GitHubAPIError as e:
        print(e)
    except Exception as e:
        logging.exception(f"Something unexpected went wrong: {e}")

    assert issues

def test_get_pulls():
    pulls = []

    try:
        pulls = github_client.get_pulls("https://github.com/matslyk0/Gitsy", state="closed")
    except GitHubAPIError as e:
        print(e)
    except Exception as e:
        logging.exception(f"Something unexpected went wrong: {e}")

    assert pulls