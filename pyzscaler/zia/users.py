from box import Box, BoxList
from restfly.endpoint import APIEndpoint

from pyzscaler.utils import Iterator, convert_keys, snake_to_camel


class UserManagementAPI(APIEndpoint):
    """
    The methods within this section use the ZIA User Management API and are accessed via ``ZIA.users``.

    """

    def list_departments(self, **kwargs) -> BoxList:
        """
        Returns the list of departments.

        Keyword Args:
            **limit_search (bool, optional):
                Limits the search to match against the department name only.
            **max_items (int, optional):
                The maximum number of items to request before stopping iteration.
            **max_pages (int, optional):
                The maximum number of pages to request before stopping iteration.
            **page_size (int, optional):
                Specifies the page size. The default size is 100, but the maximum size is 1000.
            **search (str, optional):
                The search string used to match against a department's name or comments attributes.

        Returns:
            :obj:`BoxList`: The list of departments configured in ZIA.

        Examples:
            List departments using default settings:

            >>> for department in zia.users.list_departments():
            ...   print(department)

            List departments, limiting to a maximum of 10 items:

            >>> for department in zia.users.list_departments(max_items=10):
            ...    print(department)

            List departments, returning 200 items per page for a maximum of 2 pages:

            >>> for department in zia.users.list_departments(page_size=200, max_pages=2):
            ...    print(department)
        """
        return BoxList(Iterator(self._api, "departments", **kwargs))

    def get_department(self, department_id: str) -> Box:
        """
        Returns the department details for a given department.

        Args:
            department_id (str): The unique identifier for the department.

        Returns:
            :obj:`Box`: The department resource record.

        Examples:
            >>> department = zia.users.get_department('99999')

        """
        return self._get(f"departments/{department_id}")

    def list_groups(self, **kwargs) -> BoxList:
        """
        Returns the list of user groups.

        Keyword Args:
            **max_items (int, optional):
                The maximum number of items to request before stopping iteration.
            **max_pages (int, optional):
                The maximum number of pages to request before stopping iteration.
            **page_size (int, optional):
                Specifies the page size. The default size is 100, but the maximum size is 1000.
            **search (str, optional):
                The search string used to match against a group's name or comments attributes.

        Returns:
            :obj:`BoxList`: The list of user groups configured in ZIA.

        Examples:
            List groups using default settings:

            >>> for group in zia.users.list_groups():
            ...    print(group)

            List groups, limiting to a maximum of 10 items:

            >>> for group in zia.users.list_groups(max_items=10):
            ...    print(group)

            List groups, returning 200 items per page for a maximum of 2 pages:

            >>> for group in zia.users.list_groups(page_size=200, max_pages=2):
            ...    print(group)

        """
        return BoxList(Iterator(self._api, "groups", **kwargs))

    def get_group(self, group_id: str) -> Box:
        """
        Returns the user group details for a given user group.

        Args:
            group_id (str): The unique identifier for the user group.

        Returns:
            :obj:`Box`: The user group resource record.

        Examples:
            >>> user_group = zia.users.get_group('99999')

        """
        return self._get(f"groups/{group_id}")

    def list_users(self, **kwargs) -> BoxList:
        """
        Returns the list of users.

        Keyword Args:
            **dept (str, optional):
                Filters by department name. This is a `starts with` match.
            **group (str, optional):
                Filters by group name. This is a `starts with` match.
            **max_items (int, optional):
                The maximum number of items to request before stopping iteration.
            **max_pages (int, optional):
                The maximum number of pages to request before stopping iteration.
            **name (str, optional):
                Filters by user name. This is a `partial` match.
            **page_size (int, optional):
                Specifies the page size. The default size is 100, but the maximum size is 1000.

        Returns:
            :obj:`BoxList`: The list of users configured in ZIA.

        Examples:
            List users using default settings:

            >>> for user in zia.users.list_users():
            ...    print(user)

            List users, limiting to a maximum of 10 items:

            >>> for user in zia.users.list_users(max_items=10):
            ...    print(user)

            List users, returning 200 items per page for a maximum of 2 pages:

            >>> for user in zia.users.list_users(page_size=200, max_pages=2):
            ...    print(user)

        """
        return BoxList(Iterator(self._api, "users", **kwargs))

    def add_user(self, name: str, email: str, groups: list, department: dict, **kwargs) -> Box:
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
            :obj:`Box`: The resource record for the new user.

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

    def bulk_delete_users(self, user_ids: list) -> Box:
        """
        Bulk delete ZIA users.

        Args:
            user_ids (list): List containing id int of each user that will be deleted.

        Returns:
            :obj:`Box`: Object containing list of users that were deleted.

        Examples:
            >>> bulk_delete_users = zia.users.bulk_delete_users(['99999', '88888', '77777'])

        """

        payload = {"ids": user_ids}

        return self._post("users/bulkDelete", json=payload)

    def get_user(self, user_id: str = None, email: str = None) -> Box:
        """
        Returns the user information for the specified ID or email.

        Args:
            user_id (optional, str): The unique identifier for the requested user.
            email (optional, str): The unique email for the requested user.

        Returns:
            :obj:`Box`: The resource record for the requested user.

        Examples
            >>> user = zia.users.get_user('99999')

            >>> user = zia.users.get_user(email='jane.doe@example.com')

        """

        if user_id and email:
            raise ValueError("TOO MANY ARGUMENTS: Expected either a user_id or an email. Both were provided.")

        elif email:
            user = (record for record in self.list_users(search=email) if record.email == email)
            return next(user, None)

        return self._get(f"users/{user_id}")

    def update_user(
        self,
        user_id: str,
        name: str = None,
        email: str = None,
        department: dict = None,
        groups: list = None,
        **kwargs,
    ) -> Box:
        """
        Updates the details for the specified user.

        Args:
            user_id (str):
                The unique identifier for the user.
            **kwargs:
                Optional parameters

        Keyword Args:
            **adminUser (bool):
                True if this user is an Admin user.
            **comments (str):
                Additional information about this user.
            **department (dict, optional):
                The updated department object. Defaults to existing department if not specified.
            **email (str, optional):
                The updated email. Defaults to existing email if not specified.
            **groups (:obj:`list` of :obj:`dict`, optional):
                The updated list of groups. Defaults to existing groups if not specified.
            **name (str, optional):
                The updated name. Defaults to existing name if not specified.
            **password (str):
                User's password. Applicable only when authentication type is Hosted DB. Password strength must follow
                what is defined in the auth settings.
            **tempAuthEmail (str):
                Temporary Authentication Email. If you enabled one-time tokens or links, enter the email address to
                which the Zscaler service sends the tokens or links. If this is empty, the service will send the
                email to the User email.
            **type (str):
                User type. Provided only if this user is not an end user. Accepted values are SUPERADMIN, ADMIN,
                AUDITOR, GUEST, REPORT_USER and UNAUTH_TRAFFIC_DEFAULT.

        Returns:
            :obj:`Box`: The resource record of the updated user.

        Examples:
            Update the user name:

            >>> zia.users.update_user('99999',
            ...      name='Joe Bloggs')

            Update the email and add a comment:

            >>> zia.users.update_user('99999',
            ...      name='Joe Bloggs',
            ...      comment='External auditor.')

        """
        payload = convert_keys(self.get_user(user_id))

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        return self._put(f"users/{user_id}", json=payload)

    def delete_user(self, user_id: str) -> int:
        """
        Deletes the specified user ID.

        Args:
            user_id (str): The unique identifier of the user that will be deleted.

        Returns:
            :obj:`int`: The response code for the request.

        Examples
            >>> user = zia.users.delete_user('99999')

        """
        return self._delete(f"users/{user_id}", box=False).status_code
