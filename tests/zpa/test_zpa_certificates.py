import pytest
import responses
from box import Box, BoxList
from responses import matchers

from tests.conftest import stub_sleep


# Don't need to test the data structure as we just have list and get
# methods available. id will suffice until add/update endpoints are available.
@pytest.fixture(name="certificates")
def fixture_certificates():
    return {
        "totalPages": "1",
        "totalCount": "2",
        "list": [
            {
                "id": "1",
                "modifiedTime": "1706961016",
                "creationTime": "1706961016",
                "modifiedBy": "1",
                "name": "Test 1",
                "description": "Test Certificate 1",
                "cName": "*.example.com",
                "validFromInEpochSec": "1706830039",
                "validToInEpochSec": "1714606038",
                "certificate": "-----BEGIN CERTIFICATE-----\n-----END CERTIFICATE-----\n",
                "issuedTo": "CN=*.example.com",
                "issuedBy": "CN=R3,O=Let's Encrypt,C=US",
                "serialNo": "1",
                "publicKey": "-----BEGIN PUBLIC KEY-----\n-----END PUBLIC KEY-----\n",
                "certChain": "-----BEGIN CERTIFICATE-----\n-----END CERTIFICATE-----\n",
                "san": [
                    "*.example.com"
                ]
                },
            {
                "id": "2",
                "modifiedTime": "1706961016",
                "creationTime": "1706961016",
                "modifiedBy": "1",
                "name": "Test 2",
                "description": "Test Certificate 2",
                "cName": "www.example.com",
                "validFromInEpochSec": "1706830039",
                "validToInEpochSec": "1714606038",
                "certificate": "-----BEGIN CERTIFICATE-----\n-----END CERTIFICATE-----\n",
                "issuedTo": "CN=www.example.com",
                "issuedBy": "CN=R3,O=Let's Encrypt,C=US",
                "serialNo": "1",
                "publicKey": "-----BEGIN PUBLIC KEY-----\n-----END PUBLIC KEY-----\n",
                "certChain": "-----BEGIN CERTIFICATE-----\n-----END CERTIFICATE-----\n",
                "san": [
                    "www.example.com"
                ]
                }
            ]
        }


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

@responses.activate
def test_add_certificate(zpa, certificates):
    responses.add(
        responses.POST,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/certificate",
        json=certificates["list"][0],
        status=200,
        match=[
            matchers.json_params_matcher(
                {
                "certBlob": "-----BEGIN CERTIFICATE-----\n-----END PRIVATE KEY-----",
                "description": "Test Certificate 1",
                "name": "Test 1"
                }
                )
            ],
        )
    resp = zpa.certificates.add_certificate(
        name="Test 1",
        cert_blob="-----BEGIN CERTIFICATE-----\n-----END PRIVATE KEY-----",
        description="Test Certificate 1"
    )

    assert isinstance(resp, Box)
    assert resp.id == "1"