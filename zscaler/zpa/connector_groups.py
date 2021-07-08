from restfly.endpoint import APIEndpoint


class ConnectorGroupsAPI(APIEndpoint):

    def list(self):
        """
        Provides a list of all connector groups.

        Returns:
            :obj:`list`: List of all configured connector groups.

        Examples:
            >>> connector_groups = zpa.connector_groups.list()

        """
        return self._get('appConnectorGroup').list

    def details(self, id: str):
        """
        Get information for a specified connector group.

        Args:
            id (str):
                The unique identifier for the connector group.

        Returns:
            :obj:`dict`:
                The connector group resource record.

        Examples:
            >>> connector_group = zpa.connector_groups.details('2342342354545455')

        """
        return self._get(f'appConnectorGroup/{id}')
