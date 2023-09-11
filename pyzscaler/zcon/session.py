from box import Box
from restfly import APIEndpoint

from pyzscaler.utils import obfuscate_api_key


class AuthenticationAPI(APIEndpoint):
    def status(self) -> Box:
        """
        Returns the status of the authentication session if it exists.

        Returns:
            :obj:`Box`: Session authentication information.

        Examples:
            >>> print(zcon.session.status())

        """
        return self._get("auth")

    def create(self, api_key: str, username: str, password: str) -> Box:
        """
        Create a new ZCON authentication session.

        Args:
            api_key (str): The ZCON API Key.
            username (str): Username of admin user for the authentication session.
            password (str): Password of the admin user for the authentication session.

        Returns:
            :obj:`dict`: The authenticated session information.

        Examples:
            >>> zia.session.create(api_key='123456789',
            ...     username='admin@example.com'
            ...     password='MyInsecurePassword')

        """
        api_obf = obfuscate_api_key(api_key)

        payload = {
            "apiKey": api_obf["key"],
            "username": username,
            "password": password,
            "timestamp": api_obf["timestamp"],
        }
        return self._post("auth", json=payload)

    def delete(self) -> int:
        """
        End the authentication session.

        Returns:
            :obj:`int`: The status code of the operation.

        """
        return self._delete("auth").status
