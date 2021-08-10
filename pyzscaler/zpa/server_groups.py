from restfly.endpoint import APIEndpoint

from pyzscaler.utils import snake_to_camel, add_id_groups


class ServerGroupsAPI(APIEndpoint):
    reformat_params = [
        ("application_ids", "applications"),
        ("server_ids", "servers"),
        ("app_connector_group_ids", "appConnectorGroups"),
    ]

    def list_groups(self):
        """
        Returns a list of all configured server groups.

        Returns:
            :obj:`list`: A list of all configured server groups.

        Examples:
            >>> for server_group in zpa.server_groups.list_groups():
            ...    pprint(server_group)

        """
        return self._get("serverGroup").list

    def get_group(self, group_id: str):
        """
        Provides information on the specified server group.

        Args:
            group_id (str):
                The unique id for the server group.

        Returns:
            :obj:`dict`: The resource record for the server group.

        Examples:
            >>> pprint(zpa.server_groups.get_group('2342342342344433'))

        """

        return self._get(f"serverGroup/{group_id}")

    def delete_group(self, group_id: str):
        """
        Deletes the specified server group.

        Args:
            group_id (str):
                The unique id for the server group to be deleted.

        Returns:
            :obj:`str`: The response code for the operation.

        Examples:
            >>> zpa.server_groups.delete_group('2342342342343')

        """
        return self._delete(f"serverGroup/{group_id}")

    def add_group(self, app_connector_group_ids: list, name: str, **kwargs):
        """
        Adds a server group.

        Args:
            name (str):
                The name for the server group.
            app_connector_group_ids (:obj:`list` of :obj:`str`):
                A list of application connector IDs that will be attached to the server group.
            **kwargs:
                Optional params.

        Keyword Args:
            application_ids (:obj:`list` of :obj:`str`):
                A list of unique IDs of applications to associate with this server group.
            config_space (str): The configuration space. Accepted values are `DEFAULT` or `SIEM`.
            description (str): Additional information about the server group.
            enabled (bool): Enable the server group.
            ip_anchored (bool): Enable IP Anchoring.
            dynamic_discovery (bool): Enable Dynamic Discovery.
            server_ids (:obj:`list` of :obj:`str`):
                A list of unique IDs of servers to associate with this server group.

        Returns:
            :obj:`dict`: The resource record for the newly created server group.

        Examples:
            Create a server group with the minimum params:

            >>> zpa.server_groups.add_group('new_server_group'
            ...    app_connector_group_ids['916196382959075361'])

            Create a server group and define a new server on the fly:

            >>> zpa.server_groups.add_group('new_server_group',
            ...    app_connector_group_ids=['916196382959075361'],
            ...    enabled=True,
            ...    servers=[{
            ...      'name': 'new_server',
            ...      'address': '10.0.0.30',
            ...      'enabled': True}])

        """
        # Initialise payload
        payload = {
            "name": name,
            "appConnectorGroups": [
                {"id": group_id} for group_id in app_connector_group_ids
            ],
        }

        add_id_groups(self.reformat_params, kwargs, payload)

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        return self._post("serverGroup", json=payload)

    def update_group(self, group_id: str, **kwargs):
        """
        Updates a server group.

        Args:
            group_id (str, required):
                The unique identifier for the server group.
            **kwargs: Optional keyword args.

        Keyword Args:
            app_connector_group_ids (:obj:`list` of :obj:`str`):
                A list of application connector IDs that will be attached to the server group.
            application_ids (:obj:`list` of :obj:`str`):
                A list of unique IDs of applications to associate with this server group.
            config_space (str): The configuration space. Accepted values are `DEFAULT` or `SIEM`.
            description (str): Additional information about the server group.
            enabled (bool): Enable the server group.
            ip_anchored (bool): Enable IP Anchoring.
            dynamic_discovery (bool): Enable Dynamic Discovery.
            server_ids (:obj:`list` of :obj:`str`):
                A list of unique IDs of servers to associate with this server group

        Returns:
            :obj:`dict`: The resource record for the updated server group.

        Examples:
            Update the name of a server group:

            >>> zpa.server_groups.update_group(name='Updated Name')

            Enable IP anchoring and Dynamic Discovery:

            >>> zpa.server_groups.update_group(ip_anchored=True,
            ...    dynamic_discovery=True)

        """

        # Set payload to value of existing record
        payload = {snake_to_camel(k): v for k, v in self.get_group(group_id).items()}

        add_id_groups(self.reformat_params, kwargs, payload)

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        return self._put(f"serverGroup/{group_id}", json=payload, box=False).status_code
