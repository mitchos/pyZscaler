import pytest
import responses
from box import Box


@pytest.fixture(name="activate_status")
def fixture_activate_status():
    return {"status": 200}


@pytest.fixture(name="status_data")
def fixture_status_data():
    return {
        "status": "Active",
    }


@responses.activate
def test_activate_min_args(zcon, activate_status):
    responses.add(
        method="POST",
        url="https://connector.zscaler.net/api/v1/ecAdminActivateStatus/activate",
        json=activate_status,
        status=200,
    )

    resp = zcon.config.activate()
    assert isinstance(resp, Box)
    assert resp["status"] == 200


@responses.activate
def test_force_activate(zcon, activate_status):
    responses.add(
        method="POST",
        url="https://connector.zscaler.net/api/v1/ecAdminActivateStatus/forcedActivate",
        json=activate_status,
        status=200,
    )

    resp = zcon.config.activate(force=True)
    assert isinstance(resp, Box)
    assert resp["status"] == 200


@responses.activate
def test_get_status(zcon, status_data):
    responses.add(
        method="GET",
        url="https://connector.zscaler.net/api/v1/ecAdminActivateStatus",
        json=status_data,
        status=200,
    )

    resp = zcon.config.get_status()
    assert isinstance(resp, Box)
    assert resp["status"] == "Active"
