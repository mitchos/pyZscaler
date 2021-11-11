import pytest
import responses
from box import Box
from responses import matchers

from tests.conftest import stub_sleep


@pytest.fixture(name="locations")
def fixture_locations():
    return [
        {
            "dynamiclocationGroups": [{"id": 1, "name": "Unassigned Locations"}],
            "id": 1,
            "ipAddresses": ["203.0.113.1"],
            "name": "Test A",
            "profile": "SERVER",
        },
        {
            "country": "AUSTRALIA",
            "dynamiclocationGroups": [{"id": 1, "name": "Test Group"}],
            "id": 2,
            "ipAddresses": ["203.0.113.2"],
            "name": "Test B",
            "profile": "SERVER",
            "state": "NSW",
            "staticLocationGroups": [],
            "surrogateRefreshTimeInMinutes": 0,
            "tz": "AUSTRALIA_SYDNEY",
            "vpn_credentials": [{"id": 2, "type": "UFQDN", "fqdn": "test@example.com"}],
        },
    ]


@pytest.fixture(name="sub_locations")
def fixture_sub_locations():
    return [
        {
            "id": 1,
            "name": "Guest WiFi",
            "parentId": 1,
            "country": "Test",
            "state": "Test",
            "tz": "TEST",
            "ipAddresses": ["127.0.0.1-127.0.0.9"],
            "authRequired": True,
            "surrogateRefreshTimeInMinutes": 0,
            "staticLocationGroups": [],
            "dynamiclocationGroups": [{"id": 1, "name": "Guest Wifi Group"}],
            "profile": "GUESTWIFI",
        },
        {
            "id": 2,
            "name": "other",
            "parentId": 1,
            "country": "TEST",
            "state": "Test",
            "tz": "TEST",
            "authRequired": True,
            "otherSubLocation": True,
            "surrogateRefreshTimeInMinutes": 0,
            "staticLocationGroups": [],
            "dynamiclocationGroups": [{"id": 2, "name": "Corporate User Traffic Group"}],
            "profile": "CORPORATE",
        },
    ]


@responses.activate
@stub_sleep
def test_list_locations_with_one_page(zia, paginated_items):
    items = paginated_items(200)

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/locations",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/locations",
        json=items[100:200],
        status=200,
    )

    resp = zia.locations.list_locations(max_pages=1, page_size=100)

    assert isinstance(resp, list)
    assert resp[50].id == 50
    assert len(resp) == 100


@responses.activate
@stub_sleep
def test_list_locations_with_two_pages(zia, paginated_items):
    items = paginated_items(200)

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/locations",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/locations",
        json=items[100:200],
        status=200,
    )

    resp = zia.locations.list_locations(max_pages=2, page_size=100)

    assert isinstance(resp, list)
    assert resp[50].id == 50
    assert resp[150].id == 150
    assert len(resp) == 200


@responses.activate
@stub_sleep
def test_list_locations_with_max_items_1(zia, paginated_items):
    items = paginated_items(200)
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/locations",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/locations",
        json=items[100:200],
        status=200,
    )

    resp = zia.locations.list_locations(max_items=1)

    assert isinstance(resp, list)
    assert len(resp) == 1


@responses.activate
@stub_sleep
def test_list_locations_with_max_items_150(zia, paginated_items):
    items = paginated_items(150)
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/locations",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/locations",
        json=items[100:200],
        status=200,
    )

    resp = zia.locations.list_locations(max_items=150)

    assert isinstance(resp, list)
    assert len(resp) == 150


@responses.activate
def test_get_location_by_id(zia, locations):
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/locations/2",
        json=locations[1],
        status=200,
    )

    resp = zia.locations.get_location("2")

    assert isinstance(resp, dict)
    assert resp.id == 2
    assert isinstance(resp.vpn_credentials, list)


@responses.activate
def test_get_location_by_name_and_id(zia):
    # Passing location_id and location_name should result in a ValueError.
    with pytest.raises(ValueError):
        resp = zia.locations.get_location(location_id="1", location_name="Test A")


@responses.activate
def test_get_location_by_name(zia, locations):
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/locations?search=Test+B&page=1",
        json=locations,
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/locations?search=Test+B&page=2",
        json=[],
        status=200,
    )
    resp = zia.locations.get_location(location_name="Test B")

    assert isinstance(resp, Box)
    assert resp.name == "Test B"


@responses.activate
def test_delete_location(zia, locations):
    responses.add(
        responses.DELETE,
        url="https://zsapi.zscaler.net/api/v1/locations/1",
        body="204",
        status=204,
    )

    resp = zia.locations.delete_location("1")

    assert resp == 204


@responses.activate
def test_add_location(zia, locations):
    responses.add(
        responses.POST,
        url="https://zsapi.zscaler.net/api/v1/locations",
        status=200,
        json=locations[0],
        match=[
            matchers.json_params_matcher(
                {
                    "name": "Test",
                    "ipAddresses": ["203.0.113.1"],
                }
            )
        ],
    )

    resp = zia.locations.add_location(name="Test", ip_addresses=["203.0.113.1"])

    assert isinstance(resp, dict)
    assert resp.id == 1
    assert resp.ip_addresses[0] == "203.0.113.1"


@responses.activate
def test_update_location(zia, locations):
    updated_location = locations[0]
    updated_location["name"] = "Updated Test"

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/locations/1",
        json=locations[0],
        status=200,
    )

    responses.add(
        responses.PUT,
        url="https://zsapi.zscaler.net/api/v1/locations/1",
        status=200,
        json=updated_location,
        match=[matchers.json_params_matcher(updated_location)],
    )

    resp = zia.locations.update_location("1", name="Updated Test")

    assert isinstance(resp, dict)
    assert resp.id == 1
    assert resp.name == "Updated Test"


@responses.activate
@stub_sleep
def test_list_locations_lite_with_one_page(zia, paginated_items):
    items = paginated_items(200)

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/locations/lite",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/locations/lite",
        json=items[100:200],
        status=200,
    )

    resp = zia.locations.list_locations_lite(max_pages=1, page_size=100)

    assert isinstance(resp, list)
    assert resp[50].id == 50
    assert len(resp) == 100


@responses.activate
@stub_sleep
def test_list_locations_lite_with_two_pages(zia, paginated_items):
    items = paginated_items(200)

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/locations/lite",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/locations/lite",
        json=items[100:200],
        status=200,
    )

    resp = zia.locations.list_locations_lite(max_pages=2, page_size=100)

    assert isinstance(resp, list)
    assert resp[50].id == 50
    assert resp[150].id == 150
    assert len(resp) == 200


@responses.activate
@stub_sleep
def test_list_locations_lite_with_max_items_1(zia, paginated_items):
    items = paginated_items(200)
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/locations/lite",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/locations/lite",
        json=items[100:200],
        status=200,
    )

    resp = zia.locations.list_locations_lite(max_items=1)

    assert isinstance(resp, list)
    assert len(resp) == 1


@responses.activate
@stub_sleep
def test_list_locations_lite_with_max_items_150(zia, paginated_items):
    items = paginated_items(150)
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/locations/lite",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/locations/lite",
        json=items[100:200],
        status=200,
    )

    resp = zia.locations.list_locations_lite(max_items=150)

    assert isinstance(resp, list)
    assert len(resp) == 150


@responses.activate
def test_list_sublocations(zia, sub_locations):
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/locations/1/sublocations",
        json=sub_locations,
        status=200,
    )
    resp = zia.locations.list_sub_locations("1")
    assert isinstance(resp, list)
    assert len(resp) == 2
    assert resp[0].id == 1
