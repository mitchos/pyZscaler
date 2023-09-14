import responses


@responses.activate
def test_create(zcon, session):
    responses.add(
        responses.POST,
        url="https://connector.zscaler.net/api/v1/auth",
        json=session,
        status=200,
    )

    resp = zcon.session.create(api_key="test1234567890", username="test@example.com", password="hunter2")

    assert isinstance(resp, dict)
    assert resp.auth_type == "ADMIN_LOGIN"
    assert resp.obfuscate_api_key is False
    assert resp.password_expiry_time == 0
    assert resp.password_expiry_days == 0
