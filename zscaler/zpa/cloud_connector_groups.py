from restfly.endpoint import APIEndpoint


class CloudConnectorGroupsAPI(APIEndpoint):

    def list(self):
        """
        Provides a list of all configured cloud connector groups.

        Returns:
            :obj:`list`: A list of all configured cloud connector groups.

        Examples:
            >>> for cloud_connector_group in zpa.cloud_connector_groups.list():
            ...    pprint(cloud_connector_group)

        """
        return self._get('cloudConnectorGroups').list

    def details(self, id: str):
        """
        Provides information on the specified cloud connector group.

        Args:
            id (str):
                The unique identifier for the cloud connector group.

        Returns:
            :obj:`dict`: The resource record for the cloud connector group.

        Examples:
            >>> pprint(zpa.cloud_connector_groups.details('2342342342344433'))

        """

        return self._get(f'cloudConnectorGroups/{id}')
