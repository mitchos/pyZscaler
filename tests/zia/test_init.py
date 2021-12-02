import responses


@responses.activate
def test_zia_deauthenticate(zia):
    responses.add(
        responses.DELETE,
        url="https://zsapi.zscaler.net/api/v1/authenticatedSession",
        content_type="application/json",
        status=200,
    )
    with zia:
        pass
