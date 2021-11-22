from box import Box, BoxList
from restfly.endpoint import APIEndpoint

from pyzscaler.utils import Iterator, snake_to_camel


class AppServersAPI(APIEndpoint):
    def add_server(self, name: str, address: str, enabled: bool = False, **kwargs) -> Box:
        """
        Add a new application server.

        Args:
            name (str):
                The name of the server.
            address (str):
                The IP address of the server.
            enabled (bool):
                 Enable the server. Defaults to False.
            **kwargs:
                Optional keyword args.

        Keyword Args:
            description (str):
                A description for the server.
            app_server_group_ids (list):
                Unique identifiers for the server groups the server belongs to.
            config_space (str):
                The configuration space for the server. Defaults to DEFAULT.

        Returns:
            :obj:`Box`: The resource record for the newly created server.

        Examples:
            Create a server with the minimum required parameters:

            >>> zpa.servers.add_server(
            ...   name='myserver.example',
            ...   address='192.0.2.10',
            ...   enabled=True)

        """
        payload = {"name": name, "address": address, "enabled": enabled}

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        return self._post("server", json=payload)

    def list_servers(self, **kwargs) -> BoxList:
        """
        Returns all configured servers.

        Keyword Args:
            **max_items (int):
                The maximum number of items to request before stopping iteration.
            **max_pages (int):
                The maximum number of pages to request before stopping iteration.
            **pagesize (int):
                Specifies the page size. The default size is 20, but the maximum size is 500.
            **search (str, optional):
                The search string used to match against features and fields.

        Returns:
            :obj:`BoxList`: List of all configured servers.

        Examples:
            >>> servers = zpa.servers.list_servers()
        """
        return BoxList(Iterator(self._api, "server", **kwargs))

    def get_server(self, server_id: str) -> Box:
        """
        Gets information on the specified server.

        Args:
            server_id (str):
                The unique identifier for the server.

        Returns:
            :obj:`Box`: The resource record for the server.

        Examples:
            >>> server = zpa.servers.get_server('99999')

        """
        return self._get(f"server/{server_id}")

    def delete_server(self, server_id: str) -> int:
        """
        Delete the specified server.

        The server must not be assigned to any Server Groups or the operation will fail.

        Args:
            server_id (str): The unique identifier for the server to be deleted.

        Returns:
            :obj:`int`: The response code for the operation.

        Examples:
            >>> zpa.servers.delete_server('99999')

        """
        return self._delete(f"server/{server_id}", box=False).status_code

    def update_server(self, server_id: str, **kwargs) -> Box:
        """
        Updates the specified server.

        Args:
            server_id (str):
                The unique identifier for the server being updated.
            **kwargs:
                Optional keyword args.

        Keyword Args:
            name (str):
                The name of the server.
            address (str):
                The IP address of the server.
            enabled (bool):
                 Enable the server.
            description (str):
                A description for the server.
            app_server_group_ids (list):
                Unique identifiers for the server groups the server belongs to.
            config_space (str):
                The configuration space for the server.

        Returns:
            :obj:`Box`: The resource record for the updated server.

        Examples:
            Update the name of a server:

            >>> zpa.servers.update_server(
            ...   '99999',
            ...   name='newname.example')

            Update the address and enable a server:

            >>> zpa.servers.update_server(
            ...    '99999',
            ...    address='192.0.2.20',
            ...    enabled=True)

        """
        # Set payload to value of existing record
        payload = {snake_to_camel(k): v for k, v in self.get_server(server_id).items()}

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        resp = self._put(f"server/{server_id}", json=payload, box=False).status_code

        if resp == 204:
            return self.get_server(server_id)
