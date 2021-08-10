from box import BoxList
from restfly.endpoint import APIEndpoint


class BACertificatesAPI(APIEndpoint):
    def list_browser_access(self):
        """
        Returns a list of all Browser Access certificates.

        Returns:
            :obj:`list`: List of all Browser Access certificates.

        Examples:
            >>> ba_certificates = zpa.certificates.list_browser_access()

        """
        return self._get("clientlessCertificate/issued", box=BoxList)

    def get_browser_access(self, certificate_id: str):
        """
        Returns information on a specified Browser Access certificate.

        Args:
            certificate_id (str):
                The unique identifier for the Browser Access certificate.

        Returns:
            :obj:`dict`:
                The Browser Access certificate resource record.

        Examples:
            >>> ba_certificate = zpa.certificates.get_browser_access('2342342354545455')

        """
        return self._get(f"clientlessCertificate/{certificate_id}")
