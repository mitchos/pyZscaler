import pytest
import responses
from box import Box, BoxList

from tests.conftest import stub_sleep


# Don't need to test the data structure as we just have list and get
# methods available. id will suffice until add/update endpoints are available.
@pytest.fixture(name="cloud_connector_groups")
def fixture_cloud_connector_groups():
    return {"totalPages": 1, "list": [{"id": "1"}, {"id": "2"}]}


@responses.activate
@stub_sleep
def test_list_cloud_connector_groups(zpa, cloud_connector_groups):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/cloudConnectorGroup?page=1",
        json=cloud_connector_groups,
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/cloudConnectorGroup?page=2",
        json=[],
        status=200,
    )
    resp = zpa.cloud_connector_groups.list_groups()
    assert isinstance(resp, BoxList)
    assert len(resp) == 2
    assert resp[0].id == "1"


@responses.activate
def test_get_cloud_connector_groups(zpa, cloud_connector_groups):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/cloudConnectorGroup/1",
        json=cloud_connector_groups["list"][0],
        status=200,
    )
    resp = zpa.cloud_connector_groups.get_group("1")
    assert isinstance(resp, Box)
    assert resp.id == "1"
