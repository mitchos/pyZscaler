import copy

import pytest
import responses
from box import Box, BoxList
from responses import matchers

from tests.conftest import stub_sleep


@pytest.fixture(name="policies")
def fixture_policies():
    return {"totalPages": 1, "list": [{"id": "1"}, {"id": "2"}, {"id": "3"}, {"id": "4"}]}


@pytest.fixture(name="policy_conditions")
def fixture_policy_conditions():
    return [
        [
            ("app", "id", "216197915188658453"),
            ("app", "id", "216197915188658455"),
            "OR",
        ],
        [
            ("scim", "216197915188658304", "john.doe@foo.bar"),
            ("scim", "216197915188658304", "foo.bar"),
            "OR",
        ],
        ("scim_group", "216197915188658303", "241874"),  # check backward compatibility
        [
            ("posture", "fc92ead2-4046-428d-bf3f-6e534a53194b", "TRUE"),
            ("posture", "490db9b4-96d8-4035-9b5e-935daa697f45", "TRUE"),
            "AND",
        ],
    ]


@pytest.fixture(name="policy_rules")
def fixture_policy_rules():
    return {
        "totalPages": 1,
        "list": [
            {
                "id": "1",
                "modifiedTime": "1628558068",
                "creationTime": "1620806263",
                "modifiedBy": "1",
                "name": "Test",
                "ruleOrder": "1",
                "priority": "10",
                "policyType": "1",
                "operator": "AND",
                "conditions": [
                    {
                        "id": "1",
                        "modifiedTime": "1620806263",
                        "creationTime": "1620806263",
                        "modifiedBy": "1",
                        "operator": "OR",
                        "negated": False,
                        "operands": [
                            {
                                "id": "1",
                                "creationTime": "1620806263",
                                "modifiedBy": "1",
                                "objectType": "APP_GROUP",
                                "lhs": "id",
                                "rhs": "1",
                                "name": "Test",
                            }
                        ],
                    }
                ],
                "action": "ALLOW",
                "defaultRule": False,
            },
            {
                "id": "2",
                "modifiedTime": "1628558068",
                "creationTime": "1620806263",
                "modifiedBy": "1",
                "name": "Test",
                "ruleOrder": "1",
                "priority": "10",
                "policyType": "1",
                "operator": "AND",
                "conditions": [
                    {
                        "id": "1",
                        "modifiedTime": "1620806263",
                        "creationTime": "1620806263",
                        "modifiedBy": "1",
                        "operator": "OR",
                        "negated": False,
                        "operands": [
                            {
                                "id": "1",
                                "creationTime": "1620806263",
                                "modifiedBy": "1",
                                "objectType": "APP_GROUP",
                                "lhs": "id",
                                "rhs": "1",
                                "name": "Test",
                            }
                        ],
                    }
                ],
                "action": "ALLOW",
                "defaultRule": False,
            },
        ],
    }


@responses.activate
@stub_sleep
def test_list_rules(zpa, policy_rules):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/policySet/rules/policyType/ACCESS_POLICY?page=1",  # noqa: E501
        json=policy_rules,
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/policySet/rules/policyType/ACCESS_POLICY?page=2",  # noqa: E501
        json=[],
        status=200,
    )
    resp = zpa.policies.list_rules("access")
    assert isinstance(resp, BoxList)
    assert len(resp) == 2
    assert resp[0].id == "1"


def test_list_policy_rules_error(zpa, policy_rules):
    with pytest.raises(Exception) as e_info:
        resp = zpa.policies.list_rules("test")


def test_create_conditions(zpa, policy_conditions):
    conditions = zpa.policies._create_conditions(policy_conditions)
    assert conditions == [
        {
            "operands": [
                {"objectType": "APP", "lhs": "id", "rhs": "216197915188658453"},
                {"objectType": "APP", "lhs": "id", "rhs": "216197915188658455"},
            ],
            "operator": "OR",
        },
        {
            "operands": [
                {"objectType": "SCIM", "lhs": "216197915188658304", "rhs": "john.doe@foo.bar"},
                {"objectType": "SCIM", "lhs": "216197915188658304", "rhs": "foo.bar"},
            ],
            "operator": "OR",
        },
        {"operands": [{"objectType": "SCIM_GROUP", "lhs": "216197915188658303", "rhs": "241874"}]},
        {
            "operands": [
                {"objectType": "POSTURE", "lhs": "fc92ead2-4046-428d-bf3f-6e534a53194b", "rhs": "TRUE"},
                {"objectType": "POSTURE", "lhs": "490db9b4-96d8-4035-9b5e-935daa697f45", "rhs": "TRUE"},
            ],
            "operator": "AND",
        },
    ]


@responses.activate
def test_get_access_policy(zpa, policies):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/policySet/policyType/ACCESS_POLICY",
        json=policies["list"][0],
        status=200,
    )
    resp = zpa.policies.get_policy("access")
    assert isinstance(resp, Box)
    assert resp.id == "1"


def test_get_access_policy_error(zpa, policies):
    with pytest.raises(Exception) as e_info:
        resp = zpa.policies.get_policy("test")


@responses.activate
def test_get_policy_rule(zpa, policies, policy_rules):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/policySet/policyType/ACCESS_POLICY",
        json=policies["list"][0],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/policySet/1/rule/1",
        json=policy_rules["list"][0],
        status=200,
    )
    resp = zpa.policies.get_rule("access", "1")
    assert isinstance(resp, Box)
    assert resp.id == "1"


@responses.activate
def test_delete_policy_rule(zpa, policies):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/policySet/policyType/ACCESS_POLICY",
        json=policies["list"][0],
        status=200,
    )
    responses.add(
        responses.DELETE,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/policySet/1/rule/1",
        status=204,
    )
    resp = zpa.policies.delete_rule("access", "1")
    assert isinstance(resp, int)
    assert resp == 204


@responses.activate
def test_add_access_policy_rule(zpa, policies, policy_rules):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/policySet/policyType/ACCESS_POLICY",
        json=policies["list"][0],
        status=200,
    )
    responses.add(
        responses.POST,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/policySet/1/rule",
        json=policy_rules["list"][0],
        status=200,
        match=[
            matchers.json_params_matcher(
                {
                    "name": "Test",
                    "action": "ALLOW",
                    "description": "Test",
                    "conditions": [{"operands": [{"objectType": "APP_GROUP", "lhs": "id", "rhs": "1"}]}],
                }
            )
        ],
    )
    resp = zpa.policies.add_access_rule(name="Test", action="allow", conditions=[("app_group", "id", "1")], description="Test")

    assert isinstance(resp, Box)
    assert resp.id == "1"


@responses.activate
def test_add_timeout_policy_rule(zpa, policies, policy_rules):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/policySet/policyType/TIMEOUT_POLICY",
        json=policies["list"][1],
        status=200,
    )
    responses.add(
        responses.POST,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/policySet/2/rule",
        json=policy_rules["list"][0],
        status=200,
        match=[
            matchers.json_params_matcher(
                {
                    "name": "Test",
                    "action": "RE_AUTH",
                    "description": "Test",
                    "reauthTimeout": 172800,
                    "reauthIdleTimeout": 600,
                    "conditions": [{"operands": [{"objectType": "APP_GROUP", "lhs": "id", "rhs": "1"}]}],
                }
            )
        ],
    )
    resp = zpa.policies.add_timeout_rule(name="Test", conditions=[("app_group", "id", "1")], description="Test")

    assert isinstance(resp, Box)
    assert resp.id == "1"


@responses.activate
def test_add_client_forwarding_policy_rule(zpa, policies, policy_rules):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/policySet/policyType/CLIENT_FORWARDING_POLICY",  # noqa: E501
        json=policies["list"][2],
        status=200,
    )

    responses.add(
        responses.POST,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/policySet/3/rule",
        json=policy_rules["list"][0],
        status=200,
        match=[
            matchers.json_params_matcher(
                {
                    "name": "Test",
                    "action": "INTERCEPT",
                    "description": "Test",
                    "conditions": [{"operands": [{"objectType": "APP_GROUP", "lhs": "id", "rhs": "1"}]}],
                }
            )
        ],
    )
    resp = zpa.policies.add_client_forwarding_rule(
        name="Test", action="intercept", conditions=[("app_group", "id", "1")], description="Test"
    )

    assert isinstance(resp, Box)
    assert resp.id == "1"


@responses.activate
def test_add_isolation_policy_rule(zpa, policies, policy_rules):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/policySet/policyType/ISOLATION_POLICY",  # noqa: E501
        json=policies["list"][3],
        status=200,
    )

    responses.add(
        responses.POST,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/policySet/4/rule",
        json=policy_rules["list"][0],
        status=200,
        match=[
            matchers.json_params_matcher(
                {
                    "name": "Test",
                    "action": "BYPASS",
                    "description": "Test",
                    "zpnIsolationProfileId": "321",
                    "policySetId": "4",
                    "conditions": [
                        {
                            "operands": [
                                {"objectType": "APP", "lhs": "id", "rhs": "1"},
                                {"objectType": "APP", "lhs": "id", "rhs": "2"},
                            ],
                            "operator": "OR",
                        },
                        {
                            "operands": [{"objectType": "CLIENT_TYPE", "lhs": "id", "rhs": "zpn_client_type_exporter"}],
                            "operator": "OR",
                        },
                    ],
                }
            )
        ],
    )
    resp = zpa.policies.add_isolation_rule(
        name="Test",
        action="bypass",
        zpn_isolation_profile_id="321",
        conditions=[
            [("APP", "id", "1"), ("APP", "id", "2"), "OR"],
            [("client_type", "id", "zpn_client_type_exporter"), "OR"],
        ],
        description="Test",
    )

    assert isinstance(resp, Box)
    assert resp.id == "1"


@responses.activate
def test_update_policy_rule(zpa, policies, policy_rules):
    updated_rule = policy_rules["list"][0]
    updated_rule["description"] = "Updated Test"
    updated_rule["conditions"] = [{"operands": [{"objectType": "APP_GROUP", "lhs": "id", "rhs": "2"}]}]
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/policySet/policyType/ACCESS_POLICY",
        json=policies["list"][0],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/policySet/1/rule/1",
        json=policy_rules["list"][0],
        status=200,
    )
    responses.add(
        responses.PUT,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/policySet/1/rule/1",
        status=204,
        match=[matchers.json_params_matcher(updated_rule)],
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/policySet/1/rule/1",
        json=policies["list"][0],
        status=200,
    )
    resp = zpa.policies.update_rule("access", "1", description="Updated Test", conditions=[("app_group", "id", "2")])
    assert isinstance(resp, Box)
    assert resp.id == "1"


@responses.activate
def test_reorder_rule(zpa, policies, policy_rules):
    updated_rule = copy.deepcopy(policy_rules["list"][0])
    updated_rule["ruleOrder"] = "2"
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/policySet/policyType/ACCESS_POLICY",
        json=policies["list"][0],
        status=200,
    )
    responses.add(
        responses.PUT,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/policySet/1/rule/1/reorder/2",
        status=204,
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/policySet/1/rule/1",
        json=updated_rule,
        status=200,
    )
    resp = zpa.policies.reorder_rule("access", "1", "2")
    assert isinstance(resp, Box)
    assert resp.rule_order == "2"
