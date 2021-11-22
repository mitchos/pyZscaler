from box import Box, BoxList
from restfly.endpoint import APIEndpoint

from pyzscaler.utils import Iterator


class MachineGroupsAPI(APIEndpoint):
    def list_groups(self, **kwargs) -> BoxList:
        """
        Returns a list of all configured machine groups.

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
            :obj:`list`: A list of all configured machine groups.

        Examples:
            >>> for machine_group in zpa.machine_groups.list_groups():
            ...    pprint(machine_group)

        """
        return BoxList(Iterator(self._api, "machineGroup", **kwargs))

    def get_group(self, group_id: str) -> Box:
        """
        Returns information on the specified machine group.

        Args:
            group_id (str):
                The unique identifier for the machine group.

        Returns:
            :obj:`Box`: The resource record for the machine group.

        Examples:
            >>> pprint(zpa.machine_groups.get_group('99999'))

        """

        return self._get(f"machineGroup/{group_id}")
