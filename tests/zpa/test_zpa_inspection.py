import copy

import pytest
import responses
from box import Box, BoxList
from responses import matchers

from tests.conftest import stub_sleep


@pytest.fixture(name="predefined_controls")
def fixture_predefined_controls():
    return [
        {
            "controlGroup": "Test",
            "defaultGroup": True,
            "predefinedInspectionControls": [
                {
                    "id": "1",
                    "modifiedTime": "1631459708",
                    "creationTime": "1631459708",
                    "name": "Failed to parse request body",
                    "description": "Failed to parse request body",
                    "severity": "CRITICAL",
                    "controlNumber": "200002",
                    "version": "OWASP_CRS/3.3.0",
                    "paranoiaLevel": "1",
                    "defaultAction": "BLOCK",
                    "controlGroup": "Protocol Issues",
                }
            ],
        }
    ]


@pytest.fixture(name="custom_controls")
def fixture_custom_controls():
    return [
        {
            "id": "1",
            "creationTime": "1653536435",
            "modifiedBy": "1",
            "name": "test_a",
            "severity": "INFO",
            "controlNumber": "4500000",
            "version": "1.0",
            "paranoiaLevel": "1",
            "defaultAction": "BLOCK",
            "type": "REQUEST",
            "controlRuleJson": '[{"type":"REQUEST_HEADERS","names":["test"],'
            '"conditions":[{"lhs":"SIZE","op":"GE","rhs":"10"}]}]',
        },
        {
            "id": "2",
            "modifiedTime": "1653540825",
            "creationTime": "1653540245",
            "modifiedBy": "1",
            "name": "test_b",
            "description": "test_b",
            "severity": "INFO",
            "controlNumber": "4500001",
            "version": "1.0",
            "paranoiaLevel": "1",
            "defaultAction": "PASS",
            "type": "REQUEST",
            "controlRuleJson": '[{"type":"REQUEST_HEADERS","names":["test1"],'
            '"conditions":[{"lhs":"SIZE","op":"GE","rhs":"5"}]}]',
        },
    ]


@pytest.fixture(name="inspection_profiles")
def fixture_inspection_profiles():
    return [
        {
            "id": "1",
            "modifiedTime": "1651783897",
            "creationTime": "1651783897",
            "modifiedBy": "1",
            "name": "test_a",
            "paranoiaLevel": "1",
            "controlsInfo": [{"control_type": "PREDEFINED", "count": "6"}],
            "incarnationNumber": "1",
        },
        {
            "id": "2",
            "modifiedTime": "1651784355",
            "creationTime": "1651784355",
            "modifiedBy": "1",
            "name": "test_b",
            "paranoiaLevel": "2",
            "controlsInfo": [{"control_type": "PREDEFINED", "count": "7"}],
            "incarnationNumber": "1",
        },
        {
            "id": "3",
            "modifiedTime": "1657587062",
            "creationTime": "1657587062",
            "modifiedBy": "1",
            "name": "test_c",
            "paranoiaLevel": "2",
            "predefinedControlsVersion": "OWASP_CRS/3.3.0",
            "predefinedControls": [
                {
                    "id": "1",
                    "name": "Internal error flagged",
                    "description": "Internal error flagged",
                    "severity": "CRITICAL",
                    "version": "OWASP_CRS/3.3.0",
                    "action": "BLOCK",
                },
                {"id": "2", "action": "BLOCK"},
            ],
            "customControls": [{"id": "3", "action": "BLOCK"}],
            "incarnationNumber": "1",
        },
    ]


@responses.activate
def test_list_predef_control_versions(zpa):
    control_versions = ["OWASP_CRS/3.3.0"]
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/inspectionControls/predefined/versions",
        json=control_versions,
        status=200,
    )
    resp = zpa.inspection.list_predef_control_versions()
    assert isinstance(resp, BoxList)
    assert resp[0] == "OWASP_CRS/3.3.0"


@responses.activate
def test_list_predef_controls(zpa, predefined_controls):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/inspectionControls/predefined?version=test",  # noqa: E501
        json=predefined_controls,
        status=200,
        match=[matchers.query_param_matcher({"version": "test"})],
    )
    resp = zpa.inspection.list_predef_controls(version="test")
    assert isinstance(resp, BoxList)
    assert resp[0]["control_group"] == "Test"


@responses.activate
def test_list_predef_controls_search(zpa, predefined_controls):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/inspectionControls/predefined?version=test&search=test",  # noqa: E501
        json=predefined_controls,
        status=200,
        match=[
            matchers.query_param_matcher(
                {
                    "version": "test",
                    "search": "test",
                }
            )
        ],
    )
    resp = zpa.inspection.list_predef_controls(version="test", search="test")
    assert isinstance(resp, BoxList)
    assert resp[0]["control_group"] == "Test"


@responses.activate
def test_list_control_types(zpa):
    control_types = ["CUSTOM", "PREDEFINED", "ZSCALER"]
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/inspectionControls/controlTypes",
        json=control_types,
        status=200,
    )
    resp = zpa.inspection.list_control_types()
    assert isinstance(resp, BoxList)
    assert resp[0] == "CUSTOM"


@responses.activate
def test_list_custom_control_types(zpa):
    control_types = {
        "request": ["REQUEST_HEADERS", "REQUEST_COOKIES", "REQUEST_URI", "REQUEST_METHOD", "REQUEST_BODY", "QUERY_STRING"],
        "response": ["RESPONSE_HEADERS", "RESPONSE_BODY"],
    }

    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/inspectionControls/customControlTypes",
        json=control_types,
        status=200,
    )
    resp = zpa.inspection.list_custom_control_types()
    assert isinstance(resp, Box)
    assert resp["request"][0] == "REQUEST_HEADERS"


@responses.activate
def test_list_custom_http_methods(zpa):
    methods = ["GET", "HEAD", "POST", "OPTIONS", "PUT", "DELETE", "PATCH", "TRACE", "CONNECT"]

    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/inspectionControls/custom/httpMethods",
        json=methods,
        status=200,
    )
    resp = zpa.inspection.list_custom_http_methods()
    assert isinstance(resp, BoxList)
    assert resp[0] == "GET"


@responses.activate
@stub_sleep
def test_list_custom_controls(zpa, custom_controls):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/inspectionControls/custom?page=1",
        json=custom_controls,
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/inspectionControls/custom?page=2",
        json=[],
        status=200,
    )
    resp = zpa.inspection.list_custom_controls()
    assert isinstance(resp, BoxList)
    assert resp[0]["id"] == "1"


@responses.activate
@stub_sleep
def test_list_custom_controls_params(zpa, custom_controls):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/inspectionControls/custom?search=test&sortdir=DESC&page=1",  # noqa: E501
        json=custom_controls,
        match=[matchers.query_param_matcher({"search": "test", "sortdir": "DESC", "page": "1"})],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/inspectionControls/custom?search=test&sortdir=DESC&page=2",  # noqa: E501
        json=[],
        match=[matchers.query_param_matcher({"search": "test", "sortdir": "DESC", "page": "2"})],
        status=200,
    )
    resp = zpa.inspection.list_custom_controls(search="test", sortdir="DESC")
    assert isinstance(resp, BoxList)
    assert resp[0]["id"] == "1"


@responses.activate
def test_get_custom_control(zpa, custom_controls):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/inspectionControls/custom/1",
        json=custom_controls[0],
        status=200,
    )
    resp = zpa.inspection.get_custom_control(1)
    assert isinstance(resp, Box)
    assert resp["id"] == "1"


@responses.activate
def test_add_custom_control(zpa, custom_controls):
    responses.add(
        responses.POST,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/inspectionControls/custom",
        status=204,
        json=custom_controls[0],
        match=[
            matchers.json_params_matcher(
                {
                    "name": "test_a",
                    "description": "test description",
                    "defaultAction": "BLOCK",
                    "severity": "INFO",
                    "paranoiaLevel": "3",
                    "type": "REQUEST",
                    "rules": [
                        {
                            "names": ["test"],
                            "type": "REQUEST_HEADERS",
                            "conditions": [
                                {"lhs": "SIZE", "op": "GE", "rhs": "10"},
                                {"lhs": "VALUE", "op": "CONTAINS", "rhs": "test"},
                            ],
                        }
                    ],
                }
            )
        ],
    )
    resp = zpa.inspection.add_custom_control(
        "test_a",
        severity="INFO",
        description="test description",
        paranoia_level="3",
        type="REQUEST",
        default_action="BLOCK",
        rules=[
            {
                "names": ["test"],
                "type": "REQUEST_HEADERS",
                "conditions": [
                    ("SIZE", "GE", "10"),
                    ("VALUE", "CONTAINS", "test"),
                ],
            }
        ],
    )

    assert isinstance(resp, Box)
    assert resp.name == "test_a"


@responses.activate
def test_update_custom_control(zpa, custom_controls):
    updated_control = copy.deepcopy((custom_controls[0]))
    updated_control["description"] = "updated test"
    updated_control["rules"] = [
        {
            "names": ["test_update"],
            "type": "REQUEST_HEADERS",
            "conditions": [{"lhs": "SIZE", "op": "GE", "rhs": "5"}],
        }
    ]

    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/inspectionControls/custom/1",
        json=custom_controls[0],
        status=200,
    )

    responses.add(
        responses.PUT,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/inspectionControls/custom/1",
        status=204,
        match=[matchers.json_params_matcher(updated_control)],
    )

    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/inspectionControls/custom/1",
        json={
            "id": "1",
            "creationTime": "1653536435",
            "modifiedBy": "1",
            "name": "test_a",
            "description": "updated test",
            "severity": "INFO",
            "controlNumber": "4500000",
            "version": "1.0",
            "paranoiaLevel": "1",
            "defaultAction": "BLOCK",
            "type": "REQUEST",
            "controlRuleJson": '[{"type":"REQUEST_HEADERS","names":["test_update"],'
            '"conditions":[{"lhs":"SIZE","op":"GE","rhs":"5"}]}]',
        },
        status=200,
    )

    resp = zpa.inspection.update_custom_control(
        "1",
        description="updated test",
        rules=[
            {
                "names": ["test_update"],
                "type": "REQUEST_HEADERS",
                "conditions": [
                    ("SIZE", "GE", "5"),
                ],
            }
        ],
    )

    assert resp.name == updated_control["name"]
    assert (
        resp.controlRuleJson
        == '[{"type":"REQUEST_HEADERS","names":["test_update"],"conditions":[{"lhs":"SIZE","op":"GE","rhs":"5"}]}]'
    )


@responses.activate
def test_delete_custom_control(zpa):
    responses.add(
        responses.DELETE,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/inspectionControls/custom/1",
        status=204,
    )
    resp = zpa.inspection.delete_custom_control("1")
    assert resp == 204


@responses.activate
def test_list_control_severity_types(zpa):
    severity_types = ["CRITICAL", "ERROR", "WARNING", "INFO"]
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/inspectionControls/severityTypes",
        json=severity_types,
        status=200,
    )
    resp = zpa.inspection.list_control_severity_types()
    assert isinstance(resp, BoxList)
    assert resp[0] == "CRITICAL"


@responses.activate
def test_list_control_action_types(zpa):
    action_types = ["PASS", "BLOCK", "REDIRECT"]
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/inspectionControls/actionTypes",
        json=action_types,
        status=200,
    )
    resp = zpa.inspection.list_control_action_types()
    assert isinstance(resp, BoxList)
    assert resp[0] == "PASS"


@responses.activate
def test_get_predef_control(zpa, predefined_controls):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/inspectionControls/predefined/1",
        json=predefined_controls[0]["predefinedInspectionControls"][0],
        status=200,
    )
    resp = zpa.inspection.get_predef_control(1)
    assert isinstance(resp, Box)
    assert resp["id"] == "1"


@stub_sleep
@responses.activate
def test_list_profiles(zpa, inspection_profiles):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/inspectionProfile?page=1",
        json=inspection_profiles,
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/inspectionProfile?page=2",
        json=[],
        status=200,
    )
    resp = zpa.inspection.list_profiles()
    assert isinstance(resp, BoxList)
    assert resp[0]["id"] == "1"


@stub_sleep
@responses.activate
def test_list_profiles_params(zpa, inspection_profiles):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/inspectionProfile?search=test&page=1",
        json=inspection_profiles,
        match=[matchers.query_param_matcher({"search": "test", "page": "1"})],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/inspectionProfile?search=test&page=2",
        json=[],
        match=[matchers.query_param_matcher({"search": "test", "page": "2"})],
        status=200,
    )
    resp = zpa.inspection.list_profiles(search="test")
    assert isinstance(resp, BoxList)
    assert resp[0]["id"] == "1"


@responses.activate
def test_get_profile(zpa, inspection_profiles):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/inspectionProfile/3",
        json=inspection_profiles[2],
        status=200,
    )
    resp = zpa.inspection.get_profile(3)
    assert isinstance(resp, Box)
    assert resp["id"] == "3"


@responses.activate
def test_add_profile(zpa, inspection_profiles, predefined_controls):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/inspectionControls/predefined?version=OWASP_CRS%2F3.3.0",  # noqa: E501
        json=predefined_controls,
        status=200,
        match=[matchers.query_param_matcher({"version": "OWASP_CRS/3.3.0"})],
    )
    responses.add(
        responses.POST,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/inspectionProfile",
        status=204,
        json=inspection_profiles[0],
        match=[
            matchers.json_params_matcher(
                {
                    "name": "test",
                    "description": "test description",
                    "paranoiaLevel": "1",
                    "predefinedControls": [
                        {
                            "id": "1",
                            "modifiedTime": "1631459708",
                            "creationTime": "1631459708",
                            "name": "Failed to parse request body",
                            "description": "Failed to parse request body",
                            "severity": "CRITICAL",
                            "controlNumber": "200002",
                            "version": "OWASP_CRS/3.3.0",
                            "paranoiaLevel": "1",
                            "defaultAction": "BLOCK",
                            "controlGroup": "Protocol Issues",
                        },
                        {
                            "id": "2",
                            "action": "BLOCK",
                        },
                    ],
                    "predefinedControlsVersion": "OWASP_CRS/3.3.0",
                    "customControls": [{"id": "1", "action": "BLOCK"}],
                },
            )
        ],
    )
    resp = zpa.inspection.add_profile(
        name="test",
        description="test description",
        paranoia_level="1",
        predef_controls_version="OWASP_CRS/3.3.0",
        custom_controls=[("1", "BLOCK")],
        predef_controls=[("2", "BLOCK")],
    )

    assert resp.id == "1"


@responses.activate
def test_update_profile(zpa, inspection_profiles):
    updated_profile = copy.deepcopy((inspection_profiles[2]))
    updated_profile["description"] = "updated test"
    updated_profile["predefinedControls"] = [{"id": "10", "action": "PASS"}]
    updated_profile["customControls"] = [{"id": "11", "action": "PASS"}]

    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/inspectionProfile/3",
        json=inspection_profiles[2],
        status=200,
    )
    responses.add(
        responses.PUT,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/inspectionProfile/3",
        status=204,
        match=[matchers.json_params_matcher(updated_profile)],
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/inspectionProfile/3",
        json=updated_profile,
        status=200,
    )
    resp = zpa.inspection.update_profile(
        "3", description="updated test", predef_controls=[("10", "PASS")], custom_controls=[("11", "PASS")]
    )
    assert isinstance(resp, Box)
    assert resp.description == updated_profile["description"]


@responses.activate
def test_delete_profile(zpa):
    responses.add(
        responses.DELETE,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/inspectionProfile/1",
        status=204,
    )
    resp = zpa.inspection.delete_profile("1")
    assert resp == 204


@responses.activate
def test_update_profile_and_controls(zpa):
    responses.add(
        responses.PATCH,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/inspectionProfile/1/patch",
        status=204,
        match=[
            matchers.json_params_matcher(
                {
                    "inspectionProfileId": "1",
                    "inspectionProfile": {
                        "id": "1",
                        "name": "test_d",
                    },
                }
            )
        ],
    )

    resp = zpa.inspection.update_profile_and_controls("1", inspection_profile={"id": "1", "name": "test_d"})
    assert resp == 204


@responses.activate
def test_profile_control_attach(zpa, inspection_profiles):
    responses.add(
        responses.PUT,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/inspectionProfile/1/associateAllPredefinedControls?version=OWASP_CRS%2F3.3.0",  # noqa: E501
        status=204,
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/inspectionProfile/1",
        json=inspection_profiles[0],
        status=200,
    )
    resp = zpa.inspection.profile_control_attach("1", action="attach")


@responses.activate
def test_profile_control_detach(zpa, inspection_profiles):
    responses.add(
        responses.PUT,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/inspectionProfile/1/deAssociateAllPredefinedControls",  # noqa: E501
        status=204,
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/inspectionProfile/1",
        json=inspection_profiles[0],
        status=200,
    )
    resp = zpa.inspection.profile_control_attach("1", action="detach")


@responses.activate
def test_list_policy_rules_error(zpa):
    with pytest.raises(Exception) as e_info:
        resp = zpa.inspection.profile_control_attach("99999", action="error")
