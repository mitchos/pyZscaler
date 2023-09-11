from box import Box, BoxList
from restfly import APIEndpoint

from pyzscaler.utils import convert_keys


class AdminAPI(APIEndpoint):
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
            >>> print(zcon.admin.get_role("123456789")

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
            feature_permissions_tuples (List[Tuple[str, str]]): A list of tuple pairs specifying the feature
                permissions. Each tuple contains the feature name (case-insensitive) and its access level.

                Accepted feature names (case-insensitive) are:
                - "APIKEY_MANAGEMENT"
                - "EDGE_CONNECTOR_CLOUD_PROVISIONING"
                - "EDGE_CONNECTOR_LOCATION_MANAGEMENT"
                - "EDGE_CONNECTOR_DASHBOARD"
                - "EDGE_CONNECTOR_FORWARDING"
                - "EDGE_CONNECTOR_TEMPLATE"
                - "REMOTE_ASSISTANCE_MANAGEMENT"
                - "EDGE_CONNECTOR_ADMIN_MANAGEMENT"
                - "EDGE_CONNECTOR_NSS_CONFIGURATION"

            alerting_access (str): The alerting access level.
            analysis_access (str): The analysis access level.
            admin_acct_access (str): The admin account access level.
            device_info_access (str): The device info access level.

        Note:
            For access levels, the accepted values are:
            - "NONE"
            - "READ_ONLY"
            - "READ_WRITE"

        Examples:
            Minimum required arguments:
            ```python
            add_role(name="NewRole")
            ```

            Including keyword arguments:
            ```python
            add_role(
                name="AdvancedRole",
                policy_access="READ_ONLY",
                feature_permissions_tuples=[("apikey_management", "read_only"), ("EDGE_CONNECTOR_CLOUD_PROVISIONING", "NONE")],
                alerting_access="READ_WRITE"
            )
            ```

        Returns:
            :obj:`dict`: The newly created role.

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
        for key, value in kwargs.items():
            payload[key] = value

        # Convert snake to camelcase
        payload = convert_keys(payload)

        return self._post("adminRoles", json=payload)

    def delete_role(self, role_id: str) -> int:
        """
        Delete the specified admin role.

        Args:
            role_id (str): The ID of the role to delete.

        Returns:
            :obj:`int`: The status code of the operation.

        Examples:
            >>> zcon.admin.delete_role("123456789")

        """
        return self._delete(f"adminRoles/{role_id}").status

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
            >>> zcon.admin.change_password(
            ...     username="admin@example.com",
            ...     old_password="MyInsecurePassword",
            ...     new_password="MyNewInsecurePassword")
        """
        payload = {
            "username": username,
            "oldPassword": old_password,
            "newPassword": new_password,
        }
        return self._post("admin/passwordChange", json=payload).status

    def list_admins(self, **kwargs) -> BoxList:
        """
        List all existing admin users.

        Keyword Args:
            include_auditor_users (bool): Include / exclude auditor users in the response.
            include_admin_users (bool): Include / exclude admin users in the response.
            include_api_roles (bool): Include / exclude API roles in the response.
            partner_type (str): The partner type to filter by. Available values are:
                - ``ANY``
                - ``ORG_ADMIN``
                - ``SDWAN``
                - ``MSFT_VIRTUAL_WAN``
                - ``PUBLIC_API``
                - ``EXEC_INSIGHT``
                - ``EXEC_INSIGHT_AND_ORG_ADMIN``
                - ``ZDX_ADMIN``
                - ``EDGE_CONNECTOR_ADMIN``
                - ``CSPM_ADMIN``
                - ``ZSCALER_DECEPTION_ADMIN``
                - ``ZSCALER_DECEPTION_SUPER_ADMIN``
            search (str): The search string to filter by.
            page (int): The page offset to return.
            page_size (int): The number of records to return per page.
            version (int): Specifies the admins from a backup version


        Returns:
            :obj:`BoxList`: The list of admin users.

        """
        return self._get("adminUsers")

    def get_admin(self, admin_id: str) -> Box:
        """
        Get details for a specific admin user.

        Args:
            admin_id (str): The ID of the admin user to retrieve.

        Returns:
            :obj:`Box`: The admin user details.

        Examples:
            >>> print(zcon.admin.get_admin("123456789")

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
            is_default_admin (bool): Indicates whether the admin is the default admin.
            disabled (bool): Indicates whether the admin is disabled.
            is_password_login_allowed (bool): Indicates whether the admin can log in with a password.
            new_location_create_allowed (bool): Indicates whether the admin can create new locations.
            admin_scope_type (str):
                The admin scope type. An admin's scope can be limited to certain resources,
                policies, or reports. An admin's scope can be limited by:
                    - ``ORGANIZATION``
                    - ``DEPARTMENT``
                    - ``LOCATION``
                    - ``LOCATION_GROUP``
                If not specified, the scope defaults to ``ORGANIZATION``.
            admin_scope_group_member_entity_ids (list):
                The IDs of the entities to include in the admin's scope. Only applicable if the admin scope type is
                ``LOCATION_GROUP``.
            is_deprecated_default_admin (bool):
                Indicates whether this admin is deletable. If true, this admin is read-only and not deletable.
            is_auditor (bool): Indicates whether the admin is an auditor.
            is_security_report_comm_enabled (bool): Indicates whether the admin can receive security reports.
            is_service_update_comm_enabled (bool): Indicates whether the admin can receive service updates.
            is_product_update_comm_enabled (bool): Indicates whether the admin can receive product updates.
            is_exec_mobile_app_enabled (bool): Indicates whether Executive Insights App access is enabled for the admin.
            send_mobile_app_invite (bool): Indicates whether to send an invitation email to download Executive Insights
                App to admin.
            send_zdx_onboard_invite (bool): Indicates whether to send an invitation email for ZDX onboarding to admin.
            comments (str): Comments for the admin user.
            name (str): Admin user's "friendly" name, e.g., "FirstName LastName" (this field typically matches userName.)

        Returns:
            Box: A Box object representing the newly created admin user.

        Examples:
            >>> # Create a new admin with only the required parameters
            >>> zcon.admin.add_admin("John Doe", "jdoe", "admin", "jdoe@example.com", "password123")

            >>> # Create a new admin with some additional parameters
            >>> zcon.admin.add_admin("Jane Smith", "jsmith", "admin", "jsmith@example.com", "password123",
            ...           is_default_admin=False, disabled=False, comments="New admin user")

        """
        payload = {
            "loginName": login_name,
            "userName": user_name,
            "email": email,
            "role": role,
            "password": password,
        }

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[key] = value

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
            is_default_admin (bool): Indicates whether the admin is the default admin.
            disabled (bool): Indicates whether the admin is disabled.
            is_password_login_allowed (bool): Indicates whether the admin can log in with a password.
            new_location_create_allowed (bool): Indicates whether the admin can create new locations.
            admin_scope_type (str):
                The admin scope type. An admin's scope can be limited to certain resources,
                policies, or reports. An admin's scope can be limited by:
                    - ``ORGANIZATION``
                    - ``DEPARTMENT``
                    - ``LOCATION``
                    - ``LOCATION_GROUP``
                If not specified, the scope defaults to ``ORGANIZATION``.
            admin_scope_group_member_entity_ids (list):
                The IDs of the entities to include in the admin's scope. Only applicable if the admin scope type is
                ``LOCATION_GROUP``.
            is_deprecated_default_admin (bool):
                Indicates whether this admin is deletable. If true, this admin is read-only and not deletable.
            is_auditor (bool): Indicates whether the admin is an auditor.
            is_security_report_comm_enabled (bool): Indicates whether the admin can receive security reports.
            is_service_update_comm_enabled (bool): Indicates whether the admin can receive service updates.
            is_product_update_comm_enabled (bool): Indicates whether the admin can receive product updates.
            is_exec_mobile_app_enabled (bool): Indicates whether Executive Insights App access is enabled for the admin.
            send_mobile_app_invite (bool): Indicates whether to send an invitation email to download Executive Insights
                App to admin.
            send_zdx_onboard_invite (bool): Indicates whether to send an invitation email for ZDX onboarding to admin.
            comments (str): Comments for the admin user.
            name (str): Admin user's "friendly" name, e.g., "FirstName LastName" (this field typically matches userName.)

        Returns:
            Box: A Box object representing the updated admin user.

        Examples:
            >>> # Update an admin user's role
            >>> update_admin("123", role="super_admin")

            >>> # Update multiple fields for an admin user
            >>> update_admin("123", role="super_admin", email="newemail@example.com", comments="Role updated to super admin")

        """
        payload = self.get_admin(admin_id)

        # Add optional parameters to payload
        for key, value in kwargs.items():
            if value is not None:
                payload[key] = value

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
            >>> zcon.admin.delete_admin("123456789")

        """
        return self._delete(f"adminUsers/{admin_id}").status
