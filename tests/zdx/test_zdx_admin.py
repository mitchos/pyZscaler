import responses
from box import BoxList

from pyzscaler.utils import calculate_epoch


@responses.activate
def test_list_geolocations(zdx):
    # set up the mock response

    mock_response = [
        {
            "id": "1",
            "name": "geolocation1",
            "geo_type": "region",
            "children": [{"id": "11", "description": "child geolocation1", "geo_type": "country"}],
        },
        {
            "id": "2",
            "name": "geolocation2",
            "geo_type": "region",
            "children": [{"id": "21", "description": "child geolocation2", "geo_type": "country"}],
        },
    ]
    current, past = calculate_epoch(2)
    url = "https://api.zdxcloud.net/v1/active_geo"
    responses.add(responses.GET, url, json=mock_response, status=200)

    # call the method
    result = zdx.admin.list_geolocations()

    # assert the response is correct
    assert isinstance(result, BoxList)
    assert len(result) == 2
    assert result[0]["id"] == "1"
    assert result[1]["id"] == "2"

    # assert the request is correct
    request = responses.calls[0].request
    assert request.url == url
    assert request.method == "GET"


@responses.activate
def test_list_departments(zdx):
    url = "https://api.zdxcloud.net/v1/administration/departments"
    mock_response = [{"id": "1", "name": "department1"}, {"id": "2", "name": "department2"}]
    responses.add(responses.GET, url, json=mock_response, status=200)

    # call the method
    result = zdx.admin.list_departments()

    # assert the response is correct
    assert isinstance(result, BoxList)
    assert len(result) == 2
    assert result[0]["id"] == "1"
    assert result[1]["id"] == "2"

    # assert the request is correct
    request = responses.calls[0].request
    assert request.url == url
    assert request.method == "GET"


@responses.activate
def test_list_locations(zdx):
    url = "https://api.zdxcloud.net/v1/administration/locations"
    mock_response = [{"id": "1", "name": "location1"}, {"id": "2", "name": "location2"}]
    responses.add(responses.GET, url, json=mock_response, status=200)

    # call the method
    result = zdx.admin.list_locations()

    # assert the response is correct
    assert isinstance(result, BoxList)
    assert len(result) == 2
    assert result[0]["id"] == "1"
    assert result[1]["id"] == "2"

    # assert the request is correct
    request = responses.calls[0].request
    assert request.url == url
    assert request.method == "GET"
