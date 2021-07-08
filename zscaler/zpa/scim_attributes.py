from restfly.endpoint import APIEndpoint


class SCIMAttributesAPI(APIEndpoint):

    def list(self):
        """
        Provides a list of all configured SCIM attributes.

        Returns:
            :obj:`list`: A list of all configured SCIM attributes.

        Examples:
            >>> for scim_attribute in zpa.scim_attributes.list():
            ...    pprint(scim_attribute)

        """
        return self._get('scimAttribute').list

    def details(self, idp_id: str):
        """
        Provides information on the specified SCIM attributes.

        Args:
            idp_id (str):
                The unique identifier for the IDP.

        Returns:
            :obj:`dict`: The resource record for the SCIM attributes.

        Examples:
            >>> pprint(zpa.scim_attributes.details('2342342342344433'))

        """

        return self._get(f'scimAttribute/{idp_id}')

    def values(self, idp_id: str, attribute_id: str):
        """
        Provides information on the specified SCIM attributes.

        Args:
            idp_id (str):
                The unique identifier for the IDP.
            attribute_id (str):
                The unique identifier for the attribute.

        Returns:
            :obj:`dict`: The resource record for the SCIM attribute values.

        Examples:
            >>> pprint(zpa.scim_attributes.values('2342342342344433', '1231231322332'))

        """

        return self._get(f'scimAttribute/{idp_id}/attributeId/{attribute_id}')
