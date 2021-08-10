from box import BoxList
from restfly.endpoint import APIEndpoint


class PostureProfilesAPI(APIEndpoint):
    def list_profiles(self):
        """
        Returns a list of all configured posture profiles.

        Returns:
            :obj:`list`: A list of all configured posture profiles.

        Examples:
            >>> for posture_profile in zpa.posture_profiles.list_profiles():
            ...    pprint(posture_profile)

        """
        return self._get("posture", box=BoxList)

    def get_profile(self, profile_id: str):
        """
        Returns information on the specified posture profiles.

        Args:
            profile_id (str):
                The unique identifier for the posture profiles.

        Returns:
            :obj:`dict`: The resource record for the posture profiles.

        Examples:
            >>> pprint(zpa.posture_profiles.get_profile('2342342342344433'))

        """

        return self._get(f"posture/{profile_id}")
