from box import BoxList
from restfly.endpoint import APIEndpoint


class SAMLAttributesAPI(APIEndpoint):
    def list_attributes(self):
        """
        Returns a list of all configured SAML attributes.

        Returns:
            :obj:`list`: A list of all configured SAML attributes.

        Examples:
            >>> for saml_attribute in zpa.saml_attributes.list_attributes():
            ...    pprint(saml_attribute)

        """
        return self._get("samlAttribute", box=BoxList)

    def get_attribute(self, attribute_id: str):
        """
        Returns information on the specified SAML attributes.

        Args:
            attribute_id (str):
                The unique identifier for the SAML attributes.

        Returns:
            :obj:`dict`: The resource record for the SAML attributes.

        Examples:
            >>> pprint(zpa.saml_attributes.get_attribute('2342342342344433'))

        """

        return self._get(f"samlAttribute/{attribute_id}")
