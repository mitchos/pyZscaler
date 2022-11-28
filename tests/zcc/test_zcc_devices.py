import pytest
import responses
from box import BoxList

from tests.conftest import stub_sleep


@pytest.fixture(name="devices")
def fixture_devices():
    return [{"id": 1}, {"id": 2}]


@responses.activate
@stub_sleep
def test_list_devices(devices, zcc):
    responses.add(
        method="GET",
        url="https://api-mobile.zscaler.net/papi/public/v1/getDevices?osType=3&pageSize=1&page=1",
        json=devices,
        status=200,
    )
    responses.add(
        method="GET",
        url="https://api-mobile.zscaler.net/papi/public/v1/getDevices?osType=3&pageSize=1&page=2",
        json=[],
        status=200,
    )
    resp = zcc.devices.list_devices(os_type="windows", page_size=1)

    assert isinstance(resp, BoxList)
    assert resp[0].id == 1
