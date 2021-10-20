import pytest
import responses
from responses import matchers


@pytest.fixture(name="locations")
def fixture_locations():
    return [
        {
            "dynamiclocationGroups": [{"id": 1, "name": "Unassigned Locations"}],
            "id": 1,
            "ipAddresses": ["203.0.113.1"],
            "name": "Test",
            "profile": "SERVER",
        },
        {
            "country": "AUSTRALIA",
            "dynamiclocationGroups": [{"id": 1, "name": "Test Group"}],
            "id": 2,
            "ipAddresses": ["203.0.113.2"],
            "name": "Test",
            "profile": "SERVER",
            "state": "NSW",
            "staticLocationGroups": [],
            "surrogateRefreshTimeInMinutes": 0,
            "tz": "AUSTRALIA_SYDNEY",
            "vpn_credentials": [{"id": 2, "type": "UFQDN", "fqdn": "test@example.com"}],
        },
    ]


@responses.activate
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
def test_get_location(zia, locations):
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
            responses.json_params_matcher(
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
        match=[
            matchers.json_params_matcher(updated_location)
        ],
    )

    resp = zia.locations.update_location("1", name="Updated Test")

    assert isinstance(resp, dict)
    assert resp.id == 1
    assert resp.name == "Updated Test"


@responses.activate
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
