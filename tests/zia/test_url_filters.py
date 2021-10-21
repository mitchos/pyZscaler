import pytest
import responses
from responses import matchers


@pytest.fixture(name="url_filters")
def fixture_url_filters():
    return [
        {
            "accessControl": "READ_WRITE",
            "action": "ALLOW",
            "blockOverride": False,
            "cbiProfileId": 0,
            "departments": [{"id": 1, "name": "Test"}],
            "enforceTimeValidity": False,
            "groups": [{"id": 1, "name": "Test"}],
            "id": 1,
            "locations": [{"id": 1, "name": "Test"}],
            "name": "Test A",
            "order": 1,
            "protocols": [
                "HTTPS_RULE",
                "HTTP_RULE",
            ],
            "rank": 7,
            "requestMethods": [
                "GET",
                "POST",
            ],
            "state": "ENABLED",
            "urlCategories": [
                "NUDITY",
                "PORNOGRAPHY",
            ],
            "userAgentTypes": ["MSEDGE"],
            "users": [{"id": 1, "name": "Test User A(test.usera@example.com)"}],
        },
        {
            "accessControl": "READ_WRITE",
            "action": "BLOCK",
            "blockOverride": False,
            "cbiProfileId": 0,
            "departments": [{"id": 1, "name": "Test"}],
            "enforceTimeValidity": False,
            "groups": [{"id": 1, "name": "Test"}],
            "id": 2,
            "locations": [{"id": 1, "name": "Test"}],
            "name": "Test B",
            "order": 2,
            "protocols": [
                "HTTPS_RULE",
                "HTTP_RULE",
            ],
            "rank": 7,
            "requestMethods": [
                "GET",
                "POST",
            ],
            "state": "ENABLED",
            "urlCategories": [
                "NUDITY",
                "PORNOGRAPHY",
            ],
            "userAgentTypes": ["MSEDGE"],
            "users": [{"id": 2, "name": "Test User B(test.userb@example.com)"}],
        },
    ]


@responses.activate
def test_list_rules(zia, url_filters):
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/urlFilteringRules",
        json=url_filters,
        status=200,
    )

    resp = zia.url_filters.list_rules()

    assert isinstance(resp, list)
    for rule in resp:
        assert isinstance(rule, dict)
        assert isinstance(rule.id, int)
        assert isinstance(rule.users, list)


@responses.activate
def test_get_rule(zia, url_filters):
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/urlFilteringRules/1",
        json=url_filters[0],
        status=200,
    )

    resp = zia.url_filters.get_rule("1")

    assert isinstance(resp, dict)
    assert resp.id == 1
    assert isinstance(resp.users, list)


@responses.activate
def test_delete_rule(zia):
    responses.add(
        responses.DELETE,
        url="https://zsapi.zscaler.net/api/v1/urlFilteringRules/1",
        status=204,
    )

    resp = zia.url_filters.delete_rule("1")

    assert resp == 204


@responses.activate
def test_add_rule(zia, url_filters):
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/urlFilteringRules",
        json=url_filters,
        status=200,
    )
    responses.add(
        responses.POST,
        url="https://zsapi.zscaler.net/api/v1/urlFilteringRules",
        json=url_filters[0],
        status=200,
        match=[
            matchers.json_params_matcher(
                {
                    "action": "ALLOW",
                    "departments": [{"id": 1}],
                    "groups": [{"id": 1}],
                    "locations": [{"id": 1}],
                    "name": "Test A",
                    "order": 1,
                    "protocols": [
                        "HTTPS_RULE",
                        "HTTP_RULE",
                    ],
                    "rank": 7,
                    "requestMethods": [
                        "GET",
                        "POST",
                    ],
                    "state": "ENABLED",
                    "urlCategories": [
                        "NUDITY",
                        "PORNOGRAPHY",
                    ],
                    "userAgentTypes": ["MSEDGE"],
                    "users": [{"id": 1}],
                }
            )
        ],
    )

    resp = zia.url_filters.add_rule(
        rank=7,
        name="Test A",
        action="ALLOW",
        protocols=["HTTPS_RULE", "HTTP_RULE"],
        request_methods=["GET", "POST"],
        departments=[1],
        url_categories=["NUDITY", "PORNOGRAPHY"],
        user_agent_types=["MSEDGE"],
        users=[1],
        groups=[1],
        locations=[1],
        order=1,
        state="ENABLED",
    )

    assert isinstance(resp, dict)
    assert resp.name == "Test A"


@responses.activate
def test_update_rule(zia, url_filters):
    updated_rule = url_filters[0]
    updated_rule["name"] = "Updated Test"
    updated_rule["users"] = [{"id": 1}, {"id": 2}]
    updated_rule["order"] = 2
    updated_rule["requestMethods"] = ["PUT"]

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/urlFilteringRules/1",
        json=url_filters[0],
        status=200,
    )
    responses.add(
        responses.PUT,
        url="https://zsapi.zscaler.net/api/v1/urlFilteringRules/1",
        json=updated_rule,
        status=200,
        match=[
            matchers.json_params_matcher(
                {
                    "accessControl": "READ_WRITE",
                    "action": "ALLOW",
                    "blockOverride": False,
                    "cbiProfileId": 0,
                    "departments": [{"id": 1, "name": "Test"}],
                    "enforceTimeValidity": False,
                    "groups": [{"id": 1, "name": "Test"}],
                    "id": 1,
                    "locations": [{"id": 1, "name": "Test"}],
                    "name": "Updated Test",
                    "order": 2,
                    "protocols": [
                        "HTTPS_RULE",
                        "HTTP_RULE",
                    ],
                    "rank": 7,
                    "requestMethods": [
                        "PUT",
                    ],
                    "state": "ENABLED",
                    "urlCategories": [
                        "NUDITY",
                        "PORNOGRAPHY",
                    ],
                    "userAgentTypes": ["MSEDGE"],
                    "users": [{"id": 1}, {"id": 2}],
                }
            )
        ],
    )

    resp = zia.url_filters.update_rule("1", name="Updated Test", users=[1, 2], order=2, request_methods=["PUT"])

    assert resp.name == "Updated Test"
    assert resp.users[1]["id"] == 2
    assert resp.order == 2
    assert resp.request_methods == ["PUT"]
