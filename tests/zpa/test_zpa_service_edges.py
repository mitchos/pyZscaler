import pytest
import responses
from box import Box, BoxList
from responses import matchers

from tests.conftest import stub_sleep


# Don't have an example of the service edge data format just yet.
# id will suffice until this is determined.
@pytest.fixture(name="service_edges")
def fixture_service_edges():
    return {"totalPages": 1, "list": [{"id": "1"}, {"id": "2"}]}


@pytest.fixture(name="service_edge_groups")
def fixture_service_edge_groups():
    return {"totalPages": 1, "list": [{"id": "1"}, {"id": "2"}]}


@responses.activate
@stub_sleep
def test_list_service_edges(zpa, service_edges):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/serviceEdge?page=1",
        json=service_edges,
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/serviceEdge?page=2",
        json=[],
        status=200,
    )
    resp = zpa.service_edges.list_service_edges()
    assert isinstance(resp, BoxList)
    assert len(resp) == 2
    assert resp[0].id == "1"


@responses.activate
@stub_sleep
def test_list_service_edge_groups(zpa, service_edge_groups):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/serviceEdgeGroup?page=1",
        json=service_edge_groups,
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/serviceEdgeGroup?page=2",
        json=[],
        status=200,
    )
    resp = zpa.service_edges.list_service_edge_groups()
    assert isinstance(resp, BoxList)
    assert len(resp) == 2
    assert resp[0].id == "1"


@responses.activate
def test_get_service_edge(zpa, service_edges):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/serviceEdge/1",
        json=service_edges["list"][0],
        status=200,
    )
    resp = zpa.service_edges.get_service_edge("1")
    assert isinstance(resp, Box)
    assert resp.id == "1"


@responses.activate
def test_get_service_edge_group(zpa, service_edge_groups):
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/serviceEdgeGroup/1",
        json=service_edge_groups["list"][0],
        status=200,
    )
    resp = zpa.service_edges.get_service_edge_group("1")
    assert isinstance(resp, Box)
    assert resp.id == "1"


@responses.activate
def test_bulk_delete_service_edges(zpa):
    responses.add(
        responses.POST,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/serviceEdge/bulkDelete",
        status=204,
        match=[matchers.json_params_matcher({"ids": ["1", "2"]})],
    )
    resp = zpa.service_edges.bulk_delete_service_edges(["1", "2"])
    assert isinstance(resp, int)
    assert resp == 204


@responses.activate
def test_delete_service_edge(zpa):
    responses.add(
        responses.DELETE,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/serviceEdge/1",
        status=204,
    )
    resp = zpa.service_edges.delete_service_edge("1")
    assert isinstance(resp, int)
    assert resp == 204


@responses.activate
def test_delete_service_edge_group(zpa):
    responses.add(
        responses.DELETE,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/serviceEdgeGroup/1",
        status=204,
    )
    resp = zpa.service_edges.delete_service_edge_group("1")
    assert isinstance(resp, int)
    assert resp == 204


@responses.activate
def test_update_service_edge(zpa, service_edges):
    updated_service_edge = service_edges["list"][0]
    updated_service_edge["description"] = "Updated Test"
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/serviceEdge/1",
        json=service_edges["list"][0],
        status=200,
    )
    responses.add(
        responses.PUT,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/serviceEdge/1",
        status=204,
        match=[matchers.json_params_matcher(updated_service_edge)],
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/serviceEdge/1",
        json=updated_service_edge,
        status=200,
    )
    resp = zpa.service_edges.update_service_edge("1", description="Updated Test")
    assert isinstance(resp, Box)
    assert resp.id == "1"
    assert resp.description == updated_service_edge["description"]


@responses.activate
def test_update_service_edge_group(zpa, service_edge_groups):
    updated_service_edge_group = service_edge_groups["list"][0]
    updated_service_edge_group["name"] = "Updated Test"
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/serviceEdgeGroup/1",
        json=service_edge_groups["list"][0],
        status=200,
    )
    responses.add(
        responses.PUT,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/serviceEdgeGroup/1",
        status=204,
        match=[matchers.json_params_matcher(updated_service_edge_group)],
    )
    responses.add(
        responses.GET,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/serviceEdgeGroup/1",
        json=updated_service_edge_group,
        status=200,
    )
    resp = zpa.service_edges.update_service_edge_group("1", name="Updated Test")
    assert isinstance(resp, Box)
    assert resp.id == "1"
    assert resp.name == updated_service_edge_group["name"]


@responses.activate
def test_add_service_edge_groups(zpa, service_edge_groups):
    responses.add(
        responses.POST,
        url="https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/1/serviceEdgeGroup",
        status=200,
        json=service_edge_groups["list"][0],
        match=[
            matchers.json_params_matcher(
                {
                    "name": "Test",
                    "latitude": "1.0",
                    "longitude": "1.0",
                    "location": "Sydney",
                    "enabled": True,
                    "versionProfileId": 1,
                    "overrideVersionProfile": True,
                    "trustedNetworks": [{"id": "1"}, {"id": "2"}],
                }
            )
        ],
    )
    resp = zpa.service_edges.add_service_edge_group(
        name="Test",
        latitude="1.0",
        longitude="1.0",
        location="Sydney",
        enabled=True,
        version_profile="previous_default",
        trusted_network_ids=["1", "2"],
    )
    assert isinstance(resp, Box)
    assert resp.id == "1"
