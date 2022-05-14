import responses


@responses.activate
def test_create_token(zcc, session):

    responses.add(
        responses.POST,
        url="https://api-mobile.zscaler.net/papi/auth/v1/login",
        json=session,
        status=200,
    )

    resp = zcc.session.create_token(client_id="abc123", client_secret="999999")

    assert isinstance(resp, str)
    assert resp == "ADMIN_LOGIN"
