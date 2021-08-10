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
            >>> zpa.session.create(client_id='Eh3UzT7E2RXkjCkYQMbVF9jWDJNY4geM6bMp6NXxxCkzjjf77B7YpYMMuGhb==',
            ...    client_secret='fvWHWSC(Z%]7AbmVH%qR%Yt;iUG89Z')

        """

        payload = {"client_id": client_id, "client_secret": client_secret}

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        return self._post(
            "https://config.private.zscaler.com/signin", headers=headers, data=payload
        ).access_token

    def delete(self):
        """
        Deletes the ZPA authentication session.

        Returns:
            :obj:`str`: The status code of the operation.

        Examples:
            >>> zpa.session.delete()

        """
        return self._post("https://config.private.zscaler.com/signout")
