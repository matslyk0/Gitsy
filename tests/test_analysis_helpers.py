import backend.analysis_helpers as analysis_helpers

from datetime import datetime, timezone


def test_parse_timestamp() -> None:
    iso_timestamp = "2025-09-22T14:37:52Z"
    parsed_timestamp = analysis_helpers.parse_timestamp(iso_timestamp)

    real_timestamp = datetime(2025, 9, 22, 14, 37, 52, tzinfo=timezone.utc)
    assert parsed_timestamp == real_timestamp


def test_dict_pathfind() -> None:
    dictionary = {"layer 1": {"layer 2": {"layer 3": "found it"}}}
    keys = ["layer 1", "layer 2", "layer 3"]

    result = analysis_helpers.dict_pathfind(dictionary, keys)
    assert result == "found it"


def test_get_first_timestamp() -> None:
    time_from = datetime(2025, 9, 22, 14, 37, 52, tzinfo=timezone.utc)

    dictionaries = [
        {"a": {"b": {"c": "2025-11-30T19:10:07Z"}}},
        {"a": {"b": {"c": "2024-04-15T08:15:00Z"}}},
        {"a": {"b": {"c": "2023-03-01T20:59:30Z"}}}
    ]
    keys = ["a", "b", "c"]

    result = analysis_helpers.get_first_timestamp(time_from, dictionaries, keys)[0]
    assert result == datetime(2025, 11, 30, 19, 10, 7, tzinfo=timezone.utc)


def test_get_latest_timestamp() -> None:
    time_until = datetime(2025, 9, 22, 14, 37, 52, tzinfo=timezone.utc)

    dictionaries = [
        {"a": {"b": {"c": "2025-11-30T19:10:07Z"}}},
        {"a": {"b": {"c": "2024-04-15T08:15:00Z"}}},
        {"a": {"b": {"c": "2023-03-01T20:59:30Z"}}}
    ]
    keys = ["a", "b", "c"]

    result = analysis_helpers.get_latest_timestamp(time_until, dictionaries, keys)[0]
    assert result == datetime(2024, 4, 15, 8, 15, 0, tzinfo=timezone.utc)


def test_trim_prior_entries() -> None:
    time_from = datetime(2025, 9, 22, 14, 37, 52, tzinfo=timezone.utc)

    dictionaries = [
        {"a": {"b": {"c": "2025-11-30T19:10:07Z"}}},
        {"a": {"b": {"c": "2024-04-15T08:15:00Z"}}},
        {"a": {"b": {"c": "2023-03-01T20:59:30Z"}}}
    ]
    keys = ["a", "b", "c"]

    result = analysis_helpers.trim_prior_entries(time_from, dictionaries, keys)
    assert result == [{"a": {"b": {"c": "2025-11-30T19:10:07Z"}}}]


def test_trim_leading_entries() -> None:
    time_until = datetime(2025, 9, 22, 14, 37, 52, tzinfo=timezone.utc)

    dictionaries = [
        {"a": {"b": {"c": "2025-11-30T19:10:07Z"}}},
        {"a": {"b": {"c": "2024-04-15T08:15:00Z"}}},
        {"a": {"b": {"c": "2023-03-01T20:59:30Z"}}}
    ]
    keys = ["a", "b", "c"]

    result = analysis_helpers.trim_leading_entries(time_until, dictionaries, keys)
    assert result == [{"a": {"b": {"c": "2024-04-15T08:15:00Z"}}},
                      {"a": {"b": {"c": "2023-03-01T20:59:30Z"}}}]
