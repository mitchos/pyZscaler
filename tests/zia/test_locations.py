import pytest
import responses


@pytest.fixture(name="locations")
def fixture_locations():
    return [
        {
            "dynamiclocationGroups": [
                {"id": 1, "name": "Unassigned Locations"}
            ],
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
def test_list_locations(zia, locations):
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/locations",
        json=locations,
        status=200,
    )

    resp = zia.locations.list_locations(max_items=1)

    assert isinstance(resp, list)
    for location in resp:
        assert isinstance(location, dict)
        assert isinstance(location.id, int)


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
        match=[responses.json_params_matcher({
            'name': 'Test',
            'ipAddresses': ['203.0.113.1'],
        })],
    )

    resp = zia.locations.add_location(name="Test", ip_addresses=["203.0.113.1"])

    assert isinstance(resp, dict)
    assert resp.id == 1
    assert resp.ip_addresses[0] == '203.0.113.1'


@responses.activate
def test_update_location(zia, locations):
    updated_location = locations[0]
    updated_location['name'] = 'Updated Test'

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
        match=[responses.json_params_matcher({
            'name': 'Updated Test',
            'ipAddresses': ['203.0.113.1']
        })],
    )

    resp = zia.locations.update_location('1',
                                         name='Updated Test')

    assert isinstance(resp, dict)
    assert resp.id == 1
    assert resp.name == 'Updated Test'
