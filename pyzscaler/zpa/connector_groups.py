from box import BoxList
from restfly.endpoint import APIEndpoint

from pyzscaler.utils import Iterator


class ConnectorGroupsAPI(APIEndpoint):
    def list_groups(self, **kwargs):
        """
        Returns a list of all connector groups.

        Returns:
            :obj:`list`: List of all configured connector groups.

        Examples:
            >>> connector_groups = zpa.connector_groups.list_groups()

        """
        return BoxList(Iterator(self._api, "appConnectorGroup", **kwargs))

    def get_group(self, group_id: str):
        """
        Get information for a specified connector group.

        Args:
            group_id (str):
                The unique identifier for the connector group.

        Returns:
            :obj:`dict`:
                The connector group resource record.

        Examples:
            >>> connector_group = zpa.connector_groups.get_group('2342342354545455')

        """
        return self._get(f"appConnectorGroup/{group_id}")
