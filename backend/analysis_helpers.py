from datetime import datetime


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
