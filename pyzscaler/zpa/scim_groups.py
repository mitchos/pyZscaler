from box import Box, BoxList
from restfly.endpoint import APIEndpoint, APISession

from pyzscaler.utils import Iterator


class SCIMGroupsAPI(APIEndpoint):
    def __init__(self, api: APISession):
        super().__init__(api)
        self.user_config_url = api.user_config_url

    def list_groups(self, idp_id: str, **kwargs) -> BoxList:
        """
        Returns a list of all configured SCIM groups for the specified IdP.

        Args:
            idp_id (str):
                The unique id of the IdP.

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
            >>> for scim_group in zpa.scim_groups.list_groups("999999"):
            ...    pprint(scim_group)

        """
        return BoxList(Iterator(self._api, f"{self.user_config_url}/scimgroup/idpId/{idp_id}", **kwargs))

    def get_group(self, group_id: str, **kwargs) -> Box:
        """
        Returns information on the specified SCIM group.

        Args:
            group_id (str):
                The unique identifier for the SCIM group.
            **kwargs:
                Optional keyword args.

        Keyword Args:
            all_entries (bool):
                Return all SCIM groups including the deleted ones if ``True``. Defaults to ``False``.

        Returns:
            :obj:`dict`: The resource record for the SCIM group.

        Examples:
            >>> pprint(zpa.scim_groups.get_group('99999'))

        """

        return self._get(f"{self.user_config_url}/scimgroup/{group_id}")
