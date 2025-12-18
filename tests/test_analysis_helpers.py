import backend.analysis_helpers as analysis_helpers

from datetime import datetime, timezone

# ------------------------------------- Unit Tests -------------------------------------


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
