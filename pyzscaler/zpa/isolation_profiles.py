from box import BoxList
from restfly import APISession
from restfly.endpoint import APIEndpoint

from pyzscaler.utils import Iterator


class IsolationProfilesAPI(APIEndpoint):
    def __init__(self, api: APISession):
        super().__init__(api)

        self._url = api._url

    def list_profiles(self, **kwargs) -> BoxList:
        """
        Returns a list of all configured isolation profiles.

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
            :obj:`BoxList`: A list of all configured isolation profiles.

        Examples:
            >>> for isolation_profile in zpa.isolation_profiles.list_profiles():
            ...    pprint(isolation_profile)

        """
        return BoxList(Iterator(self._api, f"{self._url}/isolation/profiles", **kwargs))
