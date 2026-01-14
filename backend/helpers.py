def parse_data(data: list[dict] | dict | None) -> list[dict]:
    """Converts the data received from the GitHub API into a list[dict]

    Args:
        data (list[dict] | dict | None): The data obtained from GitHub API.

    Returns:
        list[dict]: The data as a list of dictionaries.
    """
    if isinstance(data, list):
        return data

    if data is None:
        return []

    # deleting unwanted keys
    del data["incomplete_results"]
    del data["repository_selection"]
    del data["total_count"]

    # getting the first object of data
    keys = iter(data)
    first_key = next(keys)
    data = data[first_key]

    return data


def get_owner_and_reponame(repo_url: str) -> tuple:
    owner_and_repo = repo_url.removeprefix("https://github.com/")
    owner, _, repo_name = owner_and_repo.partition("/")

    return owner, repo_name


def parse_url(repo_url: str, target: str = None):
    """Parses a repository URL into the GitHub API format:
        https://api.github.com/repos/{owner}/{repo}

    Args:
        repo_url (str): The URL in the format https://github.com/user/repo.
        target (str): Additional term to specify which GitHub API endpoint to hit.

    Returns:
         str: a parsed URL ready to be used to make a call to GitHub's API.
    """
    owner, repo_name = get_owner_and_reponame(repo_url)
    url = f"https://api.github.com/repos/{owner}/{repo_name}"

    if target is not None:
        url += "/" + target

    return url
