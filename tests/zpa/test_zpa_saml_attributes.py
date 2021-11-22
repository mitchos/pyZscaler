import pytest
import responses
from box import Box, BoxList

from tests.conftest import stub_sleep


# Don't need to test the data structure as we just have list and get
# methods available. id will suffice until add/update endpoints are available.
@pytest.fixture(name="saml_attributes")
def fixture_saml_attributes():
    return {"totalPages": 1, "list": [{"id": "1"}, {"id": "2"}]}


@responses.activate
@stub_sleep
def test_list_saml_attributes(zpa, saml_attributes):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v2/admin/customers/1/samlAttribute?page=1",
        json=saml_attributes,
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v2/admin/customers/1/samlAttribute?page=2",
        json=[],
        status=200,
    )
    resp = zpa.saml_attributes.list_attributes()
    assert isinstance(resp, BoxList)
    assert len(resp) == 2
    assert resp[0].id == "1"


@responses.activate
@stub_sleep
def test_list_saml_attributes_by_idp(zpa, saml_attributes):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v2/admin/customers/1/samlAttribute/idp/1?page=1",
        json=saml_attributes,
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v2/admin/customers/1/samlAttribute/idp/1?page=2",
        json=[],
        status=200,
    )
    resp = zpa.saml_attributes.list_attributes_by_idp("1")
    assert isinstance(resp, BoxList)
    assert len(resp) == 2
    assert resp[0].id == "1"


@responses.activate
def test_get_saml_attribute(zpa, saml_attributes):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/samlAttribute/1",
        json=saml_attributes["list"][0],
        status=200,
    )
    resp = zpa.saml_attributes.get_attribute("1")
    assert isinstance(resp, Box)
    assert resp.id == "1"
