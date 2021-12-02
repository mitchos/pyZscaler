from box import Box, BoxList
from restfly import APISession
from restfly.endpoint import APIEndpoint

from pyzscaler.utils import Iterator


class PostureProfilesAPI(APIEndpoint):
    def __init__(self, api: APISession):
        super().__init__(api)

        self.v2_url = api.v2_url

    def list_profiles(self, **kwargs) -> BoxList:
        """
        Returns a list of all configured posture profiles.

        Keyword Args:
            **max_items (int):
                The maximum number of items to request before stopping iteration.
            **max_pages (int):
                The maximum number of pages to request before stopping iteration.
            **pagesize (int):
                Specifies the page size. The default size is 20, but the maximum size is 500.
            **search (str, optional):
                The search string used to match against features and fields.

        Returns:
            :obj:`BoxList`: A list of all configured posture profiles.

        Examples:
            >>> for posture_profile in zpa.posture_profiles.list_profiles():
            ...    pprint(posture_profile)

        """
        return BoxList(Iterator(self._api, f"{self.v2_url}/posture", **kwargs))

    def get_profile(self, profile_id: str) -> Box:
        """
        Returns information on the specified posture profiles.

        Args:
            profile_id (str):
                The unique identifier for the posture profiles.

        Returns:
            :obj:`Box`: The resource record for the posture profiles.

        Examples:
            >>> pprint(zpa.posture_profiles.get_profile('99999'))

        """

        return self._get(f"posture/{profile_id}")
