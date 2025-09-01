def test_read_dummy(client_with_overrides):
    response = client_with_overrides.get("/dummy")
    assert response.status_code == 200
    assert response.json() == []
