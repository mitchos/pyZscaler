import pytest
import responses

from pyzscaler.zdx import ZDX


@pytest.fixture(name="session")
def fixture_session():
    return {
        "token": "ADMIN_LOGIN",
    }


@pytest.fixture(name="zdx")
@responses.activate
def zdx(session):
    responses.add(
        responses.POST,
        url="https://api.zdxcloud.net/v1/oauth/token",
        content_type="application/json",
        json=session,
        status=200,
    )

    return ZDX(
        client_id="abc123",
        client_secret="999999",
    )
