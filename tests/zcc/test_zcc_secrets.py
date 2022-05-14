import pytest
import responses
from box import Box
from responses import matchers


@responses.activate
def test_get_otp(zcc):
    responses.add(
        method="GET",
        url="https://api-mobile.zscaler.net/papi/public/v1/getOtp",
        json={"otp": "123abc"},
        match=[matchers.query_param_matcher({"udid": "999999"})],
        status=200,
    )
    resp = zcc.secrets.get_otp("999999")

    assert isinstance(resp, Box)
    assert resp.otp == "123abc"


@responses.activate
def test_get_passwords_default(zcc):
    responses.add(
        method="GET",
        url="https://api-mobile.zscaler.net/papi/public/v1/getPasswords",
        json={
            "logout_pass": "test",
            "exit_pass": "test",
            "zia_disable_pass": "test",
            "zpa_disable_pass": "test",
            "zdx_disable_pass": "test",
            "uninstall_pass": "test",
        },
        match=[matchers.query_param_matcher({"username": "test@example.com", "osType": 3})],
        status=200,
    )
    resp = zcc.secrets.get_passwords("test@example.com")

    assert isinstance(resp, Box)
    assert resp.logout_pass == "test"


@responses.activate
def test_get_passwords_os_type(zcc):
    responses.add(
        method="GET",
        url="https://api-mobile.zscaler.net/papi/public/v1/getPasswords",
        json={
            "logout_pass": "test",
            "exit_pass": "test",
            "zia_disable_pass": "test",
            "zpa_disable_pass": "test",
            "zdx_disable_pass": "test",
            "uninstall_pass": "test",
        },
        match=[matchers.query_param_matcher({"username": "test@example.com", "osType": 1})],
        status=200,
    )
    resp = zcc.secrets.get_passwords("test@example.com", os_type="ios")

    assert isinstance(resp, Box)
    assert resp.logout_pass == "test"


@responses.activate
def test_get_passwords_error(zcc):
    with pytest.raises(Exception) as e_info:
        resp = zcc.secrets.get_passwords("test@example.com", os_type="unix")
