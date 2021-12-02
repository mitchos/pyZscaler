from box import Box, BoxList
from restfly.endpoint import APIEndpoint, APISession

from pyzscaler.utils import Iterator


class SCIMAttributesAPI(APIEndpoint):
    def __init__(self, api: APISession):
        super().__init__(api)
        self.user_config_url = api.user_config_url

    def list_attributes_by_idp(self, idp_id: str, **kwargs) -> BoxList:
        """
        Returns a list of all configured SCIM attributes for the specified IdP.

        Args:
            idp_id (str): The unique id of the IdP to retrieve SCIM attributes for.
            **kwargs: Optional keyword args.

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
            :obj:`BoxList`: A list of all configured SCIM attributes for the specified IdP.

        Examples:
            >>> for scim_attribute in zpa.scim_attributes.list_attributes_by_idp('99999'):
            ...    pprint(scim_attribute)

        """
        return BoxList(Iterator(self._api, f"idp/{idp_id}/scimattribute", **kwargs))

    def get_attribute(self, idp_id: str, attribute_id: str) -> Box:
        """
        Returns information on the specified SCIM attribute.

        Args:
            idp_id (str):
                The unique id of the Idp corresponding to the SCIM attribute.
            attribute_id (str):
                The unique id of the SCIM attribute.

        Returns:
            :obj:`Box`: The resource record for the SCIM attribute.

        Examples:
            >>> pprint(zpa.scim_attributes.get_attribute('99999',
            ...    scim_attribute_id="88888"))

        """

        return self._get(f"idp/{idp_id}/scimattribute/{attribute_id}")

    def get_values(self, idp_id: str, attribute_id: str, **kwargs) -> BoxList:
        """
        Returns information on the specified SCIM attributes.

        Args:
            idp_id (str):
                The unique identifier for the IDP.
            attribute_id (str):
                The unique identifier for the attribute.
            **kwargs:
                Optional keyword args.

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
            :obj:`BoxList`: The resource record for the SCIM attribute values.

        Examples:
            >>> pprint(zpa.scim_attributes.get_values('99999', '88888'))

        """
        return BoxList(
            Iterator(self._api, f"{self.user_config_url}/scimattribute/idpId/{idp_id}/attributeId/{attribute_id}", **kwargs)
        )
