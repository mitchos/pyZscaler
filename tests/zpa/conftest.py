import pytest
import responses

from pyzscaler.zpa import ZPA


@pytest.fixture(name="session")
def fixture_session():
    return {
        "token_type": "Bearer",
        "access_token": "xyz",
        "expires_in": 3600,
    }


@pytest.fixture(name="zpa")
@responses.activate
def zpa(session):
    responses.add(
        responses.POST,
        url="https://config.private.zscaler.com/signin",
        content_type="application/json",
        json=session,
        status=200,
    )
    return ZPA(
        client_id="1",
        client_secret="yyy",
        customer_id="1",
    )
