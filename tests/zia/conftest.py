import pytest
import responses

from pyzscaler.zia import ZIA


@pytest.fixture
@responses.activate
def zia():
    responses.add(
        responses.POST,
        url="https://zsapi.zscaler.net/api/v1/authenticatedSession",
        content_type="application/json",
        status=200,
    )
    return ZIA()
