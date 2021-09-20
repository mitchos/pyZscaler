import pytest
import responses


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
            responses.json_params_matcher(
                {
                    "name": "Test User A",
                    "email": "testusera@example.com",
                    "groups": {"id": "1"},
                    "department": {"id": "1"},
                    "comments": "Test"
                }
            )
        ],
    )

    resp = zia.users.add_user(
        name="Test User A",
        email="testusera@example.com",
        groups={"id": "1"},
        department={"id": "1"},
        comments="Test"
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
            responses.json_params_matcher(
                {
                    "name": updated_user["name"],
                    "email": updated_user["email"],
                    "groups": updated_user["groups"],
                    "department": updated_user["department"],
                    "comments": updated_user["comments"]
                }
            )
        ],
    )

    resp = zia.users.update_user("1", name="Test User C", comments="Updated Test")

    assert isinstance(resp, dict)


@responses.activate
def test_users_list_users(zia, users):
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/users",
        json=users,
        status=200,
    )
    resp = zia.users.list_users(max_items=2)
    assert isinstance(resp, list)
    assert len(resp) == 2
    for user in resp:
        assert isinstance(user, dict)


@responses.activate
def test_users_list_groups(zia, groups):
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/groups",
        json=groups,
        status=200,
    )

    resp = zia.users.list_groups(max_items=2)
    assert isinstance(resp, list)
    for group in resp:
        assert isinstance(group, dict)
        assert isinstance(group.id, int)


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
def test_users_list_departments(zia, departments):
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/departments",
        json=departments,
        status=200,
    )

    resp = zia.users.list_departments(max_items=2)

    assert isinstance(resp, list)
    for dept in resp:
        assert isinstance(dept, dict)
        assert isinstance(dept.id, int)


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
    responses.add(
        method="DELETE", url="https://zsapi.zscaler.net/api/v1/users/1", status=204
    )
    resp = zia.users.delete_user("1")
    assert resp == 204


@responses.activate
def test_users_bulk_delete_users(zia):
    user_ids = ['1', '2']
    responses.add(
        responses.POST,
        url="https://zsapi.zscaler.net/api/v1/users/bulkDelete",
        status=204,
        json={
            'ids': user_ids
        },
        match=[
            responses.json_params_matcher({
                "ids": user_ids
            })
        ]
    )
    resp = zia.users.bulk_delete_users(['1', '2'])
    assert isinstance(resp, dict)
    assert resp.ids == ['1', '2']
