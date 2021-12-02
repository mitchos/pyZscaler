from warnings import warn

from box import Box, BoxList
from restfly.endpoint import APIEndpoint

from pyzscaler.utils import Iterator


class ConnectorGroupsAPI(APIEndpoint):
    def list_groups(self, **kwargs) -> BoxList:
        """
        Returns a list of all connector groups.

        Warnings:
            .. deprecated:: 0.13.0
                Use :func:`zpa.connectors.list_connector_groups` instead.

        Returns:
            :obj:`BoxList`: List of all configured connector groups.

        Examples:
            >>> connector_groups = zpa.connector_groups.list_groups()

        """
        warn(
            "This endpoint is deprecated and will eventually be removed. "
            "Use zpa.connectors.list_connector_groups() instead."
        )

        return BoxList(Iterator(self._api, "appConnectorGroup", **kwargs))

    def get_group(self, group_id: str) -> Box:
        """
        Get information for a specified connector group.

        Warnings:
            .. deprecated:: 0.13.0
                Use :func:`zpa.connectors.get_connector_group` instead.

        Args:
            group_id (str):
                The unique identifier for the connector group.

        Returns:
            :obj:`Box`:
                The connector group resource record.

        Examples:
            >>> connector_group = zpa.connector_groups.get_group('2342342354545455')

        """
        warn(
            "This endpoint is deprecated and will eventually be removed. " "Use zpa.connectors.get_connector_group() instead."
        )

        return self._get(f"appConnectorGroup/{group_id}")
