import pytest
import responses
from box import Box, BoxList
from responses import matchers

from tests.conftest import stub_sleep


@pytest.fixture(name="server_groups")
def fixture_server_groups():
    return {
        "totalPages": 1,
        "list": [
            {
                "creationTime": "1625698796",
                "modifiedBy": "1",
                "id": "1",
                "enabled": True,
                "name": "Test",
                "servers": [
                    {
                        "id": "1",
                        "creationTime": "1625698796",
                        "modifiedBy": "1",
                        "name": "Test",
                        "address": "1.1.1.1",
                        "enabled": True,
                        "configSpace": "DEFAULT",
                    }
                ],
                "applications": [{"id": "1", "name": "Test"}],
                "ipAnchored": False,
                "configSpace": "DEFAULT",
                "dynamicDiscovery": False,
                "appConnectorGroups": [
                    {
                        "id": "1",
                        "creationTime": "1623441900",
                        "modifiedBy": "1",
                        "name": "Test",
                        "enabled": True,
                        "description": "Test",
                        "overrideVersionProfile": False,
                        "location": "Test",
                        "dnsQueryType": "IPV4_IPV6",
                        "cityCountry": "Test",
                        "countryCode": "TEST",
                        "lssAppConnectorGroup": False,
                    }
                ],
            },
            {
                "creationTime": "1625698796",
                "modifiedBy": "1",
                "id": "2",
                "enabled": True,
                "name": "Updated Test",
                "servers": [
                    {
                        "id": "2",
                        "creationTime": "1625698796",
                        "modifiedBy": "1",
                        "name": "Test",
                        "address": "1.1.1.1",
                        "enabled": True,
                        "configSpace": "DEFAULT",
                    }
                ],
                "applications": [{"id": "1", "name": "Test"}],
                "ipAnchored": False,
                "configSpace": "DEFAULT",
                "dynamicDiscovery": False,
                "appConnectorGroups": [
                    {
                        "id": "1",
                        "creationTime": "1623441900",
                        "modifiedBy": "1",
                        "name": "Test",
                        "enabled": True,
                        "description": "Updated Test",
                        "overrideVersionProfile": False,
                        "location": "Test",
                        "dnsQueryType": "IPV4_IPV6",
                        "cityCountry": "Test",
                        "countryCode": "TEST",
                        "lssAppConnectorGroup": False,
                    }
                ],
            },
        ],
    }


@responses.activate
@stub_sleep
def test_list_groups(zpa, server_groups):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/serverGroup?page=1",
        json=server_groups,
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/serverGroup?page=2",
        json=[],
        status=200,
    )
    resp = zpa.server_groups.list_groups()
    assert isinstance(resp, BoxList)
    assert len(resp) == 2
    assert resp[0].id == "1"


@responses.activate
def test_get_group(zpa, server_groups):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/serverGroup/1",
        json=server_groups["list"][0],
        status=200,
    )
    resp = zpa.server_groups.get_group("1")
    assert isinstance(resp, Box)
    assert resp.id == "1"


@responses.activate
def test_delete_group(zpa):
    responses.add(
        responses.DELETE,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/serverGroup/1",
        status=204,
    )
    resp = zpa.server_groups.delete_group("1")
    assert resp == 204


@responses.activate
def test_add_group(zpa, server_groups):
    responses.add(
        responses.POST,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/serverGroup",
        json=server_groups["list"][0],
        status=200,
        match=[
            matchers.json_params_matcher(
                {
                    "name": "Test",
                    "appConnectorGroups": [{"id": "1"}],
                    "description": "Test",
                    "servers": [{"id": "1"}],
                }
            )
        ],
    )
    resp = zpa.server_groups.add_group(
        name="Test",
        app_connector_group_ids=["1"],
        description="Test",
        server_ids=["1"],
    )
    assert isinstance(resp, Box)
    assert resp.id == "1"


@responses.activate
def test_update_group(zpa, server_groups):
    updated_group = server_groups["list"][0]
    updated_group["appConnectorGroups"] = [{"id": "2"}]
    updated_group["servers"] = [{"id": "2"}]
    updated_group["description"] = "Updated Test"
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/serverGroup/1",
        json=server_groups["list"][0],
        status=200,
    )
    responses.add(
        responses.PUT,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/serverGroup/1",
        status=204,
        match=[matchers.json_params_matcher(updated_group)],
    )
    resp = zpa.server_groups.update_group(
        "1",
        app_connector_group_ids=["2"],
        description="Updated Test",
        server_ids=["2"],
    )
    assert isinstance(resp, Box)
    assert resp.id == "1"
    assert resp.servers[0].id == "2"
    assert resp.app_connector_groups[0].id == "2"
    assert resp.description == "Updated Test"
