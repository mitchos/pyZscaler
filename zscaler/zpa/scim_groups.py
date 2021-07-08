from restfly.endpoint import APIEndpoint


class SCIMGroupsAPI(APIEndpoint):

    def list(self):
        """
        Provides a list of all configured SCIM groups.

        Returns:
            :obj:`list`: A list of all configured SCIM groups.

        Examples:
            >>> for scim_group in zpa.scim_groups.list():
            ...    pprint(scim_group)

        """
        return self._get('scimgroup').list

    def details(self, id: str):
        """
        Provides information on the specified SCIM group.

        Args:
            id (str):
                The unique identifier for the IDP.

        Returns:
            :obj:`dict`: The resource record for the SCIM group.

        Examples:
            >>> pprint(zpa.scim_groups.details('2342342342344433'))

        """

        return self._get(f'scimgroup/idpId/{id}')
