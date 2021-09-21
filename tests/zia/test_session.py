import pytest
import responses


@pytest.fixture(name="session")
def fixture_session():
    return {
        "authType": "ADMIN_LOGIN",
        "obfuscateApiKey": False,
        "passwordExpiryTime": 0,
        "passwordExpiryDays": 0,
    }


@responses.activate
def test_create(zia, session):

    responses.add(
        responses.POST,
        url="https://zsapi.zscaler.net/api/v1/authenticatedSession",
        json=session,
        status=200,
    )

    resp = zia.session.create(
        api_key="test1234567890", username="test@example.com", password="hunter2"
    )

    assert isinstance(resp, dict)
    assert resp.auth_type == "ADMIN_LOGIN"
    assert resp.obfuscate_api_key is False
    assert resp.password_expiry_time == 0
    assert resp.password_expiry_days == 0


@responses.activate
def test_status(zia, session):
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/authenticatedSession",
        json=session,
        status=200,
    )

    resp = zia.session.status()

    assert isinstance(resp, dict)
    assert resp.auth_type == "ADMIN_LOGIN"
    assert resp.obfuscate_api_key is False
    assert resp.password_expiry_time == 0
    assert resp.password_expiry_days == 0


@responses.activate
def test_delete(zia):
    delete_status = {"status": "ACTIVE"}
    responses.add(
        responses.DELETE,
        url="https://zsapi.zscaler.net/api/v1/authenticatedSession",
        json=delete_status,
        status=200,
    )

    resp = zia.session.delete()

    assert isinstance(resp, int)
    assert resp == 200
