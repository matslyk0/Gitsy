import requests, json

def get_repo_commits(repo_url: str):
    """
    Obtains the commits of a public repository

    Args:
        repo_url (str): string in the format https://github.com/{user}/{repo}

    Returns:
        list, dict: a .json of the commits
        str: an error message if obtaining info failed
    """

    info = repo_url.removeprefix("https://github.com/")
    url = f"https://api.github.com/repos/{info}/commits"

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error in retrieving data. Status code {response.status_code}"

def get_user_repos(user_url: str):
    """
    Obtains the public repositories of a user

    Args:
        user_url: string in the format https://github.com/{owner}

    Returns:
        list, dict: a .json of the commits
        str: an error message if obtaining info failed
    """

    info = user_url.removeprefix("https://github.com/")
    url = f"https://api.github.com/users/{info}/repos"

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error in retrieving data. Status code {response.status_code}"

output = get_repo_commits("https://github.com/matslyk0/Gitsy")
if not isinstance(output, str):
    print(json.dumps(output, indent=4))
#print(get_user_repos("matslyk0"))