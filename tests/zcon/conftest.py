import pytest
import responses

from pyzscaler.zcon import ZCON


@pytest.fixture(name="session")
def fixture_session():
    return {
        "authType": "ADMIN_LOGIN",
        "obfuscateApiKey": False,
        "passwordExpiryTime": 0,
        "passwordExpiryDays": 0,
    }


@pytest.fixture(name="zcon")
@responses.activate
def zcon(session):
    responses.add(
        responses.POST,
        url="https://connector.zscaler.net/api/v1/auth",
        content_type="application/json",
        json=session,
        status=200,
    )
    return ZCON(
        username="test@example.com",
        password="hunter2",
        cloud="zscaler",
        api_key="123456789abcdef",
    )
