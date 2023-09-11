from box import Box, BoxList
from restfly import APIEndpoint


class ConnectorsAPI(APIEndpoint):
    def list_groups(self, **kwargs) -> BoxList:
        """
        List all existing connector groups.

        Keyword Args:
            page (int): The page number to return.
            page_size (int): The number of items to return per page.

        Returns:
            :obj:`BoxList`: The list of cloud and branch connector groups.

        """
        return self._get("ecGroup", params=kwargs)

    def get_group(self, group_id: str) -> Box:
        """
        Get details for a specific connector group.

        Args:
            group_id (str): The ID of the connector group.

        Returns:
            :obj:`Box`: The connector group details.

        Examples:
            >>> print(zcon.connectors.get_group("123456789")

        """
        return self._get(f"ecGroup/{group_id}")

    def get_vm(self, group_id: str, vm_id: str):
        """
        Get details for a specific connector VM.

        Args:
            group_id (str): The ID of the connector group.
            vm_id (str): The ID of the connector VM.

        Returns:
            :obj:`Box`: The connector VM details.

        Examples:
            >>> print(zcon.connectors.get_vm("123456789", "123456789")

        """
        return self._get(f"ecGroup/{group_id}/vm/{vm_id}")

    def delete_vm(self, group_id: str, vm_id: str) -> Box:
        """
        Delete the specified connector VM.

        Args:
            group_id (str): The ID of the connector group.
            vm_id (str): The ID of the connector VM.

        Returns:
            :obj:`Box`: The status of the operation.

        """
        return self._delete(f"ecGroup/{group_id}/vm/{vm_id}")
