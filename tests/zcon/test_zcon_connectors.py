import pytest
import responses


@pytest.fixture
def connector_groups_list():
    return [
        {
            "id": 1,
            "name": "GroupA",
            "ec_vms": [
                {
                    "id": 10,
                    "name": "GroupA-VM1",
                    "ec_instances": [{"id": 100, "name": "Instance1"}, {"id": 101, "name": "Instance2"}],
                },
                {"id": 11, "name": "GroupA-VM2", "ec_instances": []},
            ],
        },
        {"id": 2, "name": "GroupB", "ec_vms": [{"id": 20, "name": "GroupB-VM1", "ec_instances": []}]},
    ]


@responses.activate
def test_list_groups(zcon, connector_groups_list):
    responses.add(
        method="GET",
        url="https://connector.zscaler.net/api/v1/ecgroup",
        json=connector_groups_list,
        status=200,
    )

    resp = zcon.connectors.list_groups()
    assert isinstance(resp, list)
    assert len(resp) == 2
    assert resp[0]["id"] == 1
    assert resp[0]["name"] == "GroupA"
    assert resp[0]["ec_vms"][0]["id"] == 10


@responses.activate
def test_get_group(zcon, connector_groups_list):
    connector_group = connector_groups_list[0]
    responses.add(
        method="GET",
        url="https://connector.zscaler.net/api/v1/ecgroup/1",
        json=connector_group,
        status=200,
    )

    resp = zcon.connectors.get_group("1")
    assert isinstance(resp, dict)
    assert resp["id"] == 1
    assert resp["name"] == "GroupA"
    assert resp["ec_vms"][0]["ec_instances"][0]["id"] == 100


@responses.activate
def test_get_vm(zcon, connector_groups_list):
    # Mock the API call to get a specific VM
    responses.add(
        method="GET",
        url="https://connector.zscaler.net/api/v1/ecgroup/1/vm/10",
        json=connector_groups_list[0]["ec_vms"][0],
        status=204,
    )

    # Execute the function and get the result
    result = zcon.connectors.get_vm("1", "10")

    # Verify the response
    assert result["id"] == connector_groups_list[0]["ec_vms"][0]["id"]
    assert result["name"] == connector_groups_list[0]["ec_vms"][0]["name"]


@responses.activate
def test_delete_vm(zcon):
    # Mock the API call to delete a specific VM
    group_id = "1"
    vm_id = "10"
    responses.add(
        method="DELETE",
        url=f"https://connector.zscaler.net/api/v1/ecgroup/{group_id}/vm/{vm_id}",
        status=204,
    )

    # Execute the function and get the result
    status_code = zcon.connectors.delete_vm(group_id, vm_id)

    # Verify the response
    assert status_code == 204
