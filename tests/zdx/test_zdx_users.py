import responses
from box import Box, BoxList


@responses.activate
def test_list_users(zdx):
    url = "https://api.zdxcloud.net/v1/users"
    mock_response = {"users": [{"id": 0, "name": "string", "email": "string"}], "next_offset": None}
    responses.add(responses.GET, url, json=mock_response, status=200)

    result = zdx.users.list_users()

    assert isinstance(result, BoxList)
    assert result == BoxList(mock_response["users"])


@responses.activate
def test_get_user(zdx):
    user_id = "999999999"
    url = f"https://api.zdxcloud.net/v1/users/{user_id}"
    mock_response = {
        "id": 0,
        "name": "string",
        "email": "string",
        "devices": [
            {
                "id": 0,
                "name": "string",
                "geo_loc": [
                    {
                        "id": "string",
                        "city": "string",
                        "state": "string",
                        "country": "string",
                        "geo_type": "string",
                        "geo_lat": "string",
                        "geo_long": "string",
                        "geo_detection": "string",
                    }
                ],
                "zs_loc": [{"id": 0, "name": "string"}],
            }
        ],
    }
    responses.add(responses.GET, url, json=mock_response, status=200)

    result = zdx.users.get_user(user_id)

    assert isinstance(result, Box)
    assert result == Box(mock_response)
