import pytest
import responses
from box import BoxList
from responses import matchers


@pytest.fixture(name="admin_users")
def fixture_users():
    return [
        {
            "loginName": "testuser@example.com",
            "userName": "Test User",
            "id": 1,
            "role": {"id": 1, "name": "Test"},
            "email": "testuser@example.com",
            "adminScopeType": "ORGANIZATION",
            "isDefaultAdmin": False,
            "isAuditor": False,
            "password": "hunter2",
            "isPasswordLoginAllowed": True,
            "isPasswordExpired": False,
            "newLocationCreateAllowed": False,
            "disabled": False,
        },
        {
            "loginName": "testuserb@example.com",
            "userName": "Test User B",
            "id": 2,
            "role": {"id": 2, "name": "Test"},
            "email": "testuserb@example.com",
            "adminScopeType": "ORGANIZATION",
            "isDefaultAdmin": False,
            "isAuditor": False,
            "password": "hunter2",
            "isPasswordLoginAllowed": True,
            "isPasswordExpired": False,
            "newLocationCreateAllowed": False,
            "disabled": False,
        },
    ]


@responses.activate
def test_admin_users_add_user(zia, admin_users):
    responses.add(
        method="POST",
        url="https://zsapi.zscaler.net/api/v1/adminUsers",
        json=admin_users[0],
        status=200,
        match=[
            matchers.json_params_matcher(
                {
                    "userName": "Test User",
                    "email": "testuser@example.com",
                    "role": {"id": "1"},
                    "password": "hunter2",
                    "loginName": "testuser@example.com",
                    "comments": "Test",
                }
            )
        ],
    )

    resp = zia.admin_and_role_management.add_user(
        name="Test User",
        email="testuser@example.com",
        login_name="testuser@example.com",
        password="hunter2",
        role_id="1",
        comments="Test",
    )

    assert isinstance(resp, dict)
    assert resp.role.id == 1
    assert resp.admin_scope_type == "ORGANIZATION"


@responses.activate
def test_admin_users_update_user(zia, admin_users):
    updated_user = admin_users[0]
    updated_user["userName"] = "Test Updated"
    updated_user["comments"] = "Updated Test"
    updated_user["adminScopeType"] = "DEPARTMENT"
    updated_user["adminScopeScopeEntities"] = [{"id": "1"}, {"id": "2"}]

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/adminUsers?page=1",
        json=admin_users,
        status=200,
    )

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/adminUsers?page=2",
        json=[],
        status=200,
    )

    responses.add(
        responses.PUT,
        url="https://zsapi.zscaler.net/api/v1/adminUsers/1",
        json=updated_user,
        match=[matchers.json_params_matcher(updated_user)],
    )

    resp = zia.admin_and_role_management.update_user(
        "1", name="Test Updated", comments="Updated Test", admin_scope="department", scope_ids=["1", "2"]
    )

    assert isinstance(resp, dict)


@responses.activate
def test_list_admin_users_with_one_page(zia, paginated_items):
    items = paginated_items(200)

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/adminUsers",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/adminUsers",
        json=items[100:200],
        status=200,
    )

    resp = zia.admin_and_role_management.list_users(max_pages=1, page_size=100)

    assert isinstance(resp, BoxList)
    assert resp[50].id == 50
    assert len(resp) == 100


@responses.activate
def test_list_admin_users_with_two_pages(zia, paginated_items):
    items = paginated_items(200)

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/adminUsers",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/adminUsers",
        json=items[100:200],
        status=200,
    )

    resp = zia.admin_and_role_management.list_users(max_pages=2, page_size=100)

    assert isinstance(resp, BoxList)
    assert resp[50].id == 50
    assert resp[150].id == 150
    assert len(resp) == 200


@responses.activate
def test_list_admin_users_with_max_items_1(zia, paginated_items):
    items = paginated_items(200)

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/adminUsers",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/adminUsers",
        json=items[100:200],
        status=200,
    )

    resp = zia.admin_and_role_management.list_users(max_items=1)

    assert isinstance(resp, BoxList)
    assert len(resp) == 1


@responses.activate
def test_list_admin_users_with_max_items_150(zia, paginated_items):
    items = paginated_items(200)

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/adminUsers",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/adminUsers",
        json=items[100:200],
        status=200,
    )

    resp = zia.admin_and_role_management.list_users(max_items=150)

    assert isinstance(resp, BoxList)
    assert len(resp) == 150


@responses.activate
def test_admin_users_get_user(admin_users, zia):
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/adminUsers?page=1",
        json=admin_users,
        status=200,
    )
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/adminUsers?page=2",
        json=[],
        status=200,
    )
    resp = zia.admin_and_role_management.get_user("1")

    assert isinstance(resp, dict)
    assert resp.id == 1


@responses.activate
def test_admin_users_delete_user(zia):
    responses.add(method="DELETE", url="https://zsapi.zscaler.net/api/v1/adminUsers/1", status=204)
    resp = zia.admin_and_role_management.delete_user("1")

    assert resp == 204
