from restfly.endpoint import APIEndpoint
from pyzscaler.utils import obfuscate_api_key


class AuthenticatedSessionAPI(APIEndpoint):
    def status(self):
        """
        Returns the status of the authentication session if it exists.

        Returns:
            :obj:`dict`: Session authentication information.

        Examples:
            >>> print(zia.session.status())

        """
        return self._get("authenticatedSession")

    def create(self, api_key: str, username: str, password: str):
        """
        Creates a ZIA authentication session.

        Args:
            api_key (str): The ZIA API Key.
            username (str): Username of admin user for the authentication session.
            password (str): Password of the admin user for the authentication session.

        Returns:
            :obj:`dict`: The authenticated session information.

        Examples:
            >>> zia.session.create(api_key='12khsdfh3289',
            ...    username='admin@example.com',
            ...    password='MyInsecurePassword')


        """
        api_obf = obfuscate_api_key(api_key)

        payload = {
            "apiKey": api_obf["key"],
            "username": username,
            "password": password,
            "timestamp": api_obf["timestamp"],
        }

        return self._post("authenticatedSession", json=payload)

    def delete(self):
        """
        Ends an authentication session.

        Returns:
            :obj:`str`: The status code of the operation.

        Examples:
            >>> zia.session.delete()

        """
        return self._delete("authenticatedSession", box=False).status_code
