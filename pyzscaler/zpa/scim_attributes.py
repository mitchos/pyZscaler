from restfly.endpoint import APIEndpoint


class SCIMAttributesAPI(APIEndpoint):
    def list_attribute(self):
        """
        Returns a list of all configured SCIM attributes.

        Returns:
            :obj:`list`: A list of all configured SCIM attributes.

        Examples:
            >>> for scim_attribute in zpa.scim_attributes.list_attribute():
            ...    pprint(scim_attribute)

        """
        return self._get("scimAttribute").list

    def get_attribute(self, idp_id: str):
        """
        Returns information on the specified SCIM attributes.

        Args:
            idp_id (str):
                The unique identifier of the Idp corresponding to the SCIM attribute.

        Returns:
            :obj:`dict`: The resource record for the SCIM attributes.

        Examples:
            >>> pprint(zpa.scim_attributes.get_attribute('2342342342344433'))

        """

        return self._get(f"scimAttribute/{idp_id}")

    def get_values(self, idp_id: str, attribute_id: str):
        """
        Returns information on the specified SCIM attributes.

        Args:
            idp_id (str):
                The unique identifier for the IDP.
            attribute_id (str):
                The unique identifier for the attribute.

        Returns:
            :obj:`dict`: The resource record for the SCIM attribute values.

        Examples:
            >>> pprint(zpa.scim_attributes.get_values('2342342342344433', '1231231322332'))

        """

        return self._get(f"scimAttribute/{idp_id}/attributeId/{attribute_id}")
