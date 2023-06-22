import responses
from box import Box, BoxList

from tests.conftest import stub_sleep


@responses.activate
def test_list_apps(zdx):
    url = "https://api.zdxcloud.net/v1/apps"
    mock_response = [{"id": "1", "name": "app1"}, {"id": "2", "name": "app2"}]
    responses.add(responses.GET, url, json=mock_response, status=200)

    result = zdx.apps.list_apps()

    assert isinstance(result, BoxList)
    assert len(result) == 2
    assert result[0]["id"] == "1"
    assert result[1]["id"] == "2"

    request = responses.calls[0].request
    assert request.url == url
    assert request.method == "GET"


@responses.activate
def test_get_app(zdx):
    app_id = "1"
    url = f"https://api.zdxcloud.net/v1/apps/{app_id}"
    mock_response = {"id": "1", "name": "app1"}
    responses.add(responses.GET, url, json=mock_response, status=200)

    result = zdx.apps.get_app(app_id)

    assert isinstance(result, Box)
    assert result["id"] == "1"
    assert result["name"] == "app1"

    request = responses.calls[0].request
    assert request.url == url
    assert request.method == "GET"


@responses.activate
def test_get_app_score(zdx):
    app_id = "1"
    url = f"https://api.zdxcloud.net/v1/apps/{app_id}/score"
    mock_response = {
        "metric": "score",
        "datapoints": [
            {"timestamp": 1644163200, "value": 80},
            {"timestamp": 1644163500, "value": 75},
        ],
    }
    responses.add(responses.GET, url, json=mock_response, status=200)

    result = zdx.apps.get_app_score(app_id)

    assert isinstance(result, Box)
    assert result["metric"] == "score"
    assert len(result["datapoints"]) == 2

    request = responses.calls[0].request
    assert request.url == url
    assert request.method == "GET"


@responses.activate
def test_get_app_metrics(zdx):
    app_id = "1"
    url = f"https://api.zdxcloud.net/v1/apps/{app_id}/metrics"
    mock_response = {
        "metric": "metricName",
        "unit": "metricUnit",
        "datapoints": [
            {"timestamp": 1644163200, "value": 100},
            {"timestamp": 1644163500, "value": 90},
        ],
    }
    responses.add(responses.GET, url, json=mock_response, status=200)

    result = zdx.apps.get_app_metrics(app_id)

    assert isinstance(result, Box)
    assert result["metric"] == "metricName"
    assert result["unit"] == "metricUnit"
    assert len(result["datapoints"]) == 2

    request = responses.calls[0].request
    assert request.url == url
    assert request.method == "GET"


@responses.activate
@stub_sleep
def test_list_app_users(zdx):
    app_id = "1"
    url = f"https://api.zdxcloud.net/v1/apps/{app_id}/users"
    mock_response = {
        "users": [
            {"id": "1", "name": "user1", "email": "user1@example.com", "score": 80},
            {"id": "2", "name": "user2", "email": "user2@example.com", "score": 90},
        ],
        "next_offset": None,
    }
    responses.add(responses.GET, url, json=mock_response, status=200)

    result = zdx.apps.list_app_users(app_id)

    assert isinstance(result, BoxList)
    assert len(result) == 2
    assert result[0]["id"] == "1"
    assert result[1]["id"] == "2"

    request = responses.calls[0].request
    assert request.url == url
    assert request.method == "GET"


@responses.activate
@stub_sleep
def test_list_app_users_multipage(zdx):
    app_id = "1"
    url = f"https://api.zdxcloud.net/v1/apps/{app_id}/users"
    url_with_offset = f"https://api.zdxcloud.net/v1/apps/{app_id}/users?offset=2"

    # First page response
    mock_response_1 = {
        "users": [
            {"id": "1", "name": "user1", "email": "user1@example.com", "score": 80},
            {"id": "2", "name": "user2", "email": "user2@example.com", "score": 90},
        ],
        "next_offset": "2",
    }
    responses.add(responses.GET, url, json=mock_response_1, status=200)

    # Second page response
    mock_response_2 = {
        "users": [
            {"id": "3", "name": "user3", "email": "user3@example.com", "score": 70},
            {"id": "4", "name": "user4", "email": "user4@example.com", "score": 60},
        ],
        "next_offset": None,  # Signifying no more pages
    }
    responses.add(responses.GET, url_with_offset, json=mock_response_2, status=200)

    result = zdx.apps.list_app_users(app_id)

    assert isinstance(result, BoxList)
    assert len(result) == 4  # Total of 4 users across 2 pages
    assert result[0]["id"] == "1"
    assert result[1]["id"] == "2"
    assert result[2]["id"] == "3"
    assert result[3]["id"] == "4"

    # Check the first API request
    request1 = responses.calls[0].request
    assert request1.url == url
    assert request1.method == "GET"

    # Check the second API request
    request2 = responses.calls[1].request
    assert request2.url == url_with_offset


@responses.activate
def test_get_app_user(zdx):
    app_id = "1"
    user_id = "1"
    url = f"https://api.zdxcloud.net/v1/apps/{app_id}/users/{user_id}"
    since = 10
    mock_response = {
        "user": {"id": "1", "name": "user1", "email": "user1@example.com", "score": 80},
        "device": {"id": "device1", "model": "iPhone", "os": "iOS"},
    }
    responses.add(responses.GET, url, json=mock_response, status=200)

    result = zdx.apps.get_app_user(app_id, user_id, since=since)

    assert isinstance(result, Box)
    assert result.user.id == mock_response["user"]["id"]
    assert result.user.name == mock_response["user"]["name"]
    assert result.user.email == mock_response["user"]["email"]
    assert result.user.score == mock_response["user"]["score"]
    assert result.device.id == mock_response["device"]["id"]
    assert result.device.model == mock_response["device"]["model"]
    assert result.device.os == mock_response["device"]["os"]
