import pytest
import responses
from box import Box, BoxList
from responses import matchers

from tests.conftest import stub_sleep


@pytest.fixture(name="lss_config")
def fixture_lss_configs():
    return {
        "totalPages": 1,
        "list": [
            {
                "config": {
                    "name": "test",
                    "lssHost": "1.1.1.1",
                    "lssPort": "80",
                    "enabled": True,
                    "format": "log_stream_content",
                    "sourceLogType": "zpn_trans_log",
                    "useTls": False,
                    "filter": [
                        "Authentication failed",
                    ],
                },
                "connectorGroups": [{"id": "1"}],
                "policyRuleResource": {
                    "conditions": [
                        {"operands": [{"objectType": "IDP", "values": ["1"]}]},
                        {"operands": [{"objectType": "CLIENT_TYPE", "values": ["zpn_client_type_edge_connector"]}]},
                        {"operands": [{"objectType": "APP", "values": ["1"]}]},
                        {"operands": [{"objectType": "APP_GROUP", "values": ["1"]}]},
                        {
                            "operands": [
                                {
                                    "objectType": "SAML",
                                    "entryValues": [
                                        {"lhs": "1", "rhs": "test_1"},
                                        {"lhs": "2", "rhs": "test_2"},
                                    ],
                                }
                            ]
                        },
                    ],
                    "name": "test_policy",
                },
                "auditMessage": "blank",
                "policyName": "test_policy",
            },
            {"id": "2"},
        ],
    }


@pytest.fixture(name="lss_client_types")
def fixture_lss_client_types():
    return {
        "zpn_client_type_edge_connector": "Cloud Connector",
    }


@pytest.fixture(name="lss_log_format")
def fixture_lss_log_formats():
    return {
        "zpn_auth_log": {
            "csv": "log_stream_content",
            "json": "log_stream_content",
            "tsv": "log_stream_content",
        },
        "zpn_trans_log": {
            "csv": "log_stream_content",
            "json": "log_stream_content",
            "tsv": "log_stream_content",
        },
    }


@pytest.fixture(name="lss_status_codes")
def fixture_lss_status_codes():
    return {
        "zpn_auth_log": {
            "zpn_status_auth_failed": {
                "error_type": "NA",
                "name": "Authentication failed",
                "admin_action": "NA",
                "status": "Error",
            },
        }
    }


@responses.activate
@stub_sleep
def test_list_lss_configs(zpa, lss_config):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v2/admin/customers/1/lssConfig?page=1",
        json=lss_config,
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v2/admin/customers/1/lssConfig?page=2",
        json=[],
        status=200,
    )
    resp = zpa.lss.list_configs()
    assert isinstance(resp, BoxList)
    assert len(resp) == 2
    assert resp[0].config.name == "test"


@responses.activate
def test_get_lss_config(zpa, lss_config):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v2/admin/customers/1/lssConfig/1",
        json=lss_config["list"][0],
        status=200,
    )
    resp = zpa.lss.get_config("1")
    assert isinstance(resp, Box)
    assert resp.config.name == "test"


@responses.activate
def test_get_lss_log_formats(zpa, lss_log_format):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v2/admin/lssConfig/logType/formats",
        json=lss_log_format,
        status=200,
    )
    resp = zpa.lss.get_log_formats()
    assert isinstance(resp, Box)
    assert resp.zpn_auth_log.csv == "log_stream_content"


@responses.activate
def test_get_lss_client_types(zpa, lss_client_types):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v2/admin/lssConfig/clientTypes",
        json=lss_client_types,
        status=200,
    )
    resp = zpa.lss.get_client_types()
    assert isinstance(resp, Box)
    assert resp.cloud_connector == "zpn_client_type_edge_connector"


@responses.activate
def test_get_lss_session_status_codes(zpa, lss_status_codes):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v2/admin/lssConfig/statusCodes",
        json=lss_status_codes,
        status=200,
    )
    resp = zpa.lss.get_status_codes()
    assert isinstance(resp, Box)
    assert resp.zpn_auth_log.zpn_status_auth_failed.name == "Authentication failed"


@responses.activate
def test_get_lss_session_status_codes_with_log_type(zpa, lss_status_codes):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v2/admin/lssConfig/statusCodes",
        json=lss_status_codes,
        status=200,
    )
    resp = zpa.lss.get_status_codes("user_status")
    assert isinstance(resp, Box)
    assert resp.zpn_status_auth_failed.name == "Authentication failed"


@responses.activate
def test_get_lss_session_status_codes_valueerror(zpa, lss_status_codes):
    with pytest.raises(Exception) as e_info:
        resp = zpa.lss.get_status_codes("error")


@responses.activate
def test_delete_lss_config(zpa):
    responses.add(
        responses.DELETE,
        url="https://config.private.zscaler.com/mgmtconfig/v2/admin/customers/1/lssConfig/1",
        status=204,
    )
    resp = zpa.lss.delete_lss_config("1")
    assert isinstance(resp, int)
    assert resp == 204


@responses.activate
def test_add_lss_config(zpa, lss_config, lss_log_format, lss_client_types):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v2/admin/lssConfig/logType/formats",
        json=lss_log_format,
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v2/admin/lssConfig/clientTypes",
        json=lss_client_types,
        status=200,
    )
    responses.add(
        responses.POST,
        url="https://config.private.zscaler.com/mgmtconfig/v2/admin/customers/1/lssConfig",
        json=lss_config["list"][0],
        status=200,
        match=[matchers.json_params_matcher(lss_config["list"][0])],
    )
    resp = zpa.lss.add_lss_config(
        name="test",
        app_connector_group_ids=["1"],
        lss_host="1.1.1.1",
        lss_port="80",
        audit_message="blank",
        source_log_type="user_activity",
        filter_status_codes=["Authentication failed"],
        policy_rules=[
            ("idp", ["1"]),
            ("client_type", ["cloud_connector"]),
            ("app", ["1"]),
            ("app_group", ["1"]),
            ("saml", [("1", "test_1"), ("2", "test_2")]),
        ],
        policy_name="test_policy",
    )

    assert isinstance(resp, Box)
    assert resp.config.name == "test"


@responses.activate
def test_add_lss_config_with_log_stream(zpa, lss_config, lss_log_format, lss_client_types):
    modified_config = lss_config["list"][0]
    modified_config["config"]["format"] = "test"

    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v2/admin/lssConfig/logType/formats",
        json=lss_log_format,
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v2/admin/lssConfig/clientTypes",
        json=lss_client_types,
        status=200,
    )
    responses.add(
        responses.POST,
        url="https://config.private.zscaler.com/mgmtconfig/v2/admin/customers/1/lssConfig",
        json=lss_config["list"][0],
        status=200,
        match=[matchers.json_params_matcher(modified_config)],
    )
    resp = zpa.lss.add_lss_config(
        name="test",
        app_connector_group_ids=["1"],
        lss_host="1.1.1.1",
        lss_port="80",
        audit_message="blank",
        log_stream_content="test",
        source_log_type="user_activity",
        filter_status_codes=["Authentication failed"],
        policy_rules=[
            ("idp", ["1"]),
            ("client_type", ["cloud_connector"]),
            ("app", ["1"]),
            ("app_group", ["1"]),
            ("saml", [("1", "test_1"), ("2", "test_2")]),
        ],
        policy_name="test_policy",
    )

    assert isinstance(resp, Box)
    assert resp.config.name == "test"


@responses.activate
def test_update_lss_config(zpa, lss_config, lss_log_format):
    updated_config = lss_config["list"][0]
    updated_config["config"]["name"] = "Test Updated"
    updated_config["description"] = "Update Description"
    updated_config["config"]["filter"] = ["CLT_INVALID_DOMAIN"]
    updated_config["config"]["sourceLogType"] = "zpn_auth_log"
    updated_config["policyRuleResource"] = {
        "name": "test_policy",
        "conditions": [{"operands": [{"objectType": "IDP", "values": ["2"]}]}],
    }

    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v2/admin/customers/1/lssConfig/1",
        json=lss_config["list"][0],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v2/admin/lssConfig/logType/formats",
        json=lss_log_format,
        status=200,
    )

    responses.add(
        responses.PUT,
        url="https://config.private.zscaler.com/mgmtconfig/v2/admin/customers/1/lssConfig/1",
        status=204,
        match=[matchers.json_params_matcher(updated_config)],
    )
    resp = zpa.lss.update_lss_config(
        "1",
        name="Test Updated",
        description="Update Description",
        filter_status_codes=["CLT_INVALID_DOMAIN"],
        policy_rules=[("idp", ["2"])],
        source_log_type="user_status",
        source_log_format="json",
    )

    assert isinstance(resp, Box)
    assert resp.config.name == updated_config["config"]["name"]
    assert resp.config.filter[0] == "CLT_INVALID_DOMAIN"
    assert resp.policy_rule_resource.conditions[0].operands[0]["values"][0] == "2"
