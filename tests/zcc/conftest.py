import pytest
import responses

from pyzscaler.zcc import ZCC


@pytest.fixture(name="session")
def fixture_session():
    return {
        "jwtToken": "ADMIN_LOGIN",
    }


@pytest.fixture(name="zcc")
@responses.activate
def zcc(session):
    responses.add(
        responses.POST,
        url="https://api-mobile.zscaler.net/papi/auth/v1/login",
        content_type="application/json",
        json=session,
        status=200,
    )
    return ZCC(
        client_id="abc123",
        client_secret="999999",
        cloud="zscaler",
    )
