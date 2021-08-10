from box import BoxList
from restfly.endpoint import APIEndpoint


class TrustedNetworksAPI(APIEndpoint):
    def list_networks(self):
        """
        Returns a list of all configured trusted networks.

        Returns:
            :obj:`list`: A list of all configured trusted networks.

        Examples:
            >>> for trusted_network in zpa.trusted_networks.list_networks():
            ...    pprint(trusted_network)

        """
        return self._get("network", box=BoxList)

    def get_network(self, network_id: str):
        """
        Returns information on the specified trusted network.

        Args:
            network_id (str):
                The unique identifier for the trusted network.

        Returns:
            :obj:`dict`: The resource record for the trusted network.

        Examples:
            >>> pprint(zpa.trusted_networks.get_network('2342342342344433'))

        """

        return self._get(f"network/{network_id}")
