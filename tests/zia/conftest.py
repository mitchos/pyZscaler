import os

import pytest
import responses

from pyzscaler.zia import ZIA


@pytest.fixture
def zia():
    return ZIA()
