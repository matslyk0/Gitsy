import backend.helpers as helpers


def test_parse_data_listdict() -> None:
    data = [{"key": "success"}]
    result = helpers.parse_data(data)
    assert result == [{"key": "success"}]


def test_parse_data_dict() -> None:
    data = {
        "incomplete_results": 0,
        "repository_selection": "something",
        "total_count": 100,
        "desired_data": [{"key": "success"}],
    }
    result = helpers.parse_data(data)
    assert result == [{"key": "success"}]


def test_parse_data_empty() -> None:
    data = None
    result = helpers.parse_data(data)
    assert result == []


def test_parse_url_without_target() -> None:
    repo_url = "https://github.com/matslyk0/Gitsy"
    result = helpers.parse_url(repo_url)
    assert result == "https://api.github.com/repos/matslyk0/Gitsy"


def test_parse_url_with_target() -> None:
    repo_url = "https://github.com/matslyk0/Gitsy"
    result = helpers.parse_url(repo_url, "commits")
    assert result == "https://api.github.com/repos/matslyk0/Gitsy/commits"


def test_get_owner_and_response() -> None:
    repo_url = "https://github.com/matslyk0/Gitsy"
    result = helpers.get_owner_and_repo(repo_url)
    assert result == ("matslyk0", "Gitsy")
