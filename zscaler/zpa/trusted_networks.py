from restfly.endpoint import APIEndpoint


class TrustedNetworksAPI(APIEndpoint):

    def list(self):
        """
        Provides a list of all configured trusted networks.

        Returns:
            :obj:`list`: A list of all configured trusted networks.

        Examples:
            >>> for trusted_network in zpa.trusted_networks.list():
            ...    pprint(trusted_network)

        """
        return self._get('network').list

    def details(self, id: str):
        """
        Provides information on the specified trusted network.

        Args:
            id (str):
                The unique identifier for the trusted network.

        Returns:
            :obj:`dict`: The resource record for the trusted network.

        Examples:
            >>> pprint(zpa.trusted_networks.details('2342342342344433'))

        """

        return self._get(f'network/{id}')
