from restfly import APISession
from restfly.endpoint import APIEndpoint


class AuthenticatedSessionAPI(APIEndpoint):
    def __init__(self, api: APISession):
        super().__init__(api)

        self.url_base = api.url_base

    def create_token(self, client_id: str, client_secret: str):
        """
        Creates a ZPA authentication token.

        Args:
            client_id (str): The ZPA API Client ID.
            client_secret (str): The ZPA API Client Secret Key.

        Returns:
            :obj:`dict`: The authenticated session information.

        Examples:
            >>> zpa.session.create_token(client_id='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx==',
            ...    client_secret='yyyyyyyyyyyyyyyyyyyyyyyyyyyyyy')

        """

        payload = {"client_id": client_id, "client_secret": client_secret}

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        return self._post(f"{self.url_base}/signin", headers=headers, data=payload).access_token
