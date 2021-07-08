from restfly.endpoint import APIEndpoint


class MachineGroupsAPI(APIEndpoint):

    def list(self):
        """
        Provides a list of all configured machine groups.

        Returns:
            :obj:`list`: A list of all configured machine groups.

        Examples:
            >>> for machine_group in zpa.machine_groups.list():
            ...    pprint(machine_group)

        """
        return self._get('machine_groups').list

    def details(self, id: str):
        """
        Provides information on the specified machine group.

        Args:
            id (str):
                The unique identifier for the machine group.

        Returns:
            :obj:`dict`: The resource record for the machine group.

        Examples:
            >>> pprint(zpa.machine_groups.details('2342342342344433'))

        """

        return self._get(f'machine_groups/{id}')
