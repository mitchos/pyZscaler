import copy

import pytest
import responses
from box import Box
from responses import matchers

from tests.conftest import stub_sleep


@pytest.fixture(name="labels")
def fixture_labels():
    return [
        {
            "id": 999999,
            "description": "Test Label Description",
            "name": "Test Label A",
            "lastModifiedTime": 1650936087,
            "lastModifiedBy": {"id": 999999, "name": "admin@example.com"},
            "createdBy": {"id": 999999, "name": "admin@example.com"},
            "referencedRuleCount": 1,
        },
        {
            "id": 888888,
            "name": "Test Label B",
            "lastModifiedTime": 1650936087,
            "lastModifiedBy": {"id": 999999, "name": "admin@example.com"},
            "createdBy": {"id": 999999, "name": "admin@example.com"},
            "referencedRuleCount": 0,
        },
    ]


@responses.activate
def test_labels_add_label(zia, labels):
    responses.add(
        method="POST",
        url="https://zsapi.zscaler.net/api/v1/ruleLabels",
        json=labels[0],
        status=200,
        match=[matchers.json_params_matcher({"name": "Test Label A", "description": "Test Label Description"})],
    )

    resp = zia.labels.add_label(name="Test Label A", description="Test Label Description")

    assert isinstance(resp, dict)
    assert resp.id == 999999
    assert resp.name == "Test Label A"


@responses.activate
@stub_sleep
def test_list_labels_with_one_page(zia, paginated_items):
    items = paginated_items(200)

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/ruleLabels",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/ruleLabels",
        json=items[100:200],
        status=200,
    )

    resp = zia.labels.list_labels(max_pages=1, page_size=100)

    assert isinstance(resp, list)
    assert resp[50].id == 50
    assert len(resp) == 100


@responses.activate
@stub_sleep
def test_list_labels_with_two_pages(zia, paginated_items):
    items = paginated_items(200)

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/ruleLabels",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/ruleLabels",
        json=items[100:200],
        status=200,
    )

    resp = zia.labels.list_labels(max_pages=2, page_size=100)

    assert isinstance(resp, list)
    assert resp[50].id == 50
    assert resp[150].id == 150
    assert len(resp) == 200


@responses.activate
@stub_sleep
def test_list_labels_with_max_items_1(zia, paginated_items):
    items = paginated_items(200)

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/ruleLabels",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/ruleLabels",
        json=items[100:200],
        status=200,
    )

    resp = zia.labels.list_labels(max_items=1)

    assert isinstance(resp, list)
    assert len(resp) == 1


@responses.activate
@stub_sleep
def test_list_labels_with_max_items_150(zia, paginated_items):
    items = paginated_items(200)

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/ruleLabels",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/ruleLabels",
        json=items[100:200],
        status=200,
    )

    resp = zia.labels.list_labels(max_items=150)

    assert isinstance(resp, list)
    assert len(resp) == 150


@responses.activate
def test_labels_get_label_by_id(labels, zia):
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/ruleLabels/999999",
        json=labels[0],
        status=200,
    )
    resp = zia.labels.get_label("999999")

    assert isinstance(resp, dict)
    assert resp.id == 999999


@responses.activate
def test_users_update_label(zia, labels):
    updated_label = copy.deepcopy(labels[0])
    updated_label["name"] = "Updated Label C"
    updated_label["description"] = "Updated Label Description"

    responses.add(
        responses.GET,
        "https://zsapi.zscaler.net/api/v1/ruleLabels/999999",
        json=labels[0],
        status=200,
    )

    responses.add(
        responses.PUT,
        url="https://zsapi.zscaler.net/api/v1/ruleLabels/999999",
        json=updated_label,
        match=[matchers.json_params_matcher(updated_label)],
    )

    resp = zia.labels.update_label(
        "999999",
        name="Updated Label C",
        description="Updated Label Description",
    )

    assert isinstance(resp, Box)
    assert resp.name == updated_label["name"]
    assert resp.description == updated_label["description"]


@responses.activate
def test_labels_delete_label(zia):
    responses.add(method="DELETE", url="https://zsapi.zscaler.net/api/v1/ruleLabels/999999", status=204)
    resp = zia.labels.delete_label("999999")
    assert resp == 204
