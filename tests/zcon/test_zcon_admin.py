import pytest
import responses
from box import Box, BoxList
from responses.matchers import json_params_matcher


@pytest.fixture(name="admin_users")
def fixture_admin_users():
    return [
        {
            "id": 1,
            "name": "Admin1",
            "role": "SuperAdmin",
        },
        {
            "id": 2,
            "name": "Admin2",
            "role": "RegularAdmin",
        },
    ]


@pytest.fixture(name="admin_roles")
def fixture_admin_roles():
    return [
        {
            "id": 11111,
            "rank": 7,
            "name": "NewRole",
            "policyAccess": "NONE",
        },
        {
            "id": 22222,
            "rank": 7,
            "name": "AdvancedRole",
            "policyAccess": "READ_ONLY",
            "alertingAccess": "READ_WRITE",
            "featurePermissions": {
                "APIKEY_MANAGEMENT": "READ_ONLY",
                "EDGE_CONNECTOR_CLOUD_PROVISIONING": "NONE",
            },
        },
    ]


@pytest.fixture
def api_keys():
    return [
        {
            "id": 1,
            "keyValue": "fakeKeyValue1",
            "permissions": ["USER_ACCESS"],
            "enabled": True,
            "lastModifiedTime": 1631541800,
            "lastModifiedBy": {
                "id": 1,
                "name": "fakeModifier1",
            },
            "partner": {
                "id": 1,
                "name": "fakePartner1",
            },
            "partnerUrl": "https://fakepartnerurl1.com",
        },
        {
            "id": 2,
            "keyValue": "fakeKeyValue2",
            "permissions": ["USER_ACCESS"],
            "enabled": False,
            "lastModifiedTime": 1631641800,
            "lastModifiedBy": {
                "id": 2,
                "name": "fakeModifier2",
            },
            "partner": {
                "id": 2,
                "name": "fakePartner2",
            },
            "partnerUrl": "https://fakepartnerurl2.com",
        },
    ]


@responses.activate
def test_add_role_min_args(zcon, admin_roles):
    responses.add(
        method="POST",
        url="https://connector.zscaler.net/api/v1/adminRoles",
        json=admin_roles[0],
        status=200,
        match=[
            json_params_matcher(
                {
                    "name": "NewRole",
                    "dashboardAccess": "NONE",
                    "policyAccess": "NONE",
                    "reportAccess": "NONE",
                    "roleType": "EDGE_CONNECTOR_ADMIN",
                    "usernameAccess": "NONE",
                }
            )
        ],
    )

    resp = zcon.admin.add_role(name="NewRole")
    assert isinstance(resp, dict)
    assert resp["name"] == "NewRole"
    assert resp["id"] == 11111


@responses.activate
def test_add_role_with_args(zcon, admin_roles):
    responses.add(
        method="POST",
        url="https://connector.zscaler.net/api/v1/adminRoles",
        json=admin_roles[1],
        status=200,
        match=[
            json_params_matcher(
                {
                    "name": "AdvancedRole",
                    "policyAccess": "READ_ONLY",
                    "alertingAccess": "READ_WRITE",
                    "dashboardAccess": "NONE",
                    "reportAccess": "NONE",
                    "usernameAccess": "NONE",
                    "roleType": "EDGE_CONNECTOR_ADMIN",
                    "featurePermissions": {"edgeConnectorCloudProvisioning": "NONE", "apikeyManagement": "READ_ONLY"},
                }
            )
        ],
    )

    resp = zcon.admin.add_role(
        name="AdvancedRole",
        policy_access="READ_ONLY",
        feature_permissions_tuples=[
            ("APIKEY_MANAGEMENT", "READ_ONLY"),
            ("EDGE_CONNECTOR_CLOUD_PROVISIONING", "NONE"),
        ],
        alerting_access="READ_WRITE",
    )
    assert isinstance(resp, dict)
    assert resp["name"] == "AdvancedRole"
    assert resp["id"] == 22222


@responses.activate
def test_list_roles(zcon, admin_roles):
    responses.add(
        method="GET",
        url="https://connector.zscaler.net/api/v1/adminRoles",
        json=admin_roles,
        status=200,
    )

    resp = zcon.admin.list_roles()
    assert isinstance(resp, list)
    assert len(resp) == len(admin_roles)
    assert resp[0]["id"] == admin_roles[0]["id"]
    assert resp[1]["name"] == admin_roles[1]["name"]


@responses.activate
def test_get_role(zcon, admin_roles):
    responses.add(
        method="GET",
        url="https://connector.zscaler.net/api/v1/adminRoles/11111",
        json=admin_roles[0],
        status=200,
    )

    resp = zcon.admin.get_role(11111)
    assert isinstance(resp, dict)
    assert resp["name"] == "NewRole"
    assert resp["id"] == 11111


@responses.activate
def test_delete_role(zcon, admin_roles):
    responses.add(
        method="DELETE",
        url="https://connector.zscaler.net/api/v1/adminRoles/11111",
        status=200,
    )

    resp = zcon.admin.delete_role(11111)
    assert isinstance(resp, int)
    assert resp == 200


@responses.activate
def test_update_role(zcon, admin_roles):
    role_id = admin_roles[0]["id"]
    update_data = {
        "policy_access": "READ_ONLY",
        "feature_permissions": [("APIKEY_MANAGEMENT", "READ_WRITE"), ("EDGE_CONNECTOR_CLOUD_PROVISIONING", "NONE")],
        "alerting_access": "READ_WRITE",
    }

    # Simulate the existing role data
    responses.add(
        method="GET", url=f"https://connector.zscaler.net/api/v1/adminRoles/{role_id}", json=admin_roles[0], status=200
    )

    # Manually set the expected updated payload
    expected_updated_payload = {
        "alertingAccess": "READ_WRITE",
        "featurePermissions": {"APIKEY_MANAGEMENT": "READ_WRITE", "EDGE_CONNECTOR_CLOUD_PROVISIONING": "NONE"},
        "id": 11111,
        "name": "NewRole",
        "policyAccess": "READ_ONLY",
        "rank": 7,
    }

    responses.add(
        method="PUT",
        url=f"https://connector.zscaler.net/api/v1/adminRoles/{role_id}",
        json=expected_updated_payload,
        status=200,
        match=[json_params_matcher(expected_updated_payload)],
    )

    resp = zcon.admin.update_role(role_id, **update_data)
    assert isinstance(resp, Box)
    assert resp["id"] == role_id
    assert resp["policy_access"] == "READ_ONLY"
    assert resp["feature_permissions"] == {"apikey_management": "READ_WRITE", "edge_connector_cloud_provisioning": "NONE"}
    assert resp["alerting_access"] == "READ_WRITE"


@responses.activate
def test_list_admins_min_args(zcon, admin_users):
    responses.add(
        method="GET",
        url="https://connector.zscaler.net/api/v1/adminUsers?partnerType=EDGE_CONNECTOR_ADMIN",
        json=admin_users,
        status=200,
    )

    resp = zcon.admin.list_admins()
    assert isinstance(resp, BoxList)
    assert resp[0]["name"] == "Admin1"
    assert resp[1]["name"] == "Admin2"


@responses.activate
def test_list_admins_with_args(zcon, admin_users):
    responses.add(
        method="GET",
        url="https://connector.zscaler.net/api/v1/adminUsers?partnerType=EDGE_CONNECTOR_ADMIN&includeAuditorUsers=True&includeAdminUsers=True&includeApiRoles=True",  # noqa
        json=admin_users,
        status=200,
    )

    resp = zcon.admin.list_admins(include_auditor_users=True, include_admin_users=True, include_api_roles=True)

    assert isinstance(resp, BoxList)
    assert resp[0]["name"] == "Admin1"
    assert resp[1]["name"] == "Admin2"


@responses.activate
def test_get_admin(zcon, admin_users):
    admin_id = admin_users[0]["id"]
    responses.add(
        method="GET", url=f"https://connector.zscaler.net/api/v1/adminUsers/{admin_id}", json=admin_users[0], status=200
    )

    resp = zcon.admin.get_admin(admin_id)
    assert isinstance(resp, Box)
    assert resp["id"] == admin_id
    assert resp["name"] == admin_users[0]["name"]
    assert resp["role"] == admin_users[0]["role"]


@responses.activate
def test_add_admin(zcon, admin_users):
    admin_data = {
        "user_name": "John Doe",
        "login_name": "johndoe",
        "role": "admin",
        "email": "johndoe@example.com",
        "password": "password123",
        "is_default_admin": False,
        "disabled": False,
        "comments": "New admin user",
    }

    responses.add(
        method="POST",
        url="https://connector.zscaler.net/api/v1/adminUsers",
        json=admin_users[0],
        status=200,
        match=[
            json_params_matcher(
                {
                    "userName": "John Doe",
                    "loginName": "johndoe",
                    "role": "admin",
                    "email": "johndoe@example.com",
                    "password": "password123",
                    "isDefaultAdmin": False,
                    "disabled": False,
                    "comments": "New admin user",
                }
            )
        ],
    )

    resp = zcon.admin.add_admin(**admin_data)
    assert isinstance(resp, Box)
    assert resp["name"] == admin_users[0]["name"]
    assert resp["id"] == admin_users[0]["id"]
    assert resp["role"] == admin_users[0]["role"]


@responses.activate
def test_update_admin(zcon, admin_users):
    admin_id = admin_users[0]["id"]
    update_data = {"role": "new_role", "email": "newemail@example.com", "disabled": True, "comments": "Updated admin user"}

    # Simulate the existing admin data
    responses.add(
        method="GET",
        url=f"https://connector.zscaler.net/api/v1/adminUsers/{admin_id}",
        json=admin_users[0],
        status=200,
    )

    # Mock the update operation
    updated_admin = admin_users[0].copy()
    updated_admin.update(update_data)

    responses.add(
        method="PUT",
        url=f"https://connector.zscaler.net/api/v1/adminUsers/{admin_id}",
        json=updated_admin,
        status=200,
        match=[
            json_params_matcher(
                {
                    "role": "new_role",
                    "email": "newemail@example.com",
                    "disabled": True,
                    "comments": "Updated admin user",
                    "id": 1,
                    "name": "Admin1",
                }
            )
        ],
    )

    resp = zcon.admin.update_admin(admin_id, **update_data)
    assert isinstance(resp, Box)
    assert resp["id"] == admin_id
    assert resp["role"] == "new_role"
    assert resp["email"] == "newemail@example.com"
    assert resp["disabled"] is True
    assert resp["comments"] == "Updated admin user"


@responses.activate
def test_delete_admin(zcon):
    admin_id_to_delete = "123456789"
    responses.add(
        method="DELETE",
        url=f"https://connector.zscaler.net/api/v1/adminUsers/{admin_id_to_delete}",
        status=204,
    )

    resp = zcon.admin.delete_admin(admin_id_to_delete)
    assert isinstance(resp, int)
    assert resp == 204


@responses.activate
def test_change_password(zcon):
    username = "jdoe"
    old_password = "oldpassword123"
    new_password = "newpassword123"

    responses.add(
        method="POST",
        url="https://connector.zscaler.net/api/v1/passwordChange",
        status=200,
        match=[
            responses.json_params_matcher(
                {
                    "userName": username,
                    "oldPassword": old_password,
                    "newPassword": new_password,
                }
            )
        ],
    )

    resp = zcon.admin.change_password(username, old_password, new_password)
    assert isinstance(resp, int)
    assert resp == 200


@responses.activate
def test_list_api_keys(zcon, api_keys):
    params = {"includePartnerKeys": True}

    responses.add(
        method="GET",
        url="https://connector.zscaler.net/api/v1/apiKeys?includePartnerKeys=True",
        json=api_keys,
        status=200,
    )

    resp = zcon.admin.list_api_keys(include_partner_keys=True)
    assert isinstance(resp, list)
    assert len(resp) == len(api_keys)
    assert resp[0]["id"] == api_keys[0]["id"]
    assert resp[1]["id"] == api_keys[1]["id"]


@responses.activate
def test_regenerate_api_key(zcon, api_keys):
    api_key_id = 1  # or "1" if the ID is a string
    new_key_value = "newRegenKey"

    # Find the API key with the matching ID and change its 'keyValue'
    regenerated_api_key = next(key for key in api_keys if key["id"] == api_key_id)
    regenerated_api_key["keyValue"] = new_key_value

    responses.add(
        method="POST",
        url=f"https://connector.zscaler.net/api/v1/apiKeys/{api_key_id}/regenerate",
        json=regenerated_api_key,
        status=200,
    )

    resp = zcon.admin.regenerate_api_key(api_key_id)
    assert isinstance(resp, dict)
    assert resp["id"] == regenerated_api_key["id"]
    assert resp["keyValue"] == new_key_value
