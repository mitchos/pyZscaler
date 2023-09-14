import pytest
import responses
from box import BoxList
from responses.matchers import json_params_matcher


@pytest.fixture(name="location_list")
def fixture_location_list():
    return BoxList(
        [
            {
                "id": 10000001,
                "name": "FakeLocation1",
                "non_editable": False,
                "parent_id": 0,
                "up_bandwidth": 1000,
                "dn_bandwidth": 1000,
                "country": "AUSTRALIA",
                "state": "NSW",
                "language": "English",
                "tz": "AUSTRALIA_SYDNEY",
                "auth_required": True,
                "ssl_scan_enabled": True,
                "dynamiclocation_groups": [{"id": 101, "name": "FakeGroup1"}],
                "profile": "CORPORATE",
            },
            {
                "id": 10000002,
                "name": "FakeLocation2",
                "non_editable": True,
                "parent_id": 1,
                "up_bandwidth": 2000,
                "dn_bandwidth": 2000,
                "country": "AUSTRALIA",
                "state": "VIC",
                "language": "English",
                "tz": "AUSTRALIA_MELBOURNE",
                "auth_required": False,
                "ssl_scan_enabled": False,
                "dynamiclocation_groups": [{"id": 102, "name": "FakeGroup2"}],
                "profile": "SERVER",
            },
        ]
    )


@pytest.fixture(name="location_template_list")
def fixture_location_template_list():
    return [
        {
            "id": 111111,
            "name": "Mock Location 1",
            "desc": "Mock description 1",
            "template": {
                "xff_forward_enabled": False,
                "auth_required": True,
            },
            "editable": False,
            "last_mod_time": 1671850480,
        },
        {
            "id": 222222,
            "name": "Mock Location 2",
            "desc": "Mock description 2",
            "template": {
                "xff_forward_enabled": True,
                "auth_required": False,
            },
            "editable": True,
            "last_mod_uid": {"id": 666666, "name": "mock-admin@11111.zscaler.net"},
            "last_mod_time": 1694482952,
        },
    ]


@responses.activate
def test_list_locations(zcon, location_list):
    responses.add(
        method="GET",
        url="https://connector.zscaler.net/api/v1/location",
        json=location_list,
        status=200,
    )

    resp = zcon.locations.list_locations()
    assert isinstance(resp, BoxList)
    assert len(resp) == 2
    assert resp[0]["id"] == 10000001
    assert resp[1]["id"] == 10000002


@responses.activate
def test_get_location(zcon, location_list):
    location_id = "10000001"
    responses.add(
        method="GET",
        url=f"https://connector.zscaler.net/api/v1/adminRoles/{location_id}",
        json=location_list[0],
        status=200,
    )

    resp = zcon.locations.get_location(location_id)
    assert resp["id"] == 10000001
    assert resp["name"] == "FakeLocation1"


@responses.activate
def test_list_location_templates(zcon, location_template_list):
    responses.add(
        method="GET",
        url="https://connector.zscaler.net/api/v1/locationTemplate",
        json=location_template_list,
        status=200,
    )

    resp = zcon.locations.list_location_templates()
    assert isinstance(resp, list)
    assert len(resp) == 2
    assert resp[0]["id"] == 111111
    assert resp[1]["id"] == 222222


@responses.activate
def test_add_location_template(zcon):
    # The template to add
    name = "New Mock Name"
    template = {"surrogate_ip": True, "template_prefix": "office", "auth_required": True}
    description = "New mock description"

    # Stub for the POST request to add a new location template
    responses.add(
        method="POST",
        url="https://connector.zscaler.net/api/v1/locationTemplate",
        json={"name": name, "template": template, "desc": description},
        match=[
            json_params_matcher(
                {
                    "name": name,
                    "template": {
                        "surrogateIP": template["surrogate_ip"],
                        "templatePrefix": template["template_prefix"],
                        "authRequired": template["auth_required"],
                    },
                    "desc": description,
                }
            )
        ],
        status=201,
    )

    # Add location template
    added_template = zcon.locations.add_location_template(name, template=template, description=description)

    # Verify the response
    assert added_template["name"] == name
    assert added_template["template"] == template
    assert added_template["desc"] == description


@responses.activate
def test_update_location_template(zcon, location_template_list):
    template_id = "111111"

    # Stub for the GET request to retrieve existing template
    responses.add(
        method="GET",
        url=f"https://connector.zscaler.net/api/v1/locationTemplate/{template_id}",
        json=location_template_list[1],
        status=200,
    )

    # Stub for the PUT request to update template
    responses.add(
        method="PUT",
        url=f"https://connector.zscaler.net/api/v1/locationTemplate/{template_id}",
        json=location_template_list[1],
        status=200,
    )

    # Update location template with the name "New Mock Name"
    updated_template = zcon.locations.update_location_template(
        template_id, name="Mock Location 2", description="Mock description 2"
    )
    assert updated_template["name"] == "Mock Location 2"
    assert updated_template["desc"] == "Mock description 2"


@responses.activate
def test_delete_location_template(zcon):
    template_id = "411908"

    # Stub for the DELETE request
    responses.add(
        method="DELETE",
        url=f"https://connector.zscaler.net/api/v1/locationTemplate/{template_id}",
        status=204,
    )

    # Delete location template
    status_code = zcon.locations.delete_location_template(template_id)
    assert status_code == 204
