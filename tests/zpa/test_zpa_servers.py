import pytest
import responses
from box import Box, BoxList
from responses import matchers

from tests.conftest import stub_sleep


# Don't need to test the data structure as we just have list and get
# methods available. id will suffice until add/update endpoints are available.
@pytest.fixture(name="servers")
def fixture_servers():
    return {
        "totalPages": 1,
        "list": [
            {
                "id": "1",
                "creationTime": "1625698796",
                "modifiedBy": "1",
                "name": "Test",
                "address": "1.1.1.1",
                "enabled": True,
                "appServerGroupIds": ["1"],
                "configSpace": "DEFAULT",
            },
            {
                "id": "2",
                "creationTime": "1625698796",
                "modifiedBy": "1",
                "name": "Test",
                "address": "1.1.1.1",
                "enabled": True,
                "appServerGroupIds": ["1"],
                "configSpace": "DEFAULT",
            },
        ],
    }


@responses.activate
@stub_sleep
def test_list_servers(zpa, servers):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/server?page=1",
        json=servers,
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/server?page=2",
        json=[],
        status=200,
    )
    resp = zpa.servers.list_servers()
    assert isinstance(resp, BoxList)
    assert len(resp) == 2
    assert resp[0].id == "1"


@responses.activate
def test_get_server(zpa, servers):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/server/1",
        json=servers["list"][0],
        status=200,
    )
    resp = zpa.servers.get_server("1")
    assert isinstance(resp, Box)
    assert resp.id == "1"


@responses.activate
def test_delete_server(zpa):
    responses.add(
        responses.DELETE,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/server/1",
        status=204,
    )
    resp = zpa.servers.delete_server("1")
    assert isinstance(resp, int)
    assert resp == 204


@responses.activate
def test_add_server(zpa, servers):
    responses.add(
        responses.POST,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/server",
        json=servers["list"][0],
        status=200,
        match=[
            matchers.json_params_matcher(
                {
                    "name": "Test",
                    "address": "1.1.1.1",
                    "enabled": True,
                    "description": "Test",
                }
            )
        ],
    )
    resp = zpa.servers.add_server(name="Test", address="1.1.1.1", enabled=True, description="Test")

    assert isinstance(resp, Box)
    assert resp.id == "1"


@responses.activate
def test_update_server(zpa, servers):
    updated_server = servers["list"][0]
    updated_server["name"] = "Updated Test"
    updated_server["appServerGroupIds"] = ["1", "2"]

    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/server/1",
        json=servers["list"][0],
        status=200,
    )

    responses.add(
        responses.PUT,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/server/1",
        status=204,
        match=[matchers.json_params_matcher(updated_server)],
    )

    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/server/1",
        json=updated_server,
        status=200,
    )

    resp = zpa.servers.update_server("1", name="Updated Test", app_server_group_ids=["1", "2"])

    assert isinstance(resp, Box)
    assert resp.id == "1"
    assert resp.name == updated_server["name"]
    assert resp.app_server_group_ids == updated_server["appServerGroupIds"]
