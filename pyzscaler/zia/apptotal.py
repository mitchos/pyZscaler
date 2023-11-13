from box import Box
from restfly.endpoint import APIEndpoint


class AppTotalAPI(APIEndpoint):
    def get_app(self, app_id: str, verbose: bool = False) -> Box:
        """
        Searches the AppTotal App Catalog by app ID. If the app exists in the catalog, the app's information is
        returned. If not, the app is submitted for analysis. After analysis is complete, a subsequent GET request is
        required to fetch the app's information.

        Args:
            app_id (str): The app ID to search for.
            verbose (bool, optional): Defaults to False.

        Returns:
            :obj:`Box`: The response object.

        Examples:
            Return verbose information on an app with ID 12345::

                zia.apptotal.get_app(app_id="12345", verbose=True)

        """
        params = {
            "app_id": app_id,
            "verbose": verbose,
        }
        return self._get("apps/app", params=params)

    def scan_app(self, app_id: str) -> Box:
        """
        Submits an app for analysis in the AppTotal Sandbox. After analysis is complete, a subsequent GET request is
        required to fetch the app's information.

        Args:
            app_id (str): The app ID to scan.

        Returns:
            :obj:`Box`: The response object.

        Examples:
            Scan an app with ID 12345::

                zia.apptotal.scan_app(app_id="12345")

        """
        payload = {
            "appId": app_id,
        }
        return self._post("apps/app", json=payload)
