from restfly.endpoint import APIEndpoint


class AppsAPI(APIEndpoint):
    def list_apps(self):
        """
        Returns a list of all active applications configured within the ZDX tenant.

        Returns:

        """
        return self._get("apps")

    def get_app(self, app_id: str):
        """
        Returns information on the specified application configured within the ZDX tenant.
        Args:
            app_id (str): The unique ID for the ZDX application.

        Returns:

        """
        return self._get(f"apps/{app_id}")
