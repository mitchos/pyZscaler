from restfly.endpoint import APIEndpoint
from box import Box, BoxList


class UserManagementAPI(APIEndpoint):
    """The methods within this section use the ZIA User Management API and are accessed via ``ZIA.users``."""

    def list_departments(self):
        """
        Retrieves a list of departments.

        Returns:
            :obj:`list`:
                The list of departments configured in ZIA.

        Examples:
            >>> departments = zia.users.list_departments()
        """
        return self._get('departments', box=BoxList)

    def get_department(self, id):
        """
        Returns the department details for a given department.

        Args:
            id (str):
                The unique identifier for the department.

        Returns:
            :obj:`dict`:
                The department resource record.

        Examples:
            >>> department = zia.users.get_department(id)

        """
        return self._get(f'departments/{id}')

    def list_groups(self):
        """
        Retrieves a list of user groups.

        Returns:
            :obj:`list`:
                The list of user groups configured in ZIA.

        Examples:
            >>> user_groups = zia.users.list_groups()
        """
        return self._get('groups', box=BoxList)

    def get_group(self, id):
        """
        Returns the user group details for a given user group.

        Args:
            id (str):
                The unique identifier for the user group.

        Returns:
            :obj:`dict`:
                The user group resource record.

        Examples:
            >>> user_group = zia.users.get_group(id)

        """
        return self._get(f'groups/{id}')

    def list(self):
        """
        Retrieves a list of users.

        Returns:
            :obj:`list`:
                The list of users configured in ZIA.

        Examples:
            >>> users = zia.users.list()
        """
        return self._get('users')

    def add(self, name: str, email: str, groups: list, department: object,
            password: str, **kwargs) -> None:
        """
        Creates a new ZIA user.

        Args:
            name (str):
                User name. This appears when choosing users for policies.
            email (str):
                User email consists of a user name and domain name. It does not have to be a valid email address,
                but it must be unique and its domain must belong to the organization.
            groups (list):
                List of Groups a user belongs to. Groups are used in policies.
            department (object):
            password (str):

        Keyword Args:
            **comments (str, optional):
                Additional information about this user.
            **tempAuthEmail (str, optional):
                Temporary Authentication Email. If you enabled one-time tokens or links, enter the email address to
                which the Zscaler service sends the tokens or links. If this is empty, the service will send the email
                to the User email.

        Returns:
            :obj:`dict`
                The resource record for the new user.

        """
        payload = {
            'name': name,
            'email': email,
            'groups': groups,
            'department': department,
            'comments': kwargs.get('comments', ''),
            'tempAuthEmail': kwargs.get('temp_auth_email', ''),
            'password': password
        }

        return self._post('users', json=payload)

    def bulk_delete(self, ids: list):
        """
        Bulk delete ZIA users.

        Args:
            ids (list):
                List containing id int of each user that will be deleted.

        Returns:
            :obj:`dict`
                Object containing list of users that were deleted

        Examples:
            >>> bulk_delete_users = zia.users.bulk_delete([1, 2, 3])
        """

        payload = {
            "ids": ids
        }

        return self._post('users/bulkDelete', json=payload)

    def get(self, id):
        """
        Get the user information for the specified ID.

        Args:
            id (str):

        Returns:
            :obj:`dict`
                The resource record for the requested user.

        Examples
            >>> user = zia.users.get('8312')

        """
        return self._post(f'users/{id}')

    def update(self, id):
        return self._put(f'users{id}')

    def delete(self, id):
        """
                Delete the specified user ID.

                Args:
                    id (str):

                Returns:
                    :obj:`dict`
                        The resource record for the requested user.

                Examples
                    >>> user = zia.users.get('8312')

                """
        return self._delete(f'users/{id}')
