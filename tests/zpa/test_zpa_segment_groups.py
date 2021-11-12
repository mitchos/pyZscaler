import pytest
import responses
from box import Box, BoxList
from responses import matchers

from tests.conftest import stub_sleep


@pytest.fixture(name="segment_groups")
def fixture_segment_groups():
    return {
        "totalPages": 1,
        "list": [
            {
                "id": "1",
                "creationTime": "1623895870",
                "modifiedBy": "1",
                "name": "Test A",
                "description": "Test",
                "enabled": True,
                "applications": [
                    {
                        "id": "1",
                        "creationTime": "1623895870",
                        "modifiedBy": "1",
                        "name": "Test",
                        "domainName": "test.example.com",
                        "domainNames": ["test.example.com"],
                        "description": "Test",
                        "enabled": True,
                        "passiveHealthEnabled": True,
                        "tcpPortRanges": ["80", "80", "443", "443"],
                        "doubleEncrypt": False,
                        "healthCheckType": "DEFAULT",
                        "icmpAccessType": "NONE",
                        "bypassType": "NEVER",
                        "configSpace": "DEFAULT",
                        "ipAnchored": False,
                        "tcpPortRange": [{"from": "80", "to": "80"}, {"from": "443", "to": "443"}],
                    }
                ],
                "policyMigrated": True,
                "configSpace": "DEFAULT",
                "tcpKeepAliveEnabled": "0",
            },
            {
                "id": "2",
                "creationTime": "1623895870",
                "modifiedBy": "1",
                "name": "Test B",
                "description": "Test",
                "enabled": True,
                "applications": [
                    {
                        "id": "1",
                        "creationTime": "1623895870",
                        "modifiedBy": "1",
                        "name": "Test",
                        "domainName": "test.example.com",
                        "domainNames": ["test.example.com"],
                        "description": "Test",
                        "enabled": True,
                        "passiveHealthEnabled": True,
                        "tcpPortRanges": ["80", "80", "443", "443"],
                        "doubleEncrypt": False,
                        "healthCheckType": "DEFAULT",
                        "icmpAccessType": "NONE",
                        "bypassType": "NEVER",
                        "configSpace": "DEFAULT",
                        "ipAnchored": False,
                        "tcpPortRange": [{"from": "80", "to": "80"}, {"from": "443", "to": "443"}],
                    }
                ],
                "policyMigrated": True,
                "configSpace": "DEFAULT",
                "tcpKeepAliveEnabled": "0",
            },
        ],
    }


@responses.activate
@stub_sleep
def test_list_groups(zpa, segment_groups):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/segmentGroup?page=1",
        json=segment_groups,
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/segmentGroup?page=2",
        json=[],
        status=200,
    )
    resp = zpa.segment_groups.list_groups()
    assert isinstance(resp, BoxList)
    assert len(resp) == 2
    assert resp[0].id == "1"


@responses.activate
def test_get_group(zpa, segment_groups):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/segmentGroup/1",
        json=segment_groups["list"][0],
        status=200,
    )
    resp = zpa.segment_groups.get_group("1")
    assert isinstance(resp, Box)
    assert resp.id == "1"


@responses.activate
def test_delete_group(zpa):
    responses.add(
        responses.DELETE,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/segmentGroup/1",
        status=204,
    )
    resp = zpa.segment_groups.delete_group("1")
    assert resp == 204


@responses.activate
def test_add_group(zpa, segment_groups):
    responses.add(
        responses.POST,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/segmentGroup",
        json=segment_groups["list"][0],
        status=200,
        match=[
            matchers.json_params_matcher(
                {
                    "name": "Test",
                    "enabled": True,
                    "applications": [{"id": "1"}],
                    "description": "Test",
                }
            )
        ],
    )
    resp = zpa.segment_groups.add_group(
        name="Test",
        enabled=True,
        application_ids=["1"],
        description="Test",
    )

    assert isinstance(resp, Box)
    assert resp.id == "1"
    assert resp.applications[0].id == "1"


@responses.activate
def test_update_group(zpa, segment_groups):
    updated_group = segment_groups["list"][0]
    updated_group["name"] = "Test Updated"
    updated_group["applications"] = [{"id": "2"}]
    updated_group["description"] = "Test Updated"

    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/segmentGroup/1",
        json=segment_groups["list"][0],
        status=200,
    )

    responses.add(
        responses.PUT,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/segmentGroup/1",
        json=updated_group,
        status=204,
        match=[matchers.json_params_matcher(updated_group)],
    )
    resp = zpa.segment_groups.update_group(
        "1",
        name="Test Updated",
        application_ids=["2"],
        description="Test Updated",
    )

    assert isinstance(resp, Box)
    assert resp.id == "1"
    assert resp.name == updated_group["name"]
    assert resp.applications[0].id == "2"
    assert resp.description == updated_group["description"]
