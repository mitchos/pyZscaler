from box import BoxList
from restfly.endpoint import APIEndpoint

from pyzscaler.utils import Iterator


class CloudConnectorGroupsAPI(APIEndpoint):
    def list_groups(self, **kwargs):
        """
        Returns a list of all configured cloud connector groups.

        Returns:
            :obj:`list`: A list of all configured cloud connector groups.

        Examples:
            >>> for cloud_connector_group in zpa.cloud_connector_groups.list_groups():
            ...    pprint(cloud_connector_group)

        """
        return BoxList(Iterator(self._api, "cloudConnectorGroups", **kwargs))

    def get_group(self, group_id: str):
        """
        Returns information on the specified cloud connector group.

        Args:
            group_id (str):
                The unique identifier for the cloud connector group.

        Returns:
            :obj:`dict`: The resource record for the cloud connector group.

        Examples:
            >>> pprint(zpa.cloud_connector_groups.get_group('2342342342344433'))

        """

        return self._get(f"cloudConnectorGroups/{group_id}")
