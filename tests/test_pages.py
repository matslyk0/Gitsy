def test_home(get_test_client):
    test_client = get_test_client
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == "Welcome to Gitsy!"


def test_getstarted(get_test_client):
    test_client = get_test_client
    response = test_client.get("/get-started")
    assert response.status_code == 200
    assert response.json() == "Let's get started with Gitsy!"


def test_createreport(get_test_client):
    test_client = get_test_client
    response = test_client.get("/create-report")
    assert response.status_code == 200
    assert response.json() == "Let's create a report!"
