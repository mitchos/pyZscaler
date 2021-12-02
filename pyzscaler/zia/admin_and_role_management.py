from box import Box, BoxList
from restfly.endpoint import APIEndpoint

from pyzscaler.utils import Iterator, snake_to_camel


class AdminAndRoleManagementAPI(APIEndpoint):
    def add_user(self, name: str, login_name: str, email: str, password: str, **kwargs) -> Box:
        """
        Adds a new admin user to ZIA.

        Args:
            name (str): The user's full name.
            login_name (str):
                The name that the admin user will use to login to ZIA in email format, i.e. `user@domain.tld.`
            email (str): The email address for the admin user.
            password (str): The password for the admin user.
            **kwargs: Optional keyword args.

        Keyword Args:
            admin_scope (str): The scope of the admin's permissions, accepted values are:
                ``organization``, ``department``, ``location``, ``location_group``
            comments (str): Additional information about the admin user.
            disabled (bool): Set to ``True`` if you want the account disabled upon creation.
            is_password_login_allowed (bool): Set to ``True`` to allow password login.
            is_security_report_comm_enabled (bool):
                Set to ``True`` to allow ZIA Security Update emails to be sent to the admin user.
            is_service_update_comm_enabled (bool):
                Set to ``True`` to allow ZIA Service Update emails to be sent to the admin user.
            is_product_update_comm_enabled (bool):
                Set to ``True`` to allow ZIA Product Update emails to be sent to the admin user.
            is_password_expired (bool):
                Set to ``True`` to expire the admin user's password upon creation.
            is_exec_mobile_app_enabled (bool):
                Set to ``True`` to enable to executive insights mobile application for the admin user.
            role_id (str): The unique id for the admin role being assigned to the admin user.
            scope_ids (list):
                A list of entity ids for the admin user's scope. e.g. if the admin user has admin_scope set to
                ``department`` then you will need to provide a list of department ids.

                **NOTE**: This param doesn't need to
                be provided if the admin user's scope is set to ``organization``.

        Returns:
            :obj:`Box`: The newly created admin user resource record.

        Examples:
            Add an admin user with the minimum required params:

            >>> admin_user = zia.admin_and_role_management.add_user(
            ...    name="Jim Bob",
            ...    login_name="jim@example.com",
            ...    password="hunter2",
            ...    email="jim@example.com")

            Add an admin user with a department admin scope:

            >>> admin_user = zia.admin_and_role_management.add_user(
            ...    name="Jane Bob",
            ...    login_name="jane@example.com",
            ...    password="hunter3",
            ...    email="jane@example.com,
            ...    admin_scope="department",
            ...    scope_ids = ['376542', '245688'])

            Add an auditor user:

            >>> auditor_user = zia.admin_and_role_management.add_user(
            ...    name="Head Bob",
            ...    login_name="head@example.com",
            ...    password="hunter4",
            ...    email="head@example.com,
            ...    is_auditor=True)

        """
        payload = {
            "userName": name,
            "loginName": login_name,
            "email": email,
            "password": password,
        }

        # Get the admin scope if provided
        admin_scope = kwargs.pop("admin_scope", None)

        # The default admin scope is organization so we don't really need to
        # send it to ZIA as part of this API call. Otherwise if the user has
        # supplied something different then we want to explicitly set that for
        # the adminScopeType.
        if admin_scope and admin_scope != "organization":
            payload["adminScopeType"] = admin_scope.upper()
            payload["adminScopeScopeEntities"] = []

        # Add optional parameters to payload
        for key, value in kwargs.items():
            # If the user has supplied ids for the admin scope then we'll add
            # them to the payload here. If the user doesn't supply them then
            # ZIA will return an error.
            if key == "scope_ids":
                for scope_id in value:
                    payload["adminScopeScopeEntities"].append({"id": scope_id})
            elif key == "role_id":
                payload["role"] = {"id": value}
            else:
                payload[snake_to_camel(key)] = value

        return self._post("adminUsers", json=payload)

    def list_users(self, **kwargs) -> BoxList:
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
            :obj:`BoxList`: The admin_users resource record.

        Examples:
            >>> users = zia.admin_and_role_management.list_users(search='login_name')

        """
        return BoxList(Iterator(self._api, "adminUsers", **kwargs))

    def list_roles(self, **kwargs) -> BoxList:
        """
        Return a list of the configured admin roles in ZIA.

        Args:
            **kwargs: Optional keyword args.

        Keyword Args:
            include_auditor_role (bool): Set to ``True`` to include auditor role information in the response.
            include_partner_role (bool): Set to ``True`` to include partner admin role information in the response.

        Returns:
            :obj:`BoxList`: A list of admin role resource records.

        Examples:
            Get a list of all configured admin roles:

            >>> roles = zia.admin_and_management_roles.list_roles()

        """
        payload = {snake_to_camel(key): value for key, value in kwargs.items()}

        return self._get("adminRoles/lite", params=payload)

    def get_user(self, user_id: str) -> Box:
        """
        Returns information on the specified admin user id.

        Args:
            user_id (str): The unique id of the admin user.

        Returns:
            :obj:`Box`: The admin user resource record.

        Examples:
            >>> print(zia.admin_and_role_management.get_user('987321202'))

        """
        admin_user = next(user for user in self.list_users() if user.id == int(user_id))

        return admin_user

    def delete_user(self, user_id: str) -> int:
        """
        Deletes the specified admin user by id.

        Args:
            user_id (str): The unique id of the admin user.

        Returns:
            :obj:`int`: The response code for the request.

        Examples:
            >>> zia.admin_role_management.delete_admin_user('99272455')

        """

        return self._delete(f"adminUsers/{user_id}", box=False).status_code

    def update_user(self, user_id: str, **kwargs) -> dict:
        """
        Update an admin user.

        Args:
            user_id (str): The unique id of the admin user to be updated.
            **kwargs: Optional keyword args.

        Keyword Args:
            admin_scope (str): The scope of the admin's permissions, accepted values are:
                ``organization``, ``department``, ``location``, ``location_group``
            comments (str): Additional information about the admin user.
            disabled (bool): Set to ``True`` if you want the account disabled upon creation.
            email (str): The email address for the admin user.
            is_password_login_allowed (bool): Set to ``True`` to allow password login.
            is_security_report_comm_enabled (bool):
                Set to ``True`` to allow ZIA Security Update emails to be sent to the admin user.
            is_service_update_comm_enabled (bool):
                Set to ``True`` to allow ZIA Service Update emails to be sent to the admin user.
            is_product_update_comm_enabled (bool):
                Set to ``True`` to allow ZIA Product Update emails to be sent to the admin user.
            is_password_expired (bool):
                Set to ``True`` to expire the admin user's password upon creation.
            is_exec_mobile_app_enabled (bool):
                Set to ``True`` to enable to executive insights mobile application for the admin user.
            name (str): The user's full name.
            password (str): The password for the admin user.
            role_id (str): The unique id for the admin role being assigned to the admin user.
            scope_ids (list):
                A list of entity ids for the admin user's scope. e.g. if the admin user has ``admin_scope`` set to
                ``department`` then you will need to provide a list of department ids.

                **NOTE:** This param doesn't need to
                be provided if the admin user's scope is set to `organization`.

        Returns:
            :obj:`dict`: The updated admin user resource record.

        Examples:
            Update the email address for an admin user:

            >>> user = zia.admin_and_role_management.update_user('99695301',
            ...    email='jimbob@example.com')

            Update the admin scope for an admin user to department:

            >>> user = zia.admin_and_role_management.update_user('99695301',
            ...    admin_scope='department',
            ...    scope_ids=['3846532', '3846541'])

        """

        # Get the resource record for the provided user id
        payload = {snake_to_camel(k): v for k, v in self.get_user(user_id).items()}

        # Get the admin scope if provided
        admin_scope = kwargs.pop("admin_scope", None)

        # The default admin scope is organization so we don't really need to
        # send it to ZIA as part of this API call. Otherwise if the user has
        # supplied something different then we want to explicitly set that for
        # the adminScopeType.
        if admin_scope and admin_scope != "organization":
            payload["adminScopeType"] = admin_scope.upper()
            payload["adminScopeScopeEntities"] = []

        # Add optional parameters to payload
        for key, value in kwargs.items():
            # If the user has supplied ids for the admin scope then we'll add
            # them to the payload here. If the user doesn't supply them then
            # ZIA will return an error.
            if key == "scope_ids":
                for scope_id in value:
                    payload["adminScopeScopeEntities"].append({"id": scope_id})
            elif key == "name":
                # We renamed the username param to make it more meaningful for pyZscaler users
                payload["userName"] = value
            else:
                payload[snake_to_camel(key)] = value

        return self._put(f"adminUsers/{user_id}", json=payload)
