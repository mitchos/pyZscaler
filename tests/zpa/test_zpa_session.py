import responses
from responses import matchers


@responses.activate
def test_create_token(zpa, session):
    responses.add(
        responses.POST,
        url="https://config.private.zscaler.com/signin",
        json=session,
        status=200,
        match=[
            matchers.urlencoded_params_matcher(
                {
                    "client_id": "1",
                    "client_secret": "yyy",
                }
            ),
            matchers.header_matcher({"Content-Type": "application/x-www-form-urlencoded"}),
        ],
    )

    resp = zpa.session.create_token(client_id="1", client_secret="yyy")

    assert isinstance(resp, str)
    assert resp == "xyz"
