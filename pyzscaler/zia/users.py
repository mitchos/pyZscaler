from restfly.endpoint import APIEndpoint
from box import BoxList


class UserManagementAPI(APIEndpoint):
    """
    The methods within this section use the ZIA User Management API and are accessed via ``ZIA.users``.

    """

    def list_departments(self):
        """
        Returns the list of departments.

        Returns:
            :obj:`list`: The list of departments configured in ZIA.

        Examples:
            >>> departments = zia.users.list_departments()
        """
        return self._get("departments", box=BoxList)

    def get_department(self, department_id: str):
        """
        Returns the department details for a given department.

        Args:
            department_id (str): The unique identifier for the department.

        Returns:
            :obj:`dict`: The department resource record.

        Examples:
            >>> department = zia.users.get_department('45543434')

        """
        return self._get(f"departments/{department_id}")

    def list_groups(self):
        """
        Returns the list of user groups.

        Returns:
            :obj:`list`: The list of user groups configured in ZIA.

        Examples:
            >>> user_groups = zia.users.list_groups()

        """
        return self._get("groups", box=BoxList)

    def get_group(self, group_id: str):
        """
        Returns the user group details for a given user group.

        Args:
            group_id (str): The unique identifier for the user group.

        Returns:
            :obj:`dict`: The user group resource record.

        Examples:
            >>> user_group = zia.users.get_group('4987453')

        """
        return self._get(f"groups/{group_id}")

    def list_users(self):
        """
        Returns the list of users.

        Returns:
            :obj:`list`: The list of users configured in ZIA.

        Examples:
            >>> users = zia.users.list_users()

        """
        return self._get("users", box=BoxList)

    def add_user(self, name: str, email: str, groups: list, department: dict, **kwargs):
        """
        Creates a new ZIA user.

        Args:
            name (str):
                User name.
            email (str):
                User email consists of a user name and domain name. It does not have to be a valid email address,
                but it must be unique and its domain must belong to the organisation.
            groups (list):
                List of Groups a user belongs to.
            department (dict):
                The department the user belongs to.

        Keyword Args:
            **comments (str):
                Additional information about this user.
            **tempAuthEmail (str):
                Temporary Authentication Email. If you enabled one-time tokens or links, enter the email address to
                which the Zscaler service sends the tokens or links. If this is empty, the service will send the
                email to the User email.
            **adminUser (bool):
                True if this user is an Admin user.
            **password (str):
                User's password. Applicable only when authentication type is Hosted DB. Password strength must follow
                what is defined in the auth settings.
            **type (str):
                User type. Provided only if this user is not an end user. Accepted values are SUPERADMIN, ADMIN,
                AUDITOR, GUEST, REPORT_USER and UNAUTH_TRAFFIC_DEFAULT.

        Returns:
            :obj:`dict`: The resource record for the new user.

        Examples:
            Add a user with the minimum required params:

            >>> zia.users.add_user(name='Jane Doe',
            ...    email='jane.doe@example.com',
            ...    groups=[{
            ...      'id': '49916183'}]
            ...    department={
            ...      'id': '49814321'})

        """
        payload = {
            "name": name,
            "email": email,
            "groups": groups,
            "department": department,
        }

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[key] = value

        return self._post("users", json=payload)

    def bulk_delete_users(self, user_ids: list):
        """
        Bulk delete ZIA users.

        Args:
            user_ids (list): List containing id int of each user that will be deleted.

        Returns:
            :obj:`dict`: Object containing list of users that were deleted

        Examples:
            >>> bulk_delete_users = zia.users.bulk_delete_users(['49272455', '49272456', '49272457'])

        """

        payload = {"ids": user_ids}

        return self._post("users/bulkDelete", json=payload)

    def get_user(self, user_id: str):
        """
        Returns the user information for the specified ID.

        Args:
            user_id (str): The unique identifier for the requested user.

        Returns:
            :obj:`dict`: The resource record for the requested user.

        Examples
            >>> user = zia.users.get_user('8312')

        """
        return self._get(f"users/{user_id}")

    def update_user(
            self,
            user_id: str,
            name: str = None,
            email: str = None,
            department: dict = None,
            groups: list = None,
            **kwargs,
    ):
        """
        Updates the details for the specified user.

        Args:
            user_id (str):
                The unique identifier for the user.
            name (str, optional):
                The updated name. Defaults to existing name if not specified.
            email (str, optional):
                The updated email. Defaults to existing email if not specified.
            department (dict, optional):
                The updated department object. Defaults to existing department if not specified.
            groups (:obj:`list` of :obj:`dict`, optional):
                The updated list of groups. Defaults to existing groups if not specified.
            **kwargs:
                Optional parameters

        Keyword Args:
            **comments (str):
                Additional information about this user.
            **tempAuthEmail (str):
                Temporary Authentication Email. If you enabled one-time tokens or links, enter the email address to
                which the Zscaler service sends the tokens or links. If this is empty, the service will send the
                email to the User email.
            **adminUser (bool):
                True if this user is an Admin user.
            **password (str):
                User's password. Applicable only when authentication type is Hosted DB. Password strength must follow
                what is defined in the auth settings.
            **type (str):
                User type. Provided only if this user is not an end user. Accepted values are SUPERADMIN, ADMIN,
                AUDITOR, GUEST, REPORT_USER and UNAUTH_TRAFFIC_DEFAULT.

        Returns:
            :obj:`dict`: The resource record of the updated user.

        Examples:
            Update the user name:

            >>> zia.users.update_user('49272455',
            ...      name='Joe Bloggs')

            Update the email and add a comment:

            >>> zia.users.update_user('47272455',
            ...      name='Joe Bloggs',
            ...      comment='External auditor.')

        """

        # Cache the user record to avoid multiple API calls
        user_record = self.get_user(user_id)

        # Assign existing values to params if we're not changing them
        if not name:
            name = user_record.name
        if not email:
            email = user_record.email
        if not department:
            department = user_record.department
        if not groups:
            groups = user_record.groups

        payload = {
            "name": name,
            "email": email,
            "department": department,
            "groups": groups,
        }

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[key] = value

        return self._put(f"users/{user_id}", json=payload)

    def delete_user(self, user_id: str):
        """
        Deletes the specified user ID.

        Args:
            user_id (str): The unique identifier of the user that will be deleted.

        Returns:
            :obj:`dict`: The response code for the request.

        Examples
            >>> user = zia.users.delete_user('49272455')

        """
        return self._delete(f"users/{user_id}", box=False).status_code
