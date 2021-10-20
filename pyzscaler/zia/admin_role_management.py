from restfly.endpoint import APIEndpoint

from pyzscaler.utils import Iterator


class AdminAndRoleManagementAPI(APIEndpoint):
    def get_admin_users(self, **kwargs):
        """
        Returns a list of admin users.

        Keyword Args:
            **include_auditor_users (bool, optional):
                Include or exclude auditor user information in the list.
            **include_admin_users (bool, optional):
                Include or exclude admin user information in the list. (default: True)
            **search (str, optional):
                The search string used to partially match against an admin/auditor user's Login ID or Name.
            **page (int, optional):
                Specifies the page offset.
            **page_size (int, optional):
                Specifies the page size. The default size is 100, but the maximum size is 1000.

        Returns:
            :obj:`list`: The admin_users resource record.

        Examples:
            >>> department = zia.admin_and_role_management.get_admin_users(search='login_name')

        """
        return list(Iterator(self._api, "adminUsers", **kwargs))
