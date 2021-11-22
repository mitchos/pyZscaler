from box import Box, BoxList
from restfly import APISession
from restfly.endpoint import APIEndpoint

from pyzscaler.utils import Iterator


class TrustedNetworksAPI(APIEndpoint):
    def __init__(self, api: APISession):
        super().__init__(api)

        self.v2_url = api.v2_url

    def list_networks(self, **kwargs) -> BoxList:
        """
        Returns a list of all configured trusted networks.

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
            :obj:`BoxList`: A list of all configured trusted networks.

        Examples:
            >>> for trusted_network in zpa.trusted_networks.list_networks():
            ...    pprint(trusted_network)

        """
        return BoxList(Iterator(self._api, f"{self.v2_url}/network", **kwargs))

    def get_network(self, network_id: str) -> Box:
        """
        Returns information on the specified trusted network.

        Args:
            network_id (str):
                The unique identifier for the trusted network.

        Returns:
            :obj:`Box`: The resource record for the trusted network.

        Examples:
            >>> pprint(zpa.trusted_networks.get_network('99999'))

        """

        return self._get(f"network/{network_id}")
