from box import BoxList
from restfly.endpoint import APIEndpoint

from pyzscaler.utils import zdx_params


class AdminAPI(APIEndpoint):
    @zdx_params
    def list_departments(self, **kwargs) -> BoxList:
        """
        Returns a list of departments that are configured within ZDX.

        Keyword Args:
            since (int): The number of hours to look back for devices.
            search (str): The search string to filter by name or department ID.

        Returns:
            :obj:`BoxList`: The list of departments in ZDX.

        Examples:
            List all departments in ZDX for the past 2 hours
            >>> for department in zdx.admin.list_departments():
            ...     print(department)

        """

        return self._get("administration/departments", params=kwargs)

    @zdx_params
    def list_locations(self, **kwargs) -> BoxList:
        # TODO: Check if the keyword arg is 'search' or 'q'. Docs are potentially wrong or inconsistent
        """
        Returns a list of locations that are configured within ZDX.

        Keyword Args:
            since (int): The number of hours to look back for devices.
            search (str): The search string to filter by name or location ID.

        Returns:
            :obj:`BoxList`: The list of locations in ZDX.

        Examples:
            List all locations in ZDX for the past 2 hours
            >>> for location in zdx.admin.list_locations():
            ...     print(location)

        """
        return self._get("administration/locations", params=kwargs)

    @zdx_params
    def list_geolocations(self, **kwargs) -> BoxList:
        """
        Returns a list of all active geolocations configured within the ZDX tenant.

        Keyword Args:
            since (int): The number of hours to look back for devices.
            location_id (str): The unique ID for the location.
            parent_geo_id (str): The unique ID for the parent geolocation.
            search (str): The search string to filter by name.

        Returns:
            :obj:`BoxList`: The list of geolocations in ZDX.

        Examples:
            List all geolocations in ZDX for the past 2 hours
            >>> for geolocation in zdx.admin.list_geolocations():
            ...     print(geolocation)

        """
        return self._get("active_geo", params=kwargs)
