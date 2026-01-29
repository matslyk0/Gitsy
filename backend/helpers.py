from datetime import datetime


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


def get_owner_and_repo(repo_url: str) -> tuple:
    """Extracts the owner name and repository name from a valid url
        in the format https://github.com/owner/repo

    Args:
        repo_url (str): The URL in the format https://github.com/user/repo.

    Returns:
        tuple: a tuple in the form (owner, repo)
    """
    owner_and_repo = repo_url.removeprefix("https://github.com/")
    owner, _, repo = owner_and_repo.partition("/")

    return owner, repo


def parse_url(repo_url: str, target: str = None):
    """Parses a repository URL into the GitHub API format:
        https://api.github.com/repos/owner/repo

    Args:
        repo_url (str): The URL in the format https://github.com/user/repo.
        target (str): Additional term to specify which GitHub API endpoint to hit.

    Returns:
         str: a parsed URL ready to be used to make a call to GitHub's API.
    """
    owner, repo = get_owner_and_repo(repo_url)
    url = f"https://api.github.com/repos/{owner}/{repo}"

    if target is not None:
        url += "/" + target

    return url


def parse_timestamp(timestamp: str) -> datetime:
    """Parses an ISO 8601 format timestamp into a datetime object.

    Args:
        timestamp (str): A timestamp in ISO 8601 format.

    Returns:
        datetime: a datetime object of the time
    """
    date = timestamp.replace("Z", "+00:00")
    return datetime.fromisoformat(date)


def dict_pathfind(dictionary: dict, keys: list):
    """Loops through a set of keys to obtain an item in a nested dictionary.

    Args:
        dictionary (dict): A non-empty dictionary of any items.
        keys (list): A list of keys in descending order.

    Returns:
        Any: The object found at the path provided.
    """
    first_key = keys[0]
    item = dictionary[first_key]

    for key in keys[1:]:
        item = item[key]

    return item
