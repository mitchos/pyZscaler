import responses
from box import Box

from tests.conftest import stub_sleep


@responses.activate
def test_create_token(zdx):
    client_id = "999999999"
    client_secret = "admin@example.com"
    url = "https://api.zdxcloud.net/v1/oauth/token"
    mock_response = {"token": "test_token", "token_type": "Bearer", "expires_in": 3600}
    responses.add(responses.POST, url, json=mock_response, status=200)

    result = zdx.session.create_token(client_id, client_secret)

    assert isinstance(result, Box)
    assert result.token == mock_response["token"]
    assert result.token_type == mock_response["token_type"]
    assert result.expires_in == mock_response["expires_in"]


@responses.activate
@stub_sleep
def test_validate_token(zdx):
    url = "https://api.zdxcloud.net/v1/oauth/validate"
    mock_response = {"valid": True}
    responses.add(responses.GET, url, json=mock_response, status=200)

    result = zdx.session.validate_token()

    assert isinstance(result, Box)
    assert result.valid == mock_response["valid"]


@responses.activate
def test_get_jwks(zdx):
    url = "https://api.zdxcloud.net/v1/oauth/jwks"
    mock_response = {
        "keys": [{"alg": "RS256", "kty": "RSA", "use": "sig", "x5c": ["test_string"], "kid": "test_kid", "x5t": "test_x5t"}]
    }
    responses.add(responses.GET, url, json=mock_response, status=200)

    result = zdx.session.get_jwks()

    assert isinstance(result, Box)
    assert result.get("keys")[0].get("alg") == mock_response["keys"][0]["alg"]
