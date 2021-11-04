from restfly.endpoint import APIEndpoint

from pyzscaler.utils import Iterator, snake_to_camel


class AdminAndRoleManagementAPI(APIEndpoint):
    def list_users(self, **kwargs):
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
            >>> users = zia.admin_and_role_management.list_users(search='login_name')

        """
        return list(Iterator(self._api, "adminUsers", **kwargs))

    def add_user(self, **kwargs):
        """
        Creates a ZIA Admin User.

        Args:
            **kwargs:
                login_name: str
                user_name: str
                email: str
                role: dict
                admin_scope: dict
                type: str
                scope_entitites: list[dict]
                is_non_editable: bool
                disabled: bool
                is_auditor: bool
                password: bool
                is_password_login_allowed: bool
                is_security_report_comm_enabled: bool
                is_service_update_comm_enabled: bool
                is_product_update_comm_enabled: bool
                is_password_expired: bool
                is_exec_mobile_app_enabled: bool
                exec_mobile_app_tokens: list[dict]

        Returns: dict of user's account

        Examples:
            >>> admin_user = zia.admin_and_role_management.add_user(
            ...    login_name='username',
            ...    user_name:'Jim Bob',
            ...    email='jim@domain.com'
            ...)

        """
        # Add parameters to payload
        payload = {}
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        return self._post("adminUsers", json=payload)
