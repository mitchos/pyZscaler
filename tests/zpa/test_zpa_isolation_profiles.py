import pytest
import responses
from box import BoxList

from tests.conftest import stub_sleep


# Don't need to test the data structure as we just have list and get
# methods available. id will suffice until add/update endpoints are available.
@pytest.fixture(name="isolation_profiles")
def fixture_isolation_profiles():
    return {"totalPages": 1, "list": [{"id": "1"}, {"id": "2"}]}


@responses.activate
@stub_sleep
def test_list_isolation_profiles(zpa, isolation_profiles):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/isolation/profiles?page=1",
        json=isolation_profiles,
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/isolation/profiles?page=2",
        json=[],
        status=200,
    )
    resp = zpa.isolation_profiles.list_profiles()
    assert isinstance(resp, BoxList)
    assert len(resp) == 2
    assert resp[0].id == "1"
