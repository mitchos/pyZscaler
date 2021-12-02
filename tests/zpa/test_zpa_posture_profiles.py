import pytest
import responses
from box import Box, BoxList

from tests.conftest import stub_sleep


# Don't need to test the data structure as we just have list and get
# methods available. id will suffice until add/update endpoints are available.
@pytest.fixture(name="posture_profiles")
def fixture_posture_profiles():
    return {"totalPages": 1, "list": [{"id": "1"}, {"id": "2"}]}


@responses.activate
@stub_sleep
def test_list_posture_profiles(zpa, posture_profiles):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v2/admin/customers/1/posture?page=1",
        json=posture_profiles,
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v2/admin/customers/1/posture?page=2",
        json=[],
        status=200,
    )
    resp = zpa.posture_profiles.list_profiles()
    assert isinstance(resp, BoxList)
    assert len(resp) == 2
    assert resp[0].id == "1"


@responses.activate
def test_get_posture_profiles(zpa, posture_profiles):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/posture/1",
        json=posture_profiles["list"][0],
        status=200,
    )
    resp = zpa.posture_profiles.get_profile("1")
    assert isinstance(resp, Box)
    assert resp.id == "1"
