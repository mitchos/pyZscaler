import pytest
import responses
from box import Box, BoxList
from responses import matchers

from tests.conftest import stub_sleep


@pytest.fixture(name="provisioning_keys")
def fixture_provisioning_keys():
    return {
        "totalPages": 1,
        "list": [
            {
                "id": "1",
                "modifiedTime": "1623890719",
                "creationTime": "1623889186",
                "modifiedBy": "1",
                "name": "Test A",
                "usageCount": "1",
                "maxUsage": "2",
                "zcomponentId": "1",
                "enabled": True,
                "zcomponentName": "Test",
                "provisioningKey": "xxxxxxxyyyyyyyzzzzzzz",
                "enrollmentCertId": "1",
                "enrollmentCertName": "Test",
                "appConnectorGroupName": "Test",
            },
            {
                "id": "2",
                "modifiedTime": "1623890719",
                "creationTime": "1623889186",
                "modifiedBy": "1",
                "name": "Test B",
                "usageCount": "1",
                "maxUsage": "2",
                "zcomponentId": "1",
                "enabled": True,
                "zcomponentName": "Test",
                "provisioningKey": "xxxxxxxyyyyyyyzzzzzzz",
                "enrollmentCertId": "1",
                "enrollmentCertName": "Test",
                "appConnectorGroupName": "Test",
            },
        ],
    }


@responses.activate
@stub_sleep
def test_list_connector_provisioning_keys(zpa, provisioning_keys):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/associationType/CONNECTOR_GRP/provisioningKey?page=1",  # noqa: E501
        json=provisioning_keys,
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/associationType/CONNECTOR_GRP/provisioningKey?page=2",  # noqa: E501
        json=[],
        status=200,
    )
    resp = zpa.provisioning.list_provisioning_keys("connector")
    assert isinstance(resp, BoxList)
    assert len(resp) == 2
    assert resp[0].id == "1"


@responses.activate
@stub_sleep
def test_list_service_edge_provisioning_keys(zpa, provisioning_keys):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/associationType/SERVICE_EDGE_GRP/provisioningKey?page=1",  # noqa: E501
        json=provisioning_keys,
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/associationType/SERVICE_EDGE_GRP/provisioningKey?page=2",  # noqa: E501
        json=[],
        status=200,
    )
    resp = zpa.provisioning.list_provisioning_keys("service_edge")
    assert isinstance(resp, BoxList)
    assert len(resp) == 2
    assert resp[0].id == "1"


@responses.activate
def test_get_connector_provisioning_key(zpa, provisioning_keys):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/associationType/CONNECTOR_GRP/provisioningKey/1",  # noqa: E501
        json=provisioning_keys["list"][0],
        status=200,
    )
    resp = zpa.provisioning.get_provisioning_key("1", key_type="connector")
    assert isinstance(resp, Box)
    assert resp.id == "1"


@responses.activate
def test_get_service_edge_provisioning_key(zpa, provisioning_keys):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/associationType/SERVICE_EDGE_GRP/provisioningKey/1",  # noqa: E501
        json=provisioning_keys["list"][0],
        status=200,
    )
    resp = zpa.provisioning.get_provisioning_key("1", key_type="service_edge")
    assert isinstance(resp, Box)
    assert resp.id == "1"


@responses.activate
def test_delete_connector_provisioning_key(zpa):
    responses.add(
        responses.DELETE,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/associationType/CONNECTOR_GRP/provisioningKey/1",  # noqa: E501
        status=204,
    )
    resp = zpa.provisioning.delete_provisioning_key("1", key_type="connector")
    assert isinstance(resp, int)
    assert resp == 204


@responses.activate
def test_delete_service_edge_provisioning_key(zpa):
    responses.add(
        responses.DELETE,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/associationType/SERVICE_EDGE_GRP/provisioningKey/1",  # noqa: E501
        status=204,
    )
    resp = zpa.provisioning.delete_provisioning_key("1", key_type="service_edge")
    assert isinstance(resp, int)
    assert resp == 204


@responses.activate
def test_add_connector_provisioning_key(zpa, provisioning_keys):
    responses.add(
        responses.POST,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/associationType/CONNECTOR_GRP/provisioningKey",  # noqa: E501
        json=provisioning_keys["list"][0],
        status=200,
        match=[
            matchers.json_params_matcher(
                {"name": "Test", "maxUsage": "2", "enrollmentCertId": "1", "zcomponentId": "1", "enabled": True}
            )
        ],
    )
    resp = zpa.provisioning.add_provisioning_key(
        key_type="connector",
        name="Test",
        max_usage="2",
        enrollment_cert_id="1",
        component_id="1",
        enabled=True,
    )
    assert isinstance(resp, Box)
    assert resp.id == "1"


@responses.activate
def test_update_connector_provisioning_key(zpa, provisioning_keys):
    updated_keys = provisioning_keys["list"][0]
    updated_keys["name"] = "Updated Test"

    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/associationType/CONNECTOR_GRP/provisioningKey/1",  # noqa: E501
        json=provisioning_keys["list"][0],
        status=200,
    )
    responses.add(
        responses.PUT,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/associationType/CONNECTOR_GRP/provisioningKey/1",  # noqa: E501
        status=204,
        match=[matchers.json_params_matcher(updated_keys)],
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/associationType/CONNECTOR_GRP/provisioningKey/1",  # noqa: E501
        json=updated_keys,
        status=200,
    )
    resp = zpa.provisioning.update_provisioning_key("1", key_type="connector", name="Updated Test")
    assert isinstance(resp, Box)
    assert resp.id == "1"
    assert resp.name == updated_keys["name"]


@responses.activate
def test_add_service_edge_provisioning_key(zpa, provisioning_keys):
    responses.add(
        responses.POST,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/associationType/SERVICE_EDGE_GRP/provisioningKey",  # noqa: E501
        json=provisioning_keys["list"][0],
        status=200,
        match=[
            matchers.json_params_matcher(
                {"name": "Test", "maxUsage": "2", "enrollmentCertId": "1", "zcomponentId": "1", "enabled": True}
            )
        ],
    )
    resp = zpa.provisioning.add_provisioning_key(
        key_type="service_edge",
        name="Test",
        max_usage="2",
        enrollment_cert_id="1",
        component_id="1",
        enabled=True,
    )
    assert isinstance(resp, Box)
    assert resp.id == "1"


@responses.activate
def test_update_service_edge_provisioning_key(zpa, provisioning_keys):
    updated_keys = provisioning_keys["list"][0]
    updated_keys["name"] = "Updated Test"

    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/associationType/SERVICE_EDGE_GRP/provisioningKey/1",  # noqa: E501
        json=provisioning_keys["list"][0],
        status=200,
    )
    responses.add(
        responses.PUT,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/associationType/SERVICE_EDGE_GRP/provisioningKey/1",  # noqa: E501
        status=204,
        match=[matchers.json_params_matcher(updated_keys)],
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/associationType/SERVICE_EDGE_GRP/provisioningKey/1",  # noqa: E501
        json=updated_keys,
        status=200,
    )
    resp = zpa.provisioning.update_provisioning_key("1", key_type="service_edge", name="Updated Test")
    assert isinstance(resp, Box)
    assert resp.id == "1"
    assert resp.name == updated_keys["name"]


def test_provisioning_key_type_valueerror(zpa, provisioning_keys):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/associationType/CONNECTOR_GRP/provisioningKey/1",  # noqa: E501
        json=provisioning_keys["list"][0],
        status=200,
    )
    with pytest.raises(Exception) as e_info:
        resp = zpa.provisioning.get_provisioning_key("1", key_type="test")
