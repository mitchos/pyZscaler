import pytest
import responses
from responses import matchers

from tests.conftest import stub_sleep


@pytest.fixture(name="users")
def fixture_users():
    return [
        {
            "id": 1,
            "name": "Test User A",
            "email": "testusera@example.com",
            "groups": {"id": 1, "name": "test"},
            "department": {"id": 1, "name": "test_department"},
            "comments": "Test",
            "adminUser": False,
            "isNonEditable": False,
            "disabled": False,
            "deleted": False,
        },
        {
            "id": 2,
            "name": "Test User B",
            "email": "testuserb@example.com",
            "groups": {"id": 1, "name": "test"},
            "department": {"id": 1, "name": "test_department"},
            "adminUser": True,
            "isNonEditable": False,
            "disabled": True,
            "deleted": False,
        },
    ]


@pytest.fixture(name="groups")
def fixture_groups():
    return [{"id": 1, "name": "Group A"}, {"id": 2, "name": "Group B"}]


@pytest.fixture(name="departments")
def fixture_depts():
    return [{"id": 1, "name": "Dept A"}, {"id": 2, "name": "Dept B"}]


@responses.activate
def test_users_add_user(zia, users):
    responses.add(
        method="POST",
        url="https://zsapi.zscaler.net/api/v1/users",
        json=users[0],
        status=200,
        match=[
            matchers.json_params_matcher(
                {
                    "name": "Test User A",
                    "email": "testusera@example.com",
                    "groups": {"id": "1"},
                    "department": {"id": "1"},
                    "comments": "Test",
                }
            )
        ],
    )

    resp = zia.users.add_user(
        name="Test User A",
        email="testusera@example.com",
        groups={"id": "1"},
        department={"id": "1"},
        comments="Test",
    )

    assert isinstance(resp, dict)
    assert resp.id == 1
    assert resp.admin_user is False
    assert resp.comments == "Test"


@responses.activate
def test_users_get_user(users, zia):
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/users/1",
        json=users[0],
        status=200,
    )
    resp = zia.users.get_user("1")

    assert isinstance(resp, dict)
    assert resp.id == 1


@responses.activate
def test_users_update_user(zia, users):
    updated_user = users[0]
    updated_user["name"] = "Test User C"
    updated_user["comments"] = "Updated Test"

    responses.add(
        responses.GET,
        "https://zsapi.zscaler.net/api/v1/users/1",
        json=users[0],
        status=200,
    )

    responses.add(
        responses.PUT,
        url="https://zsapi.zscaler.net/api/v1/users/1",
        json=updated_user,
        match=[
            matchers.json_params_matcher(
                {
                    "name": updated_user["name"],
                    "email": updated_user["email"],
                    "groups": updated_user["groups"],
                    "department": updated_user["department"],
                    "comments": updated_user["comments"],
                }
            )
        ],
    )

    resp = zia.users.update_user("1", name="Test User C", comments="Updated Test")

    assert isinstance(resp, dict)


@responses.activate
@stub_sleep
def test_list_users_with_one_page(zia, paginated_items):
    items = paginated_items(200)

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/users",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/users",
        json=items[100:200],
        status=200,
    )

    resp = zia.users.list_users(max_pages=1, page_size=100)

    assert isinstance(resp, list)
    assert resp[50].id == 50
    assert len(resp) == 100


@responses.activate
@stub_sleep
def test_list_users_with_two_pages(zia, paginated_items):
    items = paginated_items(200)

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/users",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/users",
        json=items[100:200],
        status=200,
    )

    resp = zia.users.list_users(max_pages=2, page_size=100)

    assert isinstance(resp, list)
    assert resp[50].id == 50
    assert resp[150].id == 150
    assert len(resp) == 200


@responses.activate
@stub_sleep
def test_list_users_with_max_items_1(zia, paginated_items):
    items = paginated_items(200)

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/users",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/users",
        json=items[100:200],
        status=200,
    )

    resp = zia.users.list_users(max_items=1)

    assert isinstance(resp, list)
    assert len(resp) == 1


@responses.activate
@stub_sleep
def test_list_users_with_max_items_150(zia, paginated_items):
    items = paginated_items(200)

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/users",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/users",
        json=items[100:200],
        status=200,
    )

    resp = zia.users.list_users(max_items=150)

    assert isinstance(resp, list)
    assert len(resp) == 150


@responses.activate
@stub_sleep
def test_list_groups_with_one_page(zia, paginated_items):
    items = paginated_items(200)

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/groups",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/groups",
        json=items[100:200],
        status=200,
    )

    resp = zia.users.list_groups(max_pages=1, page_size=100)

    assert isinstance(resp, list)
    assert resp[50].id == 50
    assert len(resp) == 100


@responses.activate
@stub_sleep
def test_list_groups_with_two_pages(zia, paginated_items):
    items = paginated_items(200)

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/groups",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/groups",
        json=items[100:200],
        status=200,
    )

    resp = zia.users.list_groups(max_pages=2, page_size=100)

    assert isinstance(resp, list)
    assert resp[50].id == 50
    assert resp[150].id == 150
    assert len(resp) == 200


@responses.activate
@stub_sleep
def test_list_groups_with_max_items_1(zia, paginated_items):
    items = paginated_items(200)

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/groups",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/groups",
        json=items[100:200],
        status=200,
    )

    resp = zia.users.list_groups(max_items=1)

    assert isinstance(resp, list)
    assert len(resp) == 1


@responses.activate
@stub_sleep
def test_list_groups_with_max_items_150(zia, paginated_items):
    items = paginated_items(200)

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/groups",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/groups",
        json=items[100:200],
        status=200,
    )

    resp = zia.users.list_groups(max_items=150)

    assert isinstance(resp, list)
    assert len(resp) == 150


@responses.activate
def test_users_get_group(zia, groups):
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/groups/1",
        json=groups[0],
        status=200,
    )

    resp = zia.users.get_group("1")

    assert isinstance(resp, dict)
    assert resp.id == 1


@responses.activate
@stub_sleep
def test_list_departments_with_one_page(zia, paginated_items):
    items = paginated_items(200)

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/departments",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/departments",
        json=items[100:200],
        status=200,
    )

    resp = zia.users.list_departments(max_pages=1, page_size=100)

    assert isinstance(resp, list)
    assert resp[50].id == 50
    assert len(resp) == 100


@responses.activate
@stub_sleep
def test_list_departments_with_two_pages(zia, paginated_items):
    items = paginated_items(200)

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/departments",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/departments",
        json=items[100:200],
        status=200,
    )

    resp = zia.users.list_departments(max_pages=2, page_size=100)

    assert isinstance(resp, list)
    assert resp[50].id == 50
    assert resp[150].id == 150
    assert len(resp) == 200


@responses.activate
@stub_sleep
def test_list_departments_with_max_items_1(zia, paginated_items):
    items = paginated_items(200)

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/departments",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/departments",
        json=items[100:200],
        status=200,
    )

    resp = zia.users.list_departments(max_items=1)

    assert isinstance(resp, list)
    assert len(resp) == 1


@responses.activate
@stub_sleep
def test_list_departments_with_max_items_150(zia, paginated_items):
    items = paginated_items(200)

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/departments",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/departments",
        json=items[100:200],
        status=200,
    )

    resp = zia.users.list_departments(max_items=150)

    assert isinstance(resp, list)
    assert len(resp) == 150


@responses.activate
def test_users_get_department(zia, departments):
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/departments/1",
        json=departments[0],
        status=200,
    )

    resp = zia.users.get_department("1")

    assert isinstance(resp, dict)
    assert resp.id == 1


@responses.activate
def test_users_delete_user(zia):
    responses.add(method="DELETE", url="https://zsapi.zscaler.net/api/v1/users/1", status=204)
    resp = zia.users.delete_user("1")
    assert resp == 204


@responses.activate
def test_users_bulk_delete_users(zia):
    user_ids = ["1", "2"]
    responses.add(
        responses.POST,
        url="https://zsapi.zscaler.net/api/v1/users/bulkDelete",
        status=204,
        json={"ids": user_ids},
        match=[matchers.json_params_matcher({"ids": user_ids})],
    )
    resp = zia.users.bulk_delete_users(["1", "2"])
    assert isinstance(resp, dict)
    assert resp.ids == ["1", "2"]
