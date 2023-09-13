from box import Box, BoxList
from restfly import APIEndpoint


class ZCONConnectorsAPI(APIEndpoint):
    def list_groups(self, **kwargs) -> BoxList:
        """
        List all existing connector groups.

        Keyword Args:
            page (int): The page number to return.
            page_size (int): The number of items to return per page.

        Returns:
            :obj:`BoxList`: The list of cloud and branch connector groups.

        Examples:
            List all connector groups::

                for group in zcon.connectors.list_groups():
                    print(group)

            List first page of connector groups with 10 items per page::

                for group in zcon.connectors.list_groups(page=1, page_size=10):
                    print(group)

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
            Get details of a specific connector group::

                print(zcon.connectors.get_group("123456789"))
        """
        return self._get(f"ecGroup/{group_id}")

    def get_vm(self, group_id: str, vm_id: str) -> Box:
        """
        Get details for a specific connector VM.

        Args:
            group_id (str): The ID of the connector group.
            vm_id (str): The ID of the connector VM.

        Returns:
            :obj:`Box`: The connector VM details.

        Examples:
            Get details of a specific connector VM::

                print(zcon.connectors.get_vm("123456789", "987654321"))
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

        Examples:
            Delete a specific connector VM::

                zcon.connectors.delete_vm("123456789", "987654321")
        """
        return self._delete(f"ecGroup/{group_id}/vm/{vm_id}")
