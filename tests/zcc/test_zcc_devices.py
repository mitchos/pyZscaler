import pytest
import responses
from box import BoxList
from responses import matchers


@pytest.fixture(name="devices")
def fixture_devices():
    return [{"id": 1}, {"id": 2}]


@responses.activate
def test_list_devices(devices, zcc):
    responses.add(
        method="GET",
        url="https://api-mobile.zscaler.net/papi/public/v1/getDevices",
        json=devices,
        match=[matchers.json_params_matcher({"companyId": "88888"})],
        status=200,
    )
    resp = zcc.devices.list_devices()

    assert isinstance(resp, BoxList)
    assert resp[0].id == 1
