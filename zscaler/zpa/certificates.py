from restfly.endpoint import APIEndpoint


class BACertificatesAPI(APIEndpoint):

    def browser_list(self):
        """
        Provides a list of all Browser Access certificates.

        Returns:
            :obj:`list`: List of all Browser Access certificates.

        Examples:
            >>> ba_certificates = zpa.certificates.browser_list()

        """
        return self._get('clientlessCertificate/issued').list

    def browser_details(self, id: str):
        """
        Get information for a specified Browser Access certificate.

        Args:
            id (str):
                The unique identifier for the Browser Access certificate.

        Returns:
            :obj:`dict`:
                The Browser Access certificate resource record.

        Examples:
            >>> ba_certificate = zpa.certificates.browser_details('2342342354545455')

        """
        return self._get(f'clientlessCertificate/{id}')
