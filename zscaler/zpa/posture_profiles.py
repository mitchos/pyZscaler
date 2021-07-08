from restfly.endpoint import APIEndpoint


class PostureProfilesAPI(APIEndpoint):

    def list(self):
        """
        Provides a list of all configured posture profiles.

        Returns:
            :obj:`list`: A list of all configured posture profiles.

        Examples:
            >>> for posture_profile in zpa.posture_profiles.list():
            ...    pprint(posture_profile)

        """
        return self._get('posture').list

    def details(self, id: str):
        """
        Provides information on the specified posture profiles.

        Args:
            id (str):
                The unique identifier for the posture profiles.

        Returns:
            :obj:`dict`: The resource record for the posture profiles.

        Examples:
            >>> pprint(zpa.posture_profiles.details('2342342342344433'))

        """

        return self._get(f'posture/{id}')
