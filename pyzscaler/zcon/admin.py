from box import Box, BoxList
from restfly import APIEndpoint

from pyzscaler.utils import convert_keys


class ZCONAdminAPI(APIEndpoint):
    def list_roles(self, **kwargs) -> BoxList:
        """
        List all existing admin roles.

        Keyword Args:
            include_auditor_role (bool): Include / exclude auditor roles in the response.
            include_partner_role (bool): Include / exclude partner roles in the response.
            include_api_roles (bool): Include / exclude API roles in the response.
            id (list): The ID of the roles to include.

        Returns:
            :obj:`BoxList`: The list of roles.

        Examples:
            Print all roles::

                for role in zcon.admin.list_roles():
                    print(role)

            Print all roles with additional parameters::

                for role in zcon.admin.list_roles(
                    include_auditor_role=True,
                    include_partner_role=True,
                    include_api_roles=True,
                ):
                    print(role)

        """
        return self._get("adminRoles")

    def get_role(self, role_id: str) -> Box:
        """
        Get details for a specific admin role.

        Args:
            role_id (str): The ID of the role to retrieve.

        Returns:
            :obj:`Box`: The role details.

        Examples:
            Print the details of a role::

                print(zcon.admin.get_role("123456789")

        """
        return self._get(f"adminRoles/{role_id}")

    def add_role(
        self,
        name: str,
        policy_access: str = "NONE",
        report_access: str = "NONE",
        username_access: str = "NONE",
        dashboard_access: str = "NONE",
        **kwargs,
    ):
        """
        Create a new admin role.

        Args:
            name (str): The name of the role.
            policy_access (str): The policy access level.
            report_access (str): The report access level.
            username_access (str): The username access level.
            dashboard_access (str): The dashboard access level.

        Keyword Args:
            feature_permissions_tuples (:obj:`List[Tuple[str, str]]`):
                A list of tuple pairs specifying the feature permissions. Each tuple contains the feature name
                (case-insensitive) and its access level.

                Accepted feature names (case-insensitive) are:

                - ``APIKEY_MANAGEMENT``
                - ``EDGE_CONNECTOR_CLOUD_PROVISIONING``
                - ``EDGE_CONNECTOR_LOCATION_MANAGEMENT``
                - ``EDGE_CONNECTOR_DASHBOARD``
                - ``EDGE_CONNECTOR_FORWARDING``
                - ``EDGE_CONNECTOR_TEMPLATE``
                - ``REMOTE_ASSISTANCE_MANAGEMENT``
                - ``EDGE_CONNECTOR_ADMIN_MANAGEMENT``
                - ``EDGE_CONNECTOR_NSS_CONFIGURATION``
            alerting_access (str): The alerting access level.
            analysis_access (str): The analysis access level.
            admin_acct_access (str): The admin account access level.
            device_info_access (str): The device info access level.

        Note:
            For access levels, the accepted values are:

            - ``NONE``
            - ``READ_ONLY``
            - ``READ_WRITE``


        Returns:
            :obj:`dict`: The newly created role.

        Examples:
            Minimum required arguments::

                zcon.admin.add_role(name="NewRole")

            Including keyword arguments::

                zcon.admin.add_role(
                    name="AdvancedRole",
                    policy_access="READ_ONLY",
                    feature_permissions_tuples=[
                        ("apikey_management", "read_only"),
                        ("EDGE_CONNECTOR_CLOUD_PROVISIONING", "NONE")
                    ],
                    alerting_access="READ_WRITE"
                )

        """
        payload = {
            "name": name,
            "role_type": "EDGE_CONNECTOR_ADMIN",
            "policy_access": policy_access,
            "report_access": report_access,
            "username_access": username_access,
            "dashboard_access": dashboard_access,
        }

        if feature_permissions_tuples := kwargs.pop("feature_permissions_tuples", None):
            payload["feature_permissions"] = {k.upper(): v for k, v in feature_permissions_tuples}

        # Add optional parameters to payload
        payload.update({k: v for k, v in kwargs.items() if v is not None})

        # Convert snake to camelcase
        payload = convert_keys(payload)

        return self._post("adminRoles", json=payload)

    def update_role(self, role_id: str, **kwargs) -> Box:
        """
        Update an existing admin role.

        Args:
            role_id (str): The ID of the role to update.

        Keyword Args:
            name (str): The name of the role.
            policy_access (str): The policy access level.
            report_access (str): The report access level.
            username_access (str): The username access level.
            dashboard_access (str): The dashboard access level.
            feature_permissions (:obj:`List[Tuple[str, str]]`):
                A list of tuple pairs specifying the feature permissions. Each tuple contains the feature name
                (case-insensitive) and its access level.

                Accepted feature names (case-insensitive) are:

                - ``APIKEY_MANAGEMENT``
                - ``EDGE_CONNECTOR_CLOUD_PROVISIONING``
                - ``EDGE_CONNECTOR_LOCATION_MANAGEMENT``
                - ``EDGE_CONNECTOR_DASHBOARD``
                - ``EDGE_CONNECTOR_FORWARDING``
                - ``EDGE_CONNECTOR_TEMPLATE``
                - ``REMOTE_ASSISTANCE_MANAGEMENT``
                - ``EDGE_CONNECTOR_ADMIN_MANAGEMENT``
                - ``EDGE_CONNECTOR_NSS_CONFIGURATION``
            alerting_access (str): The alerting access level.
            analysis_access (str): The analysis access level.
            admin_acct_access (str): The admin account access level.
            device_info_access (str): The device info access level.

        Note:
            For access levels, the accepted values are:

            - ``NONE``
            - ``READ_ONLY``
            - ``READ_WRITE``

        Returns:
            :obj:`Box`: The updated role.

        Examples:
            Update a role::

                zcon.admin.update_role(
                    role_id="123456789",
                    policy_access="READ_ONLY",
                    feature_permissions=[
                        ("apikey_management", "read_only"),
                        ("EDGE_CONNECTOR_CLOUD_PROVISIONING", "NONE")
                    ],
                    alerting_access="READ_WRITE"
                )

        """
        payload = self.get_role(role_id)

        # Pop the feature permissions out first so that we retain their format
        feature_permissions = kwargs.pop("feature_permissions", None)

        # Add optional parameters to payload
        payload.update({k: v for k, v in kwargs.items() if v is not None})

        # Convert snake to camelcase
        payload = convert_keys(payload)

        # Now update the feature permissions
        if feature_permissions:
            payload["featurePermissions"] = {k.upper(): v for k, v in feature_permissions}

        return self._put(f"adminRoles/{role_id}", json=payload)

    def delete_role(self, role_id: str) -> int:
        """
        Delete the specified admin role.

        Args:
            role_id (str): The ID of the role to delete.

        Returns:
            :obj:`int`: The status code of the operation.

        Examples:
            Delete a role::

                zcon.admin.delete_role("123456789")

        """
        return self._delete(f"adminRoles/{role_id}").status_code

    def change_password(self, username: str, old_password: str, new_password: str) -> int:
        """
        Change the password for the specified admin user.

        Args:
            username (str): The username of the admin user.
            old_password (str): The current password of the admin user.
            new_password (str): The new password for the admin user.

        Returns:
            :obj:`int`: The status code of the operation.

        Examples:
            Change a password::

                zcon.admin.change_password("jdoe", "oldpassword123", "newpassword123")

        """
        payload = {
            "userName": username,
            "oldPassword": old_password,
            "newPassword": new_password,
        }
        return self._post("passwordChange", json=payload).status_code

    def list_admins(self, **kwargs) -> BoxList:
        """
        List all existing admin users.

        Keyword Args:
            include_auditor_users (bool): Include / exclude auditor users in the response.
            include_admin_users (bool): Include / exclude admin users in the response.
            include_api_roles (bool): Include / exclude API roles in the response.
            search (str): The search string to filter by.
            page (int): The page offset to return.
            page_size (int): The number of records to return per page.
            version (int): Specifies the admins from a backup version


        Returns:
            :obj:`BoxList`: The list of admin users.

        Examples:
            List all admins::

                for admin in zcon.admin.list_admins():
                    print(admin)

            List all admins with advanced features::

                for admin in zcon.admin.list_admins(
                    include_auditor_users=True,
                    include_admin_users=True,
                    include_api_roles=True,
                ):
                    print(admin)

        """
        payload = {
            "partnerType": "EDGE_CONNECTOR_ADMIN",
        }

        # Update the payload with keyword arguments
        payload.update({k: v for k, v in kwargs.items() if v is not None})

        # Convert snake to camelcase if needed
        payload = convert_keys(payload)

        return self._get("adminUsers", params=payload)

    def get_admin(self, admin_id: str) -> Box:
        """
        Get details for a specific admin user.

        Args:
            admin_id (str): The ID of the admin user to retrieve.

        Returns:
            :obj:`Box`: The admin user details.

        Examples:
            Print the details of an admin user::

                print(zcon.admin.get_admin("123456789")

        """
        return self._get(f"adminUsers/{admin_id}")

    def add_admin(self, user_name: str, login_name: str, role: str, email: str, password: str, **kwargs) -> Box:
        """
        Create a new admin user.

        Args:
            user_name (str): The name of the admin user.
            login_name (str): The login name of the admin user.
            role (str): The role of the admin user.
            email (str): The email address of the admin user.
            password (str): The password for the admin user.

        Keyword Args:
            disabled (bool): Indicates whether the admin is disabled.
            new_location_create_allowed (bool): Indicates whether the admin can create new locations.
            admin_scope_type (str): The admin scope type.
            admin_scope_group_member_entity_ids (list): Applicable if the admin scope type is `LOCATION_GROUP`.
            is_default_admin (bool): Indicates whether the admin is the default admin.
            is_deprecated_default_admin (bool): Indicates whether this admin is deletable.
            is_auditor (bool): Indicates whether the admin is an auditor.
            is_security_report_comm_enabled (bool): Indicates whether the admin can receive security reports.
            is_service_update_comm_enabled (bool): Indicates whether the admin can receive service updates.
            is_password_login_allowed (bool): Indicates whether the admin can log in with a password.
            is_product_update_comm_enabled (bool): Indicates whether the admin can receive product updates.
            is_exec_mobile_app_enabled (bool): Indicates whether Executive Insights App access is enabled for the admin.
            send_mobile_app_invite (bool):
                Indicates whether to send an invitation email to download Executive Insights App to admin.
            send_zdx_onboard_invite (bool): Indicates whether to send an invitation email for ZDX onboarding to admin.
            comments (str): Comments for the admin user.
            name (str):
                Admin user's "friendly" name, e.g., "FirstName LastName" (this field typically matches userName.)

        Returns:
            Box: A Box object representing the newly created admin user.

        Examples:
            Create a new admin user with only the required parameters::

                zcon.admin.add_admin(
                    name="Jane Smith",
                    login_name="jsmith",
                    role="admin",
                    email="jsmith@example.com",
                    password="password123",
                    )

            Create a new admin with some additional parameters::

                zcon.admin.add_admin(
                    name="Jane Smith",
                    login_name="jsmith",
                    role="admin",
                    email="jsmith@example.com",
                    password="password123",
                    is_default_admin=False,
                    disabled=False,
                    comments="New admin user"

        """

        payload = {
            "loginName": login_name,
            "userName": user_name,
            "email": email,
            "role": role,
            "password": password,
        }

        # Add optional parameters to payload
        payload.update({k: v for k, v in kwargs.items() if v is not None})

        # Convert snake to camelcase
        payload = convert_keys(payload)

        return self._post("adminUsers", json=payload)

    def update_admin(self, admin_id: str, **kwargs) -> Box:
        """
        Update an existing admin user.

        Args:
            admin_id (str): The ID of the admin user to update.

        Keyword Args:
            role (str): The role of the admin user.
            email (str): The email address of the admin user.
            password (str): The password for the admin user.
            disabled (bool): Indicates whether the admin is disabled.
            new_location_create_allowed (bool): Indicates whether the admin can create new locations.
            admin_scope_type (str): The admin scope type.
            admin_scope_group_member_entity_ids (list): Applicable if the admin scope type is `LOCATION_GROUP`.
            is_default_admin (bool): Indicates whether the admin is the default admin.
            is_deprecated_default_admin (bool): Indicates whether this admin is deletable.
            is_auditor (bool): Indicates whether the admin is an auditor.
            is_security_report_comm_enabled (bool): Indicates whether the admin can receive security reports.
            is_service_update_comm_enabled (bool): Indicates whether the admin can receive service updates.
            is_password_login_allowed (bool): Indicates whether the admin can log in with a password.
            is_product_update_comm_enabled (bool): Indicates whether the admin can receive product updates.
            is_exec_mobile_app_enabled (bool): Indicates whether Executive Insights App access is enabled for the admin.
            send_mobile_app_invite (bool):
                Indicates whether to send an invitation email to download Executive Insights App to admin.
            send_zdx_onboard_invite (bool): Indicates whether to send an invitation email for ZDX onboarding to admin.
            comments (str): Comments for the admin user.
            name (str):
                Admin user's "friendly" name, e.g., "FirstName LastName" (this field typically matches userName.)

        Returns:
            Box: A Box object representing the updated admin user.

        Examples:
            Update an admin user::

                zcon.admin.update_admin(
                    admin_id="123456789",
                    admin_scope_type="LOCATION_GROUP",
                    comments="Updated admin user",
                )

        """

        payload = self.get_admin(admin_id)

        # Add optional parameters to payload
        payload.update({k: v for k, v in kwargs.items() if v is not None})

        # Convert snake to camelcase
        payload = convert_keys(payload)

        return self._put(f"adminUsers/{admin_id}", json=payload)

    def delete_admin(self, admin_id: str) -> int:
        """
        Delete the specified admin user.

        Args:
            admin_id (str): The ID of the admin user to delete.

        Returns:
            :obj:`int`: The status code of the operation.

        Examples:
            Delete an admin user::

                zcon.admin.delete_admin("123456789")

        """
        return self._delete(f"adminUsers/{admin_id}").status_code

    def list_api_keys(self, **kwargs) -> BoxList:
        """
        List all existing API keys.

        Keyword Args:
            include_partner_keys (bool): Include / exclude partner keys in the response.

        Returns:
            :obj:`BoxList`: The list of API keys.

        Examples:
            List all API keys::

                for api_key in zcon.admin.list_api_keys():
                    print(api_key)
        """
        params = {}
        if "include_partner_keys" in kwargs:
            params["includePartnerKeys"] = kwargs["include_partner_keys"]

        return self._get("apiKeys", params=params)

    def regenerate_api_key(self, api_key_id: str) -> Box:
        """
        Regenerate the specified API key.

        Args:
            api_key_id (str): The ID of the API key to regenerate.

        Returns:
            :obj:`Box`: The regenerated API key.

        Examples:
            Regenerate an API key::

                print(zcon.admin.regenerate_api_key("123456789"))

        """
        return self._post(f"apiKeys/{api_key_id}/regenerate")
