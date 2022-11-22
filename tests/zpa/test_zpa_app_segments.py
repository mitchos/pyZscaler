import copy

import pytest
import responses
from box import Box, BoxList
from responses import matchers

from tests.conftest import stub_sleep


@pytest.fixture(name="app_segments")
def fixture_app_segments():
    return {
        "totalPages": 1,
        "list": [
            {
                "creationTime": "1628211456",
                "modifiedBy": "1",
                "id": "1",
                "domainNames": ["www.example.com"],
                "name": "Test A",
                "description": "Test",
                "serverGroups": [
                    {
                        "id": "1",
                        "creationTime": "1625698796",
                        "modifiedBy": "1",
                        "name": "Test",
                        "enabled": True,
                        "configSpace": "DEFAULT",
                        "dynamicDiscovery": False,
                    }
                ],
                "enabled": True,
                "passiveHealthEnabled": True,
                "tcpPortRanges": ["443", "443", "80", "80"],
                "tcpPortRange": [{"from": "443", "to": "443"}, {"from": "80", "to": "80"}],
                "doubleEncrypt": False,
                "configSpace": "DEFAULT",
                "bypassType": "NEVER",
                "healthCheckType": "DEFAULT",
                "icmpAccessType": "NONE",
                "isCnameEnabled": True,
                "ipAnchored": False,
                "healthReporting": "ON_ACCESS",
                "segmentGroupId": "1",
                "segmentGroupName": "Test",
            },
            {
                "creationTime": "1628211456",
                "modifiedBy": "1",
                "id": "2",
                "domainNames": ["test.example.com"],
                "name": "Test B",
                "description": "Test",
                "serverGroups": [
                    {
                        "id": "1",
                        "creationTime": "1625698796",
                        "modifiedBy": "1",
                        "name": "Test",
                        "enabled": True,
                        "configSpace": "DEFAULT",
                        "dynamicDiscovery": False,
                    }
                ],
                "enabled": True,
                "passiveHealthEnabled": True,
                "tcpPortRanges": ["443", "443", "80", "80"],
                "tcpPortRange": [{"from": "443", "to": "443"}, {"from": "80", "to": "80"}],
                "doubleEncrypt": False,
                "configSpace": "DEFAULT",
                "bypassType": "NEVER",
                "healthCheckType": "DEFAULT",
                "icmpAccessType": "NONE",
                "isCnameEnabled": True,
                "ipAnchored": False,
                "healthReporting": "ON_ACCESS",
                "segmentGroupId": "1",
                "segmentGroupName": "Test",
            },
        ],
    }


@responses.activate
@stub_sleep
def test_list_segments(zpa, app_segments):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/application?page=1",
        json=app_segments,
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/application?page=2",
        json=[],
        status=200,
    )
    resp = zpa.app_segments.list_segments()
    assert isinstance(resp, BoxList)
    assert len(resp) == 2
    assert resp[0].id == "1"


@responses.activate
def test_get_segment(zpa, app_segments):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/application/1",
        json=app_segments["list"][0],
        status=200,
    )
    resp = zpa.app_segments.get_segment("1")
    assert isinstance(resp, Box)
    assert resp.id == "1"


@responses.activate
def test_delete_segment(zpa, app_segments):
    responses.add(
        responses.DELETE,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/application/1",
        status=204,
    )
    resp = zpa.app_segments.delete_segment("1")
    assert resp == 204


@responses.activate
def test_delete_segment_force(zpa, app_segments):
    responses.add(
        responses.DELETE,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/application/1?forceDelete=True",
        status=204,
    )
    resp = zpa.app_segments.delete_segment("1", force_delete=True)
    assert resp == 204


@responses.activate
def test_add_segment(zpa, app_segments):
    responses.add(
        responses.POST,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/application",
        json=app_segments["list"][0],
        status=200,
        match=[
            matchers.json_params_matcher(
                {
                    "name": "Test",
                    "domainNames": ["www.example.com", "test.example.com"],
                    "segmentGroupId": "1",
                    "serverGroups": [{"id": "1"}, {"id": "2"}],
                    "tcpPortRanges": ["443", "443", "80", "80"],
                    "udpPortRanges": ["443", "443", "80", "80"],
                    "description": "test",
                }
            )
        ],
    )
    resp = zpa.app_segments.add_segment(
        name="Test",
        domain_names=["www.example.com", "test.example.com"],
        segment_group_id="1",
        server_group_ids=["1", "2"],
        tcp_ports=["443", "443", "80", "80"],
        udp_ports=["443", "443", "80", "80"],
        description="test",
    )

    assert isinstance(resp, Box)
    assert resp.id == "1"


@responses.activate
def test_update_segment(zpa, app_segments):
    updated_segment = copy.deepcopy(app_segments["list"][0])
    updated_segment["name"] = "Test Updated"
    updated_segment["clientlessApps"] = [{"id": "1"}, {"id": "2"}]
    updated_segment["tcpPortRange"] = [{"from": "80", "to": "81"}]
    updated_segment["udpPortRange"] = [{"from": "5000", "to": "5005"}]

    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/application/1",
        json=app_segments["list"][0],
        status=200,
    )

    responses.add(
        responses.PUT,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/application/1",
        status=204,
        match=[matchers.json_params_matcher(updated_segment)],
    )

    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/application/1",
        json=updated_segment,
        status=200,
    )
    resp = zpa.app_segments.update_segment(
        "1", name="Test Updated", clientless_app_ids=["1", "2"], tcp_ports=[("80", "81")], udp_ports=[("5000", "5005")]
    )

    assert isinstance(resp, Box)
    assert resp.name == updated_segment["name"]
    assert resp.clientless_apps == updated_segment["clientlessApps"]
