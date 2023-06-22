import time
from hashlib import sha256

from box import Box
from restfly.endpoint import APIEndpoint


class SessionAPI(APIEndpoint):
    def create_token(self, client_id: str, client_secret: str) -> Box:
        """
        Creates a ZDX authentication token.

        Args:
            client_id (str): The ZDX API Key ID.
            client_secret (str): The ZDX API Key Secret.

        Returns:
            :obj:`Box`: The authenticated session information.

        Examples:
            >>> zia.session.create(client_id='999999999',
            ...    client_secret='admin@example.com')

        """
        epoch_time = int(time.time())

        # Zscaler requires the API Secret Key to be appended with the epoch timestamp, separated by a colon. We then
        # need to take the SHA256 hash of this string and pass that as the API Secret Key.
        api_secret_format = f"{client_secret}:{epoch_time}"
        api_secret_hash = sha256(api_secret_format.encode("utf-8")).hexdigest()

        payload = {"key_id": client_id, "key_secret": api_secret_hash, "timestamp": epoch_time}

        return self._post("oauth/token", json=payload)

    def validate_token(self):
        """
        Validates the current ZDX JWT token.

        Returns:
            :obj:`Box`: The validated session information.

        Examples:
            >>> validation = zdx.session.validate()

        """
        return self._get("oauth/validate")

    def get_jwks(self):
        """
        Returns a JSON Web Key Set (JWKS) that contains the public keys that can be used to verify the JWT tokens.

        Returns:
            :obj:`Box`: The JSON Web Key Set (JWKS).

        Examples:
            >>> jwks = zdx.session.get_jwks()

        """
        return self._get("oauth/jwks")
