from datetime import datetime, timedelta
from backend.exceptions import TimeOutOfBoundsError


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
    """Loops through a set of keys to obtain an item.

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


def get_first_timestamp(time_from: datetime, dictionaries: list[dict], keys: list) -> datetime:
    """Calculates the closest timestamp after the one provided.

    Args:
        time_from (datetime): The time to start looking from.
        dictionaries (list[dict]): The dictionaries to look through.
        keys (list): A list of keys in descending order to find timestamps.

    Returns:
        datetime: The closest timestamp after the one provided.

    Raises:
         TimeOutOfBoundsError: If there is no closest timestamp after the one provided.
    """
    earliest_dictionary = dictionaries[::-1][0]
    earliest_timestamp_raw = dict_pathfind(earliest_dictionary, keys)
    earliest_timestamp = parse_timestamp(earliest_timestamp_raw)
    if earliest_timestamp >= time_from:
        return earliest_timestamp

    remaining_dictionaries = dictionaries[::-1][1:]
    for dictionary in remaining_dictionaries:
        timestamp_raw = dict_pathfind(dictionary, keys)
        timestamp = parse_timestamp(timestamp_raw)
        if timestamp >= time_from:
            return timestamp

    raise TimeOutOfBoundsError("Could not find nearest timestamp - try an earlier one.")


def get_latest_timestamp(time_until: datetime, dictionaries: list[dict], keys: list) -> datetime:
    """Calculates the closest timestamp before the one provided.

    Args:
        time_until (datetime): The time to start looking before.
        dictionaries (list[dict]): The dictionaries to look through.
        keys (list): A list of keys in descending order to find timestamps.

    Returns:
        datetime: The closest timestamp before the one provided.

    Raises:
         TimeOutOfBoundsError: If there is no closest timestamp before the one provided.
    """
    latest_dictionary = dictionaries[0]
    latest_timestamp_raw = dict_pathfind(latest_dictionary, keys)
    latest_timestamp = parse_timestamp(latest_timestamp_raw)
    if latest_timestamp <= time_until:
        return latest_timestamp

    remaining_dictionaries = dictionaries[1:]
    for dictionary in remaining_dictionaries:
        timestamp_raw = dict_pathfind(dictionary, keys)
        timestamp = parse_timestamp(timestamp_raw)
        if timestamp <= time_until:
            return timestamp

    raise TimeOutOfBoundsError("Could not find nearest timestamp - try a later one.")


def trim_prior_entries(time_from: datetime, dictionaries: list[dict], keys: list) -> list[dict]:
    """Clears dictionaries from a list before the timestamp provided.

    Args:
        time_from (datetime): The time from which dictionaries are included.
        dictionaries (list[dict]): A list of dictionaries with timestamps.
        keys (list): A list of keys in descending order to find timestamps.

    Returns:
        list[dict]: The entry list with less or equal objects.

    Raises:
        TimeOutOfBoundsError: If the timestamp provided was too late.
    """
    earliest_dictionary = dictionaries[::-1][0]
    earliest_timestamp_raw = dict_pathfind(earliest_dictionary, keys)
    earliest_timestamp = parse_timestamp(earliest_timestamp_raw)
    if earliest_timestamp >= time_from:
        return dictionaries

    latest_dictionary = dictionaries[0]
    latest_timestamp_raw = dict_pathfind(latest_dictionary, keys)
    latest_timestamp = parse_timestamp(latest_timestamp_raw)
    if latest_timestamp < time_from:
        raise TimeOutOfBoundsError("Timestamp is too far ahead - try an earlier one.")

    trimmed_dictionaries = dictionaries[:]
    for dictionary in dictionaries:
        timestamp_raw = dict_pathfind(dictionary, keys)
        timestamp = parse_timestamp(timestamp_raw)
        if timestamp < time_from:
            trimmed_dictionaries.remove(dictionary)

    return trimmed_dictionaries


def trim_leading_entries(time_until: datetime, dictionaries: list[dict], keys: list) -> list[dict]:
    """Clears dictionaries from a list after the timestamp provided.

    Args:
        time_until (datetime): The time until which dictionaries are included.
        dictionaries (list[dict]): A list of dictionaries with timestamps.
        keys (list): A list of keys in descending order to find timestamps.

    Returns:
        list[dict]: The entry list with less or equal objects.

    Raises:
        TimeOutOfBoundsError: If the timestamp provided was too early.
    """
    latest_dictionary = dictionaries[0]
    latest_timestamp_raw = dict_pathfind(latest_dictionary, keys)
    latest_timestamp = parse_timestamp(latest_timestamp_raw)
    if latest_timestamp <= time_until:
        return dictionaries

    earliest_dictionary = dictionaries[::-1][0]
    earliest_timestamp_raw = dict_pathfind(earliest_dictionary, keys)
    earliest_timestamp = parse_timestamp(earliest_timestamp_raw)
    if earliest_timestamp > time_until:
        raise TimeOutOfBoundsError("Timestamp is too far behind - try a later one.")

    trimmed_dictionaries = dictionaries[:]
    for dictionary in dictionaries:
        timestamp_raw = dict_pathfind(dictionary, keys)
        timestamp = parse_timestamp(timestamp_raw)
        if timestamp > time_until:
            trimmed_dictionaries.remove(dictionary)

    return trimmed_dictionaries