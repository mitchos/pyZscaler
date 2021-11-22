import pytest
import responses
from box import Box, BoxList

from tests.conftest import stub_sleep


# Don't need to test the data structure as we just have list and get
# methods available. id will suffice until add/update endpoints are available.
@pytest.fixture(name="certificates")
def fixture_certificates():
    return {"totalPages": 1, "list": [{"id": "1"}, {"id": "2"}]}


@responses.activate
@stub_sleep
def test_list_browser_access(zpa, certificates):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v2/admin/customers/1/clientlessCertificate/issued?page=1",
        json=certificates,
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v2/admin/customers/1/clientlessCertificate/issued?page=2",
        json=[],
        status=200,
    )
    resp = zpa.certificates.list_browser_access()
    assert isinstance(resp, BoxList)
    assert len(resp) == 2
    assert resp[0].id == "1"


@responses.activate
def test_get_browser_access(zpa, certificates):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/clientlessCertificate/1",
        json=certificates["list"][0],
        status=200,
    )
    resp = zpa.certificates.get_browser_access("1")
    assert isinstance(resp, Box)
    assert resp.id == "1"


@responses.activate
@stub_sleep
def test_list_enrolment(zpa, certificates):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v2/admin/customers/1/enrollmentCert?page=1",
        json=certificates,
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v2/admin/customers/1/enrollmentCert?page=2",
        json=[],
        status=200,
    )
    resp = zpa.certificates.list_enrolment()
    assert isinstance(resp, BoxList)
    assert len(resp) == 2
    assert resp[0].id == "1"


@responses.activate
def test_get_enrolment(zpa, certificates):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/enrollmentCert/1",
        json=certificates["list"][0],
        status=200,
    )
    resp = zpa.certificates.get_enrolment("1")
    assert isinstance(resp, Box)
    assert resp.id == "1"
