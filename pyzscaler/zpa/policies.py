from restfly.endpoint import APIEndpoint

from pyzscaler.utils import snake_to_camel


class PolicySetsAPI(APIEndpoint):
    @staticmethod
    def _create_conditions(conditions):
        """
        Creates a dict template for feeding conditions into the ZPA Policies API when adding or updating a policy.

        Args:
            conditions (list): List of condition tuples.

        Returns:
            :obj:`dict`: The conditions template.

        """

        template = []

        for condition in conditions:
            if isinstance(condition, tuple) and len(condition) == 3:
                operand = {
                    "operands": [
                        {
                            "objectType": condition[0].upper(),
                            "lhs": condition[1],
                            "rhs": condition[2],
                        }
                    ]
                }
                template.append(operand)

        return template

    def list_policies(self, policy_type: str):
        """
        Returns the policy and rule sets for the given policy type.

        Args:
            policy_type (str): The type of policy to be returned. Accepted values are:

                 |  `access`
                 |  `timeout`
                 |  `client_forwarding`

        Returns:
            :obj:`dict`: Resource record of the specified policy.

        Examples:
            Request the specified Policy.

            >>> pprint(zpa.policies.list_policies('access'))

        """
        # Rename policy type to names that ZPA API is expecting.
        if policy_type == "access":
            policy_type = "global"
        elif policy_type == "timeout":
            policy_type = "reauth"
        elif policy_type == "client_forwarding":
            policy_type = "bypass"

        return self._get(f"policySet/{policy_type}")

    def get_rule(self, policy_type: str, rule_id: str):
        """
        Returns the specified policy rule.

        Args:
            policy_type (str): The type of policy to be returned. Accepted values are:

                 |  `access`
                 |  `timeout`
                 |  `client_forwarding`
            rule_id (str): The unique identifier for the policy rule.

        Returns:
            :obj:`dict`: The resource record for the requested rule.

        Examples:
            >>> policy_rule = zpa.policies.get_rule(policy_id='234234234344',
            ...    rule_id='23456546546456')

        """
        # Get the policy id for the supplied policy_type
        _policy_id = self.list_policies(policy_type).id

        return self._get(f"policySet/{_policy_id}/rule/{rule_id}")

    def list_rules(self, policy_type: str):
        """
        Returns policy rules for a given policy type.

        Args:
            policy_type (str):
                The policy type. Accepted values are:

                |  `access` - returns Access Policy rules
                |  `timeout` - returns Timeout Policy rules
                |  `client_forwarding` - returns Client Forwarding Policy rules

        Returns:
            :obj:`list`: A list of all policy rules that match the requested type.

        Examples:
            >>> for policy in zpa.policies.list_type('type')
            ...    pprint(policy)

        """

        # Rename policy type to names that ZPA API is expecting.
        if policy_type == "access":
            policy_type = "GLOBAL_POLICY"
        elif policy_type == "timeout":
            policy_type = "REAUTH_POLICY"
        elif policy_type == "client_forwarding":
            policy_type = "BYPASS_POLICY"

        return self._get(f"policySet/rules/policyType/{policy_type}").list

    def delete_rule(self, policy_type: str, rule_id: str):
        """
        Deletes the specified policy rule.

        Args:
            policy_type (str):
                The type of policy the rule belongs to. Accepted values are:

                 |  `access`
                 |  `timeout`
                 |  `client_forwarding`
            rule_id (str):
                The unique identifier for the policy rule.

        Returns:
            :obj:`str`: The response code for the operation.

        Examples:
            >>> zpa.policies.delete_rule(policy_id='2342567567355535',
            ...    rule_id='23322646655778')

        """

        # Get policy id for specified policy type
        _policy_id = self.list_policies(policy_type).id

        return self._delete(f"policySet/{_policy_id}/rule/{rule_id}")

    def add_access_rule(self, name: str, action: str, **kwargs):
        """
        Add a new Access Policy rule.

        See the `ZPA Access Policy API reference <https://help.zscaler.com/zpa/access-policy-use-cases>`_
        for further detail on optional keyword parameter structures.

        Args:
            name (str):
                The name of the new rule.
            action (str):
                The action for the policy. Accepted values are:

                |  `allow`
                |  `deny`
            **kwargs:
                Optional keyword args.

        Keyword Args:
            conditions (list):
                A list of conditional rule tuples. Tuples must follow the convention: `Object Type`, `LHS value`,
                `RHS value`. If you are adding multiple values for the same object type then you will need
                a new entry for each value.
                E.g.

                .. code-block:: python

                    [('app', 'id', '926196382959075416'),
                    ('app', 'id', '926196382959075417'),
                    ('app_group', 'id', '926196382959075332),
                    ('client_type', 'zpn_client_type_exporter', 'zpn_client_type_zapp'),
                    ('trusted_network', 'b15e4cad-fa6e-8182-9fc3-8125ee6a65e1', True)]
            custom_msg (str):
                A custom message.
            description (str):
                A description for the rule.

        Returns:
            :obj:`dict`: The resource record of the newly created access policy rule.

        """

        # Initialise the payload
        payload = {
            "name": name,
            "action": action.upper(),
            "conditions": self._create_conditions(kwargs.pop("conditions", [])),
        }

        # Get the policy id of the provided policy type for the URL.
        _policy_id = self.list_policies("access").id

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        return self._post(f"policySet/{_policy_id}/rule", json=payload)

    def add_timeout_rule(self, name: str, **kwargs):
        """
        Add a new Timeout Policy rule.

        See the `ZPA Timeout Policy API reference <https://help.zscaler.com/zpa/timeout-policy-use-cases>`_
        for further detail on optional keyword parameter structures.

        Args:
            name (str):
                The name of the new rule.
            **kwargs:
                Optional parameters.

        Keyword Args:
            conditions (list):
                A list of conditional rule tuples. Tuples must follow the convention: `Object Type`, `LHS value`,
                `RHS value`. If you are adding multiple values for the same object type then you will need
                a new entry for each value.
                E.g.

                .. code-block:: python

                    [('app', 'id', '926196382959075416'),
                    ('app', 'id', '926196382959075417'),
                    ('app_group', 'id', '926196382959075332),
                    ('client_type', 'zpn_client_type_exporter', 'zpn_client_type_zapp'),
                    ('trusted_network', 'b15e4cad-fa6e-8182-9fc3-8125ee6a65e1', True)]
            custom_msg (str):
                A custom message.
            description (str):
                A description for the rule.
            re_auth_idle_timeout (int):
                The re-authentication idle timeout value in seconds.
            re_auth_timeout (int):
                The re-authentication timeout value in seconds.

        Returns:
            :obj:`dict`: The resource record of the newly created Timeout Policy rule.

        """

        # Initialise the payload
        payload = {
            "name": name,
            "action": "RE_AUTH",
            "conditions": self._create_conditions(kwargs.pop("conditions", [])),
        }

        # Get the policy id of the provided policy type for the URL.
        _policy_id = self.list_policies("timeout").id

        # Use specified timeouts or default to UI values
        payload["reauthTimeout"] = kwargs.get("re_auth_timeout", 172800)
        payload["reauthIdleTimeout"] = kwargs.get("re_auth_idle_timeout", 600)

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        return self._post(f"policySet/{_policy_id}/rule", json=payload)

    def add_client_forwarding_rule(self, name: str, action: str, **kwargs):
        """
        Add a new Client Forwarding Policy rule.

        See the
        `ZPA Client Forwarding Policy API reference <https://help.zscaler.com/zpa/client-forwarding-policy-use-cases>`_
        for further detail on optional keyword parameter structures.

        Args:
            name (str):
                The name of the new rule.
            action (str):
                The action for the policy. Accepted values are:

                |  `intercept`
                |  `intercept_accessible`
                |  `bypass`
            **kwargs:
                Optional keyword args.

        Keyword Args:
            conditions (list):
                A list of conditional rule tuples. Tuples must follow the convention: `Object Type`, `LHS value`,
                `RHS value`. If you are adding multiple values for the same object type then you will need
                a new entry for each value.
                E.g.

                .. code-block:: python

                    [('app', 'id', '926196382959075416'),
                    ('app', 'id', '926196382959075417'),
                    ('app_group', 'id', '926196382959075332),
                    ('client_type', 'zpn_client_type_exporter', 'zpn_client_type_zapp'),
                    ('trusted_network', 'b15e4cad-fa6e-8182-9fc3-8125ee6a65e1', True)]
            custom_msg (str):
                A custom message.
            description (str):
                A description for the rule.

        Returns:
            :obj:`dict`: The resource record of the newly created Client Forwarding Policy rule.

        """

        # Initialise the payload
        payload = {
            "name": name,
            "action": action.upper(),
            "conditions": self._create_conditions(kwargs.pop("conditions", [])),
        }

        # Get the policy id of the provided policy type for the URL.
        _policy_id = self.list_policies("client_forwarding").id

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        return self._post(f"policySet/{_policy_id}/rule", json=payload)

    def update_rule(self, policy_type: str, rule_id: str, **kwargs):
        """
        Update an existing policy rule

        Args:
            policy_type (str):
                The policy type. Accepted values are:

                 |  `access`
                 |  `timeout`
                 |  `client_forwarding`
            rule_id (str):
                The unique identifier for the rule to be updated.
            **kwargs:
                Optional keyword args.

        Keyword Args:
            conditions (list):
                A list of conditional rule tuples. Tuples must follow the convention: `Object Type`, `LHS value`,
                `RHS value`. If you are adding multiple values for the same object type then you will need
                a new entry for each value.
                E.g.

                .. code-block:: python

                    [('app', 'id', '926196382959075416'),
                    ('app', 'id', '926196382959075417'),
                    ('app_group', 'id', '926196382959075332),
                    ('client_type', 'zpn_client_type_exporter', 'zpn_client_type_zapp'),
                    ('trusted_network', 'b15e4cad-fa6e-8182-9fc3-8125ee6a65e1', True)]
            custom_msg (str):
                A custom message.
            description (str):
                A description for the rule.

        Returns:
            :obj:`str`: The response code for the operation.

        Examples:
            Updates the name only for an Access Policy rule:

            >>> zpa.policies.update_rule('access', '72057615512764594', name='new_rule_name')

            Updates the action only for a Client Forwarding Policy rule:

            >>> zpa.policies.update_rule('client_forwarding', '72057615512764595', action='BYPASS')

        """

        current_rule = self.get_rule(policy_type, rule_id)
        payload = {snake_to_camel(k): v for k, v in current_rule.items()}

        # Add optional parameters to payload
        for key, value in kwargs.items():
            if key == "conditions":
                payload["conditions"] = self._create_conditions(value)
            else:
                payload[snake_to_camel(key)] = value

        return self._put(
            f"policySet/{current_rule.policySetId}/rule/{rule_id}",
            json=payload,
            box=False,
        ).status_code
