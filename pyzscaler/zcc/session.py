from box import Box
from restfly.endpoint import APIEndpoint


class AuthenticatedSessionAPI(APIEndpoint):
    def create_token(self, client_id: str, client_secret: str) -> Box:
        """
        Creates a ZCC authentication token.

        Args:
            client_id (str): The ZCC Portal Client ID.
            client_secret (str): The ZCC Portal Client Secret.

        Returns:
            :obj:`Box`: The authenticated session information.

        Examples:
            >>> zia.session.create(api_key='999999999',
            ...    username='admin@example.com',
            ...    password='MyInsecurePassword')


        """

        payload = {
            "apiKey": client_id,
            "secretKey": client_secret,
        }

        return self._post("auth/v1/login", json=payload).jwt_token
