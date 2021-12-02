import pytest
import responses
from box import Box, BoxList

from tests.conftest import stub_sleep


# Don't need to test the data structure as we just have list and get
# methods available. id will suffice until add/update endpoints are available.
@pytest.fixture(name="scim_attributes")
def fixture_scim_attributes():
    return {"totalPages": 1, "list": [{"id": "1"}, {"id": "2"}]}


@responses.activate
@stub_sleep
def test_list_scim_attributes_by_idp(zpa, scim_attributes):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/idp/1/scimattribute?page=1",
        json=scim_attributes,
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/idp/1/scimattribute?page=2",
        json=[],
        status=200,
    )
    resp = zpa.scim_attributes.list_attributes_by_idp("1")
    assert isinstance(resp, BoxList)
    assert len(resp) == 2
    assert resp[0].id == "1"


@responses.activate
def test_get_scim_attribute(zpa, scim_attributes):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/idp/1/scimattribute/1",
        json=scim_attributes["list"][0],
        status=200,
    )
    resp = zpa.scim_attributes.get_attribute("1", "1")
    assert isinstance(resp, Box)
    assert resp.id == "1"


@responses.activate
@stub_sleep
def test_list_scim_values(zpa, scim_attributes):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/userconfig/v1/customers/1/scimattribute/idpId/1/attributeId/1?page=1",
        json=scim_attributes,
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/userconfig/v1/customers/1/scimattribute/idpId/1/attributeId/1?page=2",
        json=[],
        status=200,
    )
    resp = zpa.scim_attributes.get_values("1", "1")
    assert isinstance(resp, BoxList)
    assert len(resp) == 2
    assert resp[0].id == "1"
