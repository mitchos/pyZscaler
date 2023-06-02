from box import BoxList
from restfly.endpoint import APIEndpoint

from pyzscaler.utils import ZDXIterator, zdx_params


class AppsAPI(APIEndpoint):
    @zdx_params
    def list_apps(self, **kwargs) -> BoxList:
        """
        Returns a list of all active applications configured within the ZDX tenant.

        Keyword Args:
            since (int): The number of hours to look back for devices.
            location_id (str): The unique ID for the location.
            department_id (str): The unique ID for the department.
            geo_id (str): The unique ID for the geolocation.

        Returns:
            :obj:`BoxList`: The list of applications in ZDX.

        Examples:
            List all applications in ZDX for the past 2 hours
            >>> for app in zdx.apps.list_apps():
            ...     print(app)

        """
        return self._get("apps", params=kwargs)

    @zdx_params
    def get_app(self, app_id: str, **kwargs):
        """
        Returns information on the specified application configured within the ZDX tenant.

        Args:
            app_id (str): The unique ID for the ZDX application.

        Keyword Args:
            since (int): The number of hours to look back for devices.
            location_id (str): The unique ID for the location.
            department_id (str): The unique ID for the department.
            geo_id (str): The unique ID for the geolocation.

        Returns:
            :obj:`Box`: The application information.

        Examples:
            Return information on the application with the ID of 999999999:
            >>> zia.apps.get_app(app_id='999999999')

        """
        return self._get(f"apps/{app_id}", params=kwargs)

    @zdx_params
    def get_app_score(self, app_id: str, **kwargs):
        """
        Returns the ZDX score trend for the specified application configured within the ZDX tenant.

        Args:
            app_id (str): The unique ID for the ZDX application.

        Keyword Args:
            since (int): The number of hours to look back for devices.
            location_id (str): The unique ID for the location.
            department_id (str): The unique ID for the department.
            geo_id (str): The unique ID for the geolocation.

        Returns:
            :obj:`Box`: The application's ZDX score trend.

        Examples:
            Return the ZDX score trend for the application with the ID of 999999999:
            >>> zia.apps.get_app_score(app_id='999999999')

        """
        return self._get(f"apps/{app_id}/score", params=kwargs)

    @zdx_params
    def get_app_metrics(self, app_id: str, **kwargs):
        """
        Returns the ZDX metrics for the specified application configured within the ZDX tenant.

        Args:
            app_id (str): The unique ID for the ZDX application.

        Keyword Args:
            since (int): The number of hours to look back for devices.
            location_id (str): The unique ID for the location.
            department_id (str): The unique ID for the department.
            geo_id (str): The unique ID for the geolocation.
            metric_name (str): The name of the metric to return. Available values are:
                * `pft` - Page Fetch Time
                * `dns` - DNS Time
                * `availability`

        Returns:
            :obj:`Box`: The application's ZDX metrics.

        Examples:
            Return the ZDX metrics for the application with the ID of 999999999:
            >>> zia.apps.get_app_metrics(app_id='999999999')

            Return the ZDX metrics for the app with an ID of 999999999 for the last 24 hours, including dns matrics,
            geolocation, department and location IDs:
            >>> zia.apps.get_app_metrics(app_id='999999999', since=24, metric_name='dns', location_id='888888888',
            ...                          geo_id='777777777', department_id='666666666')

        """
        return self._get(f"apps/{app_id}/metrics", params=kwargs)

    @zdx_params
    def list_app_users(self, app_id: str, **kwargs):
        """
        Returns a list of users and devices that were used to access the specified application configured within
        the ZDX tenant.

        Args:
            app_id (str): The unique ID for the ZDX application.

        Keyword Args:
            since (int): The number of hours to look back for devices.
            location_id (str): The unique ID for the location.
            department_id (str): The unique ID for the department.
            geo_id (str): The unique ID for the geolocation.
            score_bucket (str): The ZDX score bucket to filter by. Available values are:
                * `poor` - 0-33
                * `okay` - 34-65
                * `good` - 66-100

        Returns:
            :obj:`BoxList`: The list of users and devices used to access the application.

        Examples:
            Return a list of users and devices who have accessed the application with the ID of 999999999:
            >>> for user in zia.apps.get_app_users(app_id='999999999'):
            ...     print(user)

        """
        return BoxList(
            ZDXIterator(
                self._api,
                f"apps/{app_id}/users",
                pagination="offset_limit",
                **kwargs,
            )
        )

    @zdx_params
    def get_app_user(self, app_id: str, user_id: str, **kwargs):
        """
        Returns information on the specified user and device that was used to access the specified application
        configured within the ZDX tenant.

        Args:
            app_id (str): The unique ID for the ZDX application.
            user_id (str): The unique ID for the ZDX user.

        Keyword Args:
            since (int): The number of hours to look back for devices.

        Returns:
            :obj:`Box`: The user and device information.

        Examples:
            Return information on the user with the ID of 999999999 who has accessed the application with the ID of
            888888888:
            >>> zia.apps.get_app_user(app_id='888888888', user_id='999999999')

        """
        return self._get(f"apps/{app_id}/users/{user_id}", params=kwargs)
