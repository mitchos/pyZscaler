from box import Box, BoxList
from restfly.endpoint import APIEndpoint

from pyzscaler.utils import Iterator


class SCIMGroupsAPI(APIEndpoint):
    def list_groups(self, **kwargs) -> BoxList:
        """
        Returns a list of all configured SCIM groups.

        Keyword Args:
            **end_time (str):
                The end of a time range for requesting last updated data (modified_time) for the SCIM group.
                This requires setting the ``start_time`` parameter as well.
            **idp_group_id (str):
                The unique id of the IdP group.
            **max_items (int):
                The maximum number of items to request before stopping iteration.
            **max_pages (int):
                The maximum number of pages to request before stopping iteration.
            **pagesize (int):
                Specifies the page size. The default size is 20, but the maximum size is 500.
            **scim_user_id (str):
                The unique id for the SCIM user.
            **search (str, optional):
                The search string used to match against features and fields.
            **sort_order (str):
                Sort the last updated time (modified_time) by ascending ``ASC`` or descending ``DSC`` order. Defaults to
                ``DSC``.
            **start_time (str):
                The start of a time range for requesting last updated data (modified_time) for the SCIM group.
                This requires setting the ``end_time`` parameter as well.

        Returns:
            :obj:`list`: A list of all configured SCIM groups.

        Examples:
            >>> for scim_group in zpa.scim_groups.list_groups():
            ...    pprint(scim_group)

        """
        return BoxList(Iterator(self._api, "scimgroup", **kwargs))

    def get_group(self, idp_id: str) -> Box:
        """
        Returns information on the specified SCIM group.

        Args:
            idp_id (str):
                The unique identifier for the Idp corresponding to the SCIM group.

        Returns:
            :obj:`dict`: The resource record for the SCIM group.

        Examples:
            >>> pprint(zpa.scim_groups.get_group('99999'))

        """

        return self._get(f"scimgroup/idpId/{idp_id}")
