from box import BoxList
from restfly.endpoint import APIEndpoint


class IDPControllerAPI(APIEndpoint):
    def list_idps(self):
        """
        Returns a list of all configured IDPs.

        Returns:
            :obj:`list`: A list of all configured IDPs.

        Examples:
            >>> for idp in zpa.idp.list_idps():
            ...    pprint(idp)

        """
        return self._get("idp", box=BoxList)

    def get_idp(self, idp_id: str):
        """
        Returns information on the specified IDP.

        Args:
            idp_id (str):
                The unique identifier for the IDP.

        Returns:
            :obj:`dict`: The resource record for the IDP.

        Examples:
            >>> pprint(zpa.idp.get_idp('2342342342344433'))

        """

        return self._get(f"idp/{idp_id}")
