from restfly.endpoint import APIEndpoint


class SAMLAttributesAPI(APIEndpoint):

    def list(self):
        """
        Provides a list of all configured SAML attributes.

        Returns:
            :obj:`list`: A list of all configured SAML attributes.

        Examples:
            >>> for saml_attribute in zpa.saml_attributes.list():
            ...    pprint(saml_attribute)

        """
        return self._get('samlAttribute').list

    def details(self, id: str):
        """
        Provides information on the specified SAML attributes.

        Args:
            id (str):
                The unique identifier for the SAML attributes.

        Returns:
            :obj:`dict`: The resource record for the SAML attributes.

        Examples:
            >>> pprint(zpa.saml_attributes.details('2342342342344433'))

        """

        return self._get(f'samlAttribute/{id}')
