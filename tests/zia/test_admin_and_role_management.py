# FIXME: This whole file isn't working as I don't know how, yet, to write a test.  Basically I've copy/pasted test_users.py.
import pytest
import responses
from responses import matchers

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
