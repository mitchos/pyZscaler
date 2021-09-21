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
    return ZIA(
        username="test@example.com",
        password="hunter2",
        cloud="zscaler",
        api_key="123456789abcdef",
    )


@pytest.fixture(name="paginated_items")
def fixture_pagination_items():
    def _method(num):
        items = []
        for x in range(0, num):
            items.append({"id": x})
        return items

    return _method
