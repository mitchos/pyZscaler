from restfly.endpoint import APIEndpoint


class AuthenticatedSessionAPI(APIEndpoint):
    def create_token(self, client_id, client_secret):
        """
        Creates a ZPA authentication token.

        Args:
            client_id (str): The ZPA API Client ID.
            client_secret (str): The ZPA API Client Secret Key.

        Returns:
            :obj:`dict`: The authenticated session information.

        Examples:
            >>> zpa.session.create(client_id='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx==',
            ...    client_secret='yyyyyyyyyyyyyyyyyyyyyyyyyyyyyy')

        """

        payload = {"client_id": client_id, "client_secret": client_secret}

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        return self._post("https://config.private.zscaler.com/signin", headers=headers, data=payload).access_token
