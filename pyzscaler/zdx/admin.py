from restfly.endpoint import APIEndpoint


class AdminAPI(APIEndpoint):
    def get_departments(self):
        """
        Returns a list of departments that are configured within ZDX.

        Returns:

        """
        return self._get("administration/departments")

    def get_locations(self):
        """
        Returns a list of locations that are configured within ZDX.

        Returns:

        """
        return self._get("administration/locations")
