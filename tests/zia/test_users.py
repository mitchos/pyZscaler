import os

import pytest
from restfly.errors import APIError
from restfly.utils import check


@pytest.fixture(name="user")
def fixture_user(request, zia):
    """
    Fixture to create a user
    """
    domain = os.getenv("ZIA_TEST_DOMAIN")
    group_id = None
    dept_id = None

    # Use built-in Service Admin group for testing - always exists
    for group in zia.users.list_groups():
        if group.name == "Service Admin":
            group_id = group.id

    # Use built-in Service Admin department for testing - always exists
    for dept in zia.users.list_departments():
        if dept.name == "Service Admin":
            dept_id = dept.id

    user = zia.users.add_user(
        name="Test User",
        email=f"test.user@{domain}",
        groups=[{"id": group_id}],
        department={"id": dept_id},
    )

    def teardown():
        """ Cleanup function to delete user."""
        try:
            zia.users.delete_user(user.id)
        except APIError as err:
            print(err)

    request.addfinalizer(teardown)
    return user


def test_users_add_user(user):
    assert isinstance(user, dict)
    check("id", user["id"], int)
    check("name", user["name"], str)
    check("email", user["email"], str)
    assert isinstance(user["groups"], list)
    for group in user["groups"]:
        check("group_id", group["id"], int)


def test_users_get_user(user, zia):
    test_user = zia.users.get_user(user.id)
    check("id", test_user["id"], int)
    check("name", test_user["name"], str)
    check("email", test_user["email"], str)
    assert isinstance(test_user["groups"], list)
    for group in test_user["groups"]:
        check("group_id", group["id"], int)
        check("group_name", group["name"], str)
    check("department", test_user["department"], dict)
    check("admin_user", test_user["admin_user"], bool)
    if "is_non_editable" in test_user and test_user["is_non_editable"]:
        check("is_non_editable", test_user["is_non_editable"], bool)
    check("deleted", test_user["deleted"], bool)
    if "temp_auth_email" in test_user and test_user["temp_auth_email"]:
        check("temp_auth_email", test_user["temp_auth_email"], str)


def test_users_update_user(user, zia):
    updated_name = "updated_test_name"
    updated_user = zia.users.update_user(user.id, name=updated_name)

    check("id", updated_user["id"], int)
    check("name", updated_user["name"], str)
    assert updated_user["name"] == updated_name
    check("email", updated_user["email"], str)
    assert isinstance(updated_user["groups"], list)
    for group in updated_user["groups"]:
        check("group_id", group["id"], int)
        check("group_name", group["name"], str)
    check("department", updated_user["department"], dict)
    check("admin_user", updated_user["admin_user"], bool)
    check("deleted", updated_user["deleted"], bool)
    if "temp_auth_email" in updated_user and updated_user["temp_auth_email"]:
        check("temp_auth_email", updated_user["temp_auth_email"], str)


def test_users_list_users(zia):
    users = zia.users.list_users()
    assert isinstance(users, list)
    for user in users:
        assert isinstance(user, dict)
        check("id", user["id"], int)
        check("name", user["name"], str)
        check("email", user["email"], str)
        assert isinstance(user["groups"], list)
        for group in user["groups"]:
            check("group_id", group["id"], int)
            check("group_name", group["name"], str)
        # check("department", user["department"], dict)
        check("admin_user", user["admin_user"], bool)
        check("is_non_editable", user["is_non_editable"], bool)
        check("deleted", user["deleted"], bool)
        if "temp_auth_email" in user and user["temp_auth_email"]:
            check("temp_auth_email", user["temp_auth_email"], str)


def test_users_list_groups(zia):
    groups = zia.users.list_groups()
    assert isinstance(groups, list)
    for group in groups:
        check("group", group, dict)
        check("id", group["id"], int)
        check("name", group["name"], str)
        if "is_non_editable" in group and group["is_non_editable"]:
            check("is_non_editable", group["is_non_editable"], bool)


def test_users_list_departments(zia):
    departments = zia.users.list_departments()
    assert isinstance(departments, list)
    for department in departments:
        check("department", department, dict)
        check("id", department["id"], int)
        check("name", department["name"], str)
        if "is_non_editable" in department and department["is_non_editable"]:
            check("is_non_editable", department["is_non_editable"], bool)


def test_users_get_group(zia):
    group_id = zia.users.list_groups()[0].id
    group = zia.users.get_group(group_id)
    check("group", group, dict)
    check("id", group["id"], int)
    check("name", group["name"], str)
    if "is_non_editable" in group and group["is_non_editable"]:
        check("is_non_editable", group["is_non_editable"], bool)


def test_users_get_department(zia):
    department_id = zia.users.list_departments()[0].id
    department = zia.users.get_department(department_id)
    check("department", department, dict)
    check("id", department["id"], int)
    check("name", department["name"], str)
    if "is_non_editable" in department and department["is_non_editable"]:
        check("is_non_editable", department["is_non_editable"], bool)


def test_users_delete_user(user, zia):
    resp = zia.users.delete_user(user.id)
    check("response", resp, int)
    assert resp == 204