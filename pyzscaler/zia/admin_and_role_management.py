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

    def get_admin_roles_lite(self, **kwargs):
        """
        Gets a name and ID dictionary of all admin roles. The list only includes the name and ID for all admin roles.

        Keyword Args:
            **include_auditor_users (bool, optional):
                Include or exclude auditor role information in the list.
            **include_partner_role (bool, optional):
                Include or exclude partner admin role information in the list. (default: True)

        Returns:
            :obj:`list`: The admin_users resource record.

        Example Payload Values:
            {
              "id": 0,
              "loginName": "string",
              "userName": "string",
              "email": "string",
              "role": {
                "id": 0,
                "name": "string",
                "extensions": {
                  "additionalProp1": "string",
                  "additionalProp2": "string",
                  "additionalProp3": "string"
                }
              },
              "comments": "string",
              "adminScope": {
                "scopeGroupMemberEntities": [
                  {
                    "id": 0,
                    "name": "string",
                    "extensions": {
                      "additionalProp1": "string",
                      "additionalProp2": "string",
                      "additionalProp3": "string"
                    }
                  }
                ],
                "Type": "ORGANIZATION",
                "ScopeEntities": [
                  {
                    "id": 0,
                    "name": "string",
                    "extensions": {
                      "additionalProp1": "string",
                      "additionalProp2": "string",
                      "additionalProp3": "string"
                    }
                  }
                ]
              },
              "isNonEditable": false,
              "disabled": true,
              "isAuditor": false,
              "password": "string",
              "isPasswordLoginAllowed": false,
              "isSecurityReportCommEnabled": false,
              "isServiceUpdateCommEnabled": false,
              "isProductUpdateCommEnabled": false,
              "isPasswordExpired": false,
              "isExecMobileAppEnabled": false,
              "execMobileAppTokens": [
                {
                  "cloud": "string",
                  "orgId": 0,
                  "name": "string",
                  "tokenId": "string",
                  "token": "string",
                  "tokenExpiry": 0,
                  "createTime": 0,
                  "deviceId": "string",
                  "deviceName": "string"
                }
              ]
            }

        Examples:
            >>> department = zia.admin_and_role_management.get_admin_roles_lite()

        """
        return list(Iterator(self._api, "adminRoles", **kwargs))

    def create_admin_user(self, **kwargs):
        """
        Creates an admin or auditor user.

        Args:
            **kwargs:

        Returns:

        """