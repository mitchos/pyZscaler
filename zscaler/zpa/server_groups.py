from restfly.endpoint import APIEndpoint
from restfly.errors import RequiredParameterError


class ServerGroupsAPI(APIEndpoint):

    def list(self):
        """
        Provides a list of all configured server groups.

        Returns:
            :obj:`list`: A list of all configured server groups.

        Examples:
            >>> for server_group in zpa.server_groups.list():
            ...    pprint(server_group)

        """
        return self._get('serverGroup').list

    def details(self, id: str):
        """
        Provides information on the specified server group.

        Args:
            id (str):
                The unique identifier for the server group.

        Returns:
            :obj:`dict`: The resource record for the server group.

        Examples:
            >>> pprint(zpa.server_groups.details('2342342342344433'))

        """

        return self._get(f'serverGroup/{id}')

    def delete(self, id: str):
        """
        Deletes the specified server group.

        Args:
            id (str):
                The unique identifier for the server group to be deleted.

        Returns:
            :obj:`str`: The response code for the operation.

        Examples:
            >>> zpa.server_groups.delete('2342342342343')

        """
        return self._delete(f'serverGroup/{id}')

    def add(self, name: str, app_connector_ids: list, **kwargs):
        """Adds a server group.

        Args:
            name (str):
                The name for the server group.
            app_connector_ids (:obj:`list` of :obj:`str`):
                A list of application connector IDs that will be attached to the server group.
            **kwargs:
                Optional params.

        Keyword Args:
            applications (list):
            configSpace (str):
            description (str):
            enabled (bool):
            ipAnchored (bool):
            dynamicDiscovery (bool):
            servers (list):

        Returns:
            :obj:`dict`: The resource record for the newly created server group.

        Examples:
            Create a server group with the minimum params:

            >>> zpa.server_groups.add('new_server_group'
            ...    app_connector_ids['23423423432444'])

            Create a server group and define a new server on the fly:

            >>> zpa.server_groups.add('new_server_group',
            ...    app_connector_ids=['23423423432444'],
            ...    enabled=True,
            ...    servers=[{
            ...      'name': 'new_server',
            ...      'address': '10.0.0.30',
            ...      'enabled': True}])

        """
        # Initialise payload
        payload = {
            'name': name,
            'appConnectorGroups': []
        }
        # Iterate through provided app connector group IDs and add to payload
        for app_connector_id in app_connector_ids:
            app_connector_group = {
                'id': app_connector_id
            }
            payload['appConnectorGroups'].append(app_connector_group)
        # Add optional params to payload
        for key, value in kwargs.items():
            payload[key] = value

        return self._post('serverGroup', json=payload)

    def update(self, id: str, dynamic_discovery: bool = None, servers: list = None, **kwargs):
        """
        Updates a server group.

        .. Note:: The ZPA server group API requires the dynamic_discovery and servers params to be provided for all
            updates.

        Args:
            id (str, required):
                The unique identifier for the server group.
            dynamic_discovery (bool, required):
                Should Dynamic Discovery be enabled.
            servers (:obj:`list` of :obj:`dict`):
                The server objects for the server group.
            **kwargs:

        Returns:
            :obj:`dict`: The resource record for the updated server group.

        """

        payload = {
            'id': id,
        }
        if dynamic_discovery is None:
            payload['dynamicDiscovery'] = dynamic_discovery

        if servers is not None:
            payload['servers'] = servers

        # Add optional params to payload
        for key, value in kwargs.items():
            payload[key] = value

        print(payload)

        return self._put(f'serverGroup/{id}', json=payload, box=False)
