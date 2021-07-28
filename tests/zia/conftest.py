import pytest

from pyzscaler.zia import ZIA


@pytest.fixture
def zia():
    return ZIA()
