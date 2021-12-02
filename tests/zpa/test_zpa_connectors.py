import pytest
import responses
from box import Box, BoxList
from responses import matchers

from tests.conftest import stub_sleep


@pytest.fixture(name="app_connectors")
def fixture_app_connectors():
    return {
        "totalPages": 1,
        "list": [
            {
                "id": "1",
                "modifiedTime": "1636691900",
                "creationTime": "1623442121",
                "modifiedBy": "1",
                "name": "TEST-A",
                "fingerprint": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx=",
                "issuedCertId": "1",
                "enabled": False,
                "expectedVersion": "1.1.1",
                "currentVersion": "1.1.1",
                "previousVersion": "1.1.1",
                "lastUpgradeTime": "1636293669",
                "upgradeStatus": "COMPLETE",
                "controlChannelStatus": "ZPN_STATUS_AUTHENTICATED",
                "upgradeAttempt": "0",
                "ctrlBrokerName": "TEST",
                "lastBrokerConnectTime": "1637086569",
                "lastBrokerConnectTimeDuration": "01d 01h 01m 01s",
                "sargeVersion": "1.1.1",
                "lastBrokerDisconnectTime": "1636488462",
                "lastBrokerDisconnectTimeDuration": "01d 01h 01m 01s",
                "privateIp": "1.1.1.1",
                "publicIp": "1.1.1.1",
                "platform": "el7",
                "applicationStartTime": "1636293669",
                "latitude": "1.0",
                "longitude": "1.0",
                "location": "Sydney, Australia",
                "provisioningKeyId": "1",
                "provisioningKeyName": "TEST",
                "enrollmentCert": {"id": "1", "name": "Test"},
                "appConnectorGroupId": "1",
                "appConnectorGroupName": "Test",
            },
            {
                "id": "2",
                "modifiedTime": "1636691900",
                "creationTime": "1623442121",
                "modifiedBy": "1",
                "name": "TEST-B",
                "fingerprint": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx=",
                "issuedCertId": "1",
                "enabled": False,
                "expectedVersion": "1.1.1",
                "currentVersion": "1.1.1",
                "previousVersion": "1.1.1",
                "lastUpgradeTime": "1636293669",
                "upgradeStatus": "COMPLETE",
                "controlChannelStatus": "ZPN_STATUS_AUTHENTICATED",
                "upgradeAttempt": "0",
                "ctrlBrokerName": "TEST",
                "lastBrokerConnectTime": "1637086569",
                "lastBrokerConnectTimeDuration": "01d 01h 01m 01s",
                "sargeVersion": "1.1.1",
                "lastBrokerDisconnectTime": "1636488462",
                "lastBrokerDisconnectTimeDuration": "01d 01h 01m 01s",
                "privateIp": "1.1.1.1",
                "publicIp": "1.1.1.1",
                "platform": "el7",
                "applicationStartTime": "1636293669",
                "latitude": "1.0",
                "longitude": "1.0",
                "location": "Sydney, Australia",
                "provisioningKeyId": "1",
                "provisioningKeyName": "TEST",
                "enrollmentCert": {"id": "1", "name": "Test"},
                "appConnectorGroupId": "1",
                "appConnectorGroupName": "Test",
            },
        ],
    }


@pytest.fixture(name="app_connector_groups")
def fixture_app_connector_groups():
    return {
        "list": [
            {
                "id": "1",
                "creationTime": "1623889185",
                "modifiedBy": "1",
                "name": "Test",
                "enabled": True,
                "versionProfileId": "1",
                "overrideVersionProfile": True,
                "versionProfileName": "Previous Default",
                "versionProfileVisibilityScope": "ALL",
                "upgradeTimeInSecs": "50400",
                "upgradeDay": "SUNDAY",
                "location": "Sydney",
                "latitude": "1.0",
                "longitude": "1.0",
                "dnsQueryType": "IPV4_IPV6",
                "cityCountry": "Sydney, AU",
                "countryCode": "AU",
                "connectors": [
                    {
                        "id": "1",
                        "modifiedTime": "1623890719",
                        "creationTime": "1623890719",
                        "modifiedBy": "1",
                        "name": "Test",
                        "fingerprint": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx=",
                        "issuedCertId": "1",
                        "enabled": True,
                        "assistantVersion": {
                            "id": "1",
                            "modifiedTime": "1628887775",
                            "creationTime": "1623890722",
                            "modifiedBy": "1",
                            "expectedVersion": "11.111.1",
                            "currentVersion": "11.111.1",
                            "systemStartTime": "1628851547",
                            "applicationStartTime": "1623890722",
                            "lastBrokerConnectTime": "1628887123253882",
                            "lastBrokerDisconnectTime": "1628887775472165",
                            "brokerId": "1",
                            "restartTimeInSec": "1629036000",
                            "platform": "el7",
                            "upgradeStatus": "IN_PROGRESS",
                            "ctrlChannelStatus": "ZPN_STATUS_DISCONNECTED",
                            "latitude": "1.0",
                            "longitude": "1.0",
                            "privateIp": "1.1.1.1",
                            "publicIp": "1.1.1.1",
                            "loneWarrior": True,
                            "mtunnelId": "xxyyzz",
                            "upgradeAttempt": "1",
                            "appConnectorGroupId": "1",
                        },
                        "upgradeAttempt": "0",
                        "provisioningKeyId": "1",
                    }
                ],
                "lssAppConnectorGroup": False,
            },
            {
                "id": "2",
                "creationTime": "1623889185",
                "modifiedBy": "1",
                "name": "Test",
                "enabled": True,
                "versionProfileId": "0",
                "overrideVersionProfile": False,
                "versionProfileName": "Default",
                "versionProfileVisibilityScope": "ALL",
                "upgradeTimeInSecs": "50400",
                "upgradeDay": "SUNDAY",
                "location": "Sydney",
                "latitude": "1.0",
                "longitude": "1.0",
                "dnsQueryType": "IPV4_IPV6",
                "cityCountry": "Sydney, AU",
                "countryCode": "AU",
                "connectors": [
                    {
                        "id": "1",
                        "modifiedTime": "1623890719",
                        "creationTime": "1623890719",
                        "modifiedBy": "1",
                        "name": "Test",
                        "fingerprint": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx=",
                        "issuedCertId": "1",
                        "enabled": True,
                        "assistantVersion": {
                            "id": "1",
                            "modifiedTime": "1628887775",
                            "creationTime": "1623890722",
                            "modifiedBy": "1",
                            "expectedVersion": "11.111.1",
                            "currentVersion": "11.111.1",
                            "systemStartTime": "1628851547",
                            "applicationStartTime": "1623890722",
                            "lastBrokerConnectTime": "1628887123253882",
                            "lastBrokerDisconnectTime": "1628887775472165",
                            "brokerId": "1",
                            "restartTimeInSec": "1629036000",
                            "platform": "el7",
                            "upgradeStatus": "IN_PROGRESS",
                            "ctrlChannelStatus": "ZPN_STATUS_DISCONNECTED",
                            "latitude": "1.0",
                            "longitude": "1.0",
                            "privateIp": "1.1.1.1",
                            "publicIp": "1.1.1.1",
                            "loneWarrior": True,
                            "mtunnelId": "xxyyzz",
                            "upgradeAttempt": "1",
                            "appConnectorGroupId": "1",
                        },
                        "upgradeAttempt": "0",
                        "provisioningKeyId": "1",
                    }
                ],
                "lssAppConnectorGroup": False,
            },
        ]
    }


@responses.activate
@stub_sleep
def test_list_connectors(zpa, app_connectors):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/connector?page=1",
        json=app_connectors,
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/connector?page=2",
        json=[],
        status=200,
    )
    resp = zpa.connectors.list_connectors()
    assert isinstance(resp, BoxList)
    assert len(resp) == 2
    assert resp[0].id == "1"


@responses.activate
def test_get_connector(zpa, app_connectors):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/connector/1",
        json=app_connectors["list"][0],
        status=200,
    )
    resp = zpa.connectors.get_connector("1")
    assert isinstance(resp, Box)
    assert resp.id == "1"


@responses.activate
def test_update_connector(zpa, app_connectors):
    updated_connector = app_connectors["list"][0]
    updated_connector["name"] = "Updated Test"
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/connector/1",
        json=app_connectors["list"][0],
        status=200,
    )
    responses.add(
        responses.PUT,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/connector/1",
        status=204,
        match=[matchers.json_params_matcher(updated_connector)],
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/connector/1",
        json=updated_connector,
        status=200,
    )
    resp = zpa.connectors.update_connector("1", name="Updated Test")
    assert isinstance(resp, Box)
    assert resp.id == "1"
    assert resp.name == updated_connector["name"]


@responses.activate
def test_delete_connector(zpa):
    responses.add(
        responses.DELETE,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/connector/1",
        status=204,
    )
    resp = zpa.connectors.delete_connector("1")
    assert resp == 204


@responses.activate
def test_bulk_delete_connectors(zpa):
    responses.add(
        responses.POST,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/connector/bulkDelete",
        status=204,
        match=[matchers.json_params_matcher({"ids": ["1", "2"]})],
    )
    resp = zpa.connectors.bulk_delete_connectors(["1", "2"])
    assert isinstance(resp, int)
    assert resp == 204


@responses.activate
@stub_sleep
def test_list_connector_groups(zpa, app_connector_groups):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/appConnectorGroup?page=1",
        json=app_connector_groups,
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/appConnectorGroup?page=2",
        json=[],
        status=200,
    )
    resp = zpa.connectors.list_connector_groups()
    assert isinstance(resp, BoxList)
    assert len(resp) == 2
    assert resp[0].id == "1"


@responses.activate
def test_get_connector_group(zpa, app_connector_groups):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/appConnectorGroup/1",
        json=app_connector_groups["list"][0],
        status=200,
    )
    resp = zpa.connectors.get_connector_group("1")
    assert isinstance(resp, Box)
    assert resp.id == "1"


@responses.activate
def test_add_connector_group(zpa, app_connector_groups):
    responses.add(
        responses.POST,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/appConnectorGroup",
        status=204,
        json=app_connector_groups["list"][0],
        match=[
            matchers.json_params_matcher(
                {
                    "name": "Test",
                    "latitude": "1.0",
                    "longitude": "1.0",
                    "location": "Test",
                    "connectors": [{"id": "1"}, {"id": "2"}],
                    "serverGroups": [{"id": "1"}, {"id": "2"}],
                    "versionProfileId": 0,
                    "overrideVersionProfile": True,
                    "description": "Test",
                }
            )
        ],
    )
    resp = zpa.connectors.add_connector_group(
        name="Test",
        description="Test",
        latitude="1.0",
        longitude="1.0",
        location="Test",
        connector_ids=["1", "2"],
        server_group_ids=["1", "2"],
        version_profile="default",
    )

    assert isinstance(resp, Box)
    assert resp.name == "Test"


@responses.activate
def test_update_connector_group(zpa, app_connector_groups):
    updated_group = app_connector_groups["list"][0]
    updated_group["name"] = "Updated Test"
    updated_group["connectors"] = [{"id": "3"}]
    updated_group["serverGroups"] = [{"id": "3"}]
    updated_group["versionProfileId"] = 1

    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/appConnectorGroup/1",
        json=app_connector_groups["list"][0],
        status=200,
    )

    responses.add(
        responses.PUT,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/appConnectorGroup/1",
        status=204,
        match=[matchers.json_params_matcher(updated_group)],
    )

    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/appConnectorGroup/1",
        json=updated_group,
        status=200,
    )

    resp = zpa.connectors.update_connector_group(
        "1", name="Updated Test", connector_ids=["3"], server_group_ids=["3"], version_profile="previous_default"
    )

    assert isinstance(resp, Box)
    assert resp.name == updated_group["name"]
    assert resp.connectors == updated_group["connectors"]
    assert resp.server_groups == updated_group["serverGroups"]
    assert resp.version_profile_id == updated_group["versionProfileId"]


@responses.activate
def test_delete_connector_group(zpa):
    responses.add(
        responses.DELETE,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/appConnectorGroup/1",
        status=204,
    )
    resp = zpa.connectors.delete_connector_group("1")
    assert resp == 204
