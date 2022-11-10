from box import Box, BoxList
from restfly.endpoint import APIEndpoint

from pyzscaler.utils import Iterator


class CloudConnectorGroupsAPI(APIEndpoint):
    def list_groups(self, **kwargs) -> BoxList:
        """
        Returns a list of all configured cloud connector groups.

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
            :obj:`BoxList`: A list of all configured cloud connector groups.

        Examples:
            >>> for cloud_connector_group in zpa.cloud_connector_groups.list_groups():
            ...    pprint(cloud_connector_group)

        """
        return BoxList(Iterator(self._api, "cloudConnectorGroup", **kwargs))

    def get_group(self, group_id: str) -> Box:
        """
        Returns information on the specified cloud connector group.

        Args:
            group_id (str):
                The unique identifier for the cloud connector group.

        Returns:
            :obj:`Box`: The resource record for the cloud connector group.

        Examples:
            >>> pprint(zpa.cloud_connector_groups.get_group('99999'))

        """

        return self._get(f"cloudConnectorGroup/{group_id}")
