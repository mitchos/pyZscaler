from restfly.endpoint import APIEndpoint


class AppServersAPI(APIEndpoint):

    def add_server(self, name: str = None, address: str = None, enabled: bool = False, **kwargs):
        """
        Add a new application server.

        Args:
            name (str, required):
                The name of the server.
            address (str, required):
                The IP address of the server.
            enabled (bool, required):
                 Should the server be enabled. Defaults to False.
            **kwargs:

        Keyword Args:
            description (str, optional):
                A description for the server.
            appServerGroupIds (:obj:`list` of :obj:`str`), optional):
                Unique identifiers for the server groups the server belongs to.
            configSpace (str, optional):
                The configuration space for the server. Defaults to DEFAULT.

        Returns:
            :obj:`dict`: The resource record for the newly created server.

        Examples:
            Create a server with the minimum required parameters:

            >>> zpa.servers.add_server(
            ...   name='myserver.example',
            ...   address='192.0.2.10',
            ...   enabled=True)

        """
        payload = {
            "name": name,
            "address": address,
            "enabled": enabled,
            "description": kwargs.get('description', ''),
            "appServerGroupIds": kwargs.get('server_group_ids', []),
            "configSpace": kwargs.get('config_space', 'DEFAULT')
        }
        return self._post('server', json=payload)

    def list_servers(self):
        """
        Returns all configured servers.

        Returns:
            :obj:`list`: List of all configured servers.

        Examples:
            >>> servers = zpa.servers.list_servers()
        """
        return self._get('server').list

    def get_server(self, server_id: str):
        """
        Get information for the specified server id.

        Args:
            server_id (str):
                The unique identifier for the server.

        Returns:
            :obj:`dict`: The resource record for the server.

        Examples:
            >>> server = zpa.servers.get_server('12')

        """
        return self._get(f'server/{server_id}')

    def delete_server(self, server_id: str):
        """
        Delete the specified server.

        Args:
            server_id (str):
                The unique identifier for the server to be deleted.

        Returns:
            :obj:`str`: The response code for the operation.

        Examples:
            >>> zpa.servers.delete_server('32')

        """
        return self._delete(f'server/{server_id}')

    def update_server(self, server_id: str, **kwargs):
        """Updates the specified server

        Args:
            server_id (str):
                The unique identifier for the server being updated.
            **kwargs:

        Keyword Args:
            name (str, optional):
                The name of the server.
            address (str, optional):
                The IP address of the server.
            enabled (bool, optional):
                 Should the server be enabled.
            description (str, optional):
                A description for the server.
            appServerGroupIds (list(str), optional):
                Unique identifiers for the server groups the server belongs to.
            configSpace (str, optional):
                The configuration space for the server.

        Returns:
            :obj:`dict`: The resource record for the updated server.

        Examples:
            Update the name of a server:

            >>> zpa.servers.update_server(
            ...   '23483234823484',
            ...   name='newname.example')

            Update the address and enable a server:

            >>> zpa.servers.update_server(
            ...    '23483234823484',
            ...    address='192.0.2.20',
            ...    enabled=True)

        """
        payload = {
            'id': server_id
        }

        for key, value in kwargs.items():
            payload[key] = value

        return self._put(f'server/{server_id}', json=payload)
