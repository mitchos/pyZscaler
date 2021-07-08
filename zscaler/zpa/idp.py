from restfly.endpoint import APIEndpoint


class IDPControllerAPI(APIEndpoint):

    def list(self):
        """
        Provides a list of all configured IDPs.

        Returns:
            :obj:`list`: A list of all configured IDPs.

        Examples:
            >>> for idp in zpa.idp.list():
            ...    pprint(idp)

        """
        return self._get('idp').list

    def details(self, id: str):
        """
        Provides information on the specified IDP.

        Args:
            id (str):
                The unique identifier for the IDP.

        Returns:
            :obj:`dict`: The resource record for the IDP.

        Examples:
            >>> pprint(zpa.idp.details('2342342342344433'))

        """

        return self._get(f'idp/{id}')
