from box import Box, BoxList
from restfly.endpoint import APIEndpoint

from pyzscaler.utils import Iterator, convert_keys, snake_to_camel


class PolicySetsAPI(APIEndpoint):
    POLICY_MAP = {
        "access": "ACCESS_POLICY",
        "timeout": "TIMEOUT_POLICY",
        "client_forwarding": "CLIENT_FORWARDING_POLICY",
        "siem": "SIEM_POLICY",
    }

    @staticmethod
    def _create_conditions(conditions: list):
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

    def get_policy(self, policy_type: str) -> Box:
        """
        Returns the policy and rule sets for the given policy type.

        Args:
            policy_type (str): The type of policy to be returned. Accepted values are:

                 |  ``access`` - returns the Access Policy
                 |  ``timeout`` - returns the Timeout Policy
                 |  ``client_forwarding`` - returns the Client Forwarding Policy
                 |  ``siem`` - returns the SIEM Policy

        Returns:
            :obj:`Box`: The resource record of the specified policy type.

        Examples:
            Request the specified Policy.

            >>> pprint(zpa.policies.get_policy('access'))

        """
        # Map the simplified policy_type name to the name expected by the Zscaler API
        mapped_policy_type = self.POLICY_MAP.get(policy_type, None)

        # If the user provided an incorrect name, raise an error
        if not mapped_policy_type:
            raise ValueError(
                f"Incorrect policy type provided: {policy_type}\n "
                f"Policy type must be 'access', 'timeout', 'client_forwarding' or 'siem'."
            )

        return self._get(f"policySet/policyType/{mapped_policy_type}")

    def get_rule(self, policy_type: str, rule_id: str) -> Box:
        """
        Returns the specified policy rule.

        Args:
            policy_type (str): The type of policy to be returned. Accepted values are:

                 |  ``access``
                 |  ``timeout``
                 |  ``client_forwarding``
                 |  ``siem``
            rule_id (str): The unique identifier for the policy rule.

        Returns:
            :obj:`Box`: The resource record for the requested rule.

        Examples:
            >>> policy_rule = zpa.policies.get_rule(policy_id='99999',
            ...    rule_id='88888')

        """
        # Get the policy id for the supplied policy_type
        policy_id = self.get_policy(policy_type).id

        return self._get(f"policySet/{policy_id}/rule/{rule_id}")

    def list_rules(self, policy_type: str, **kwargs) -> BoxList:
        """
        Returns policy rules for a given policy type.

        Args:
            policy_type (str):
                The policy type. Accepted values are:

                |  ``access`` - returns Access Policy rules
                |  ``timeout`` - returns Timeout Policy rules
                |  ``client_forwarding`` - returns Client Forwarding Policy rules

        Returns:
            :obj:`list`: A list of all policy rules that match the requested type.

        Examples:
            >>> for policy in zpa.policies.list_type('type')
            ...    pprint(policy)

        """

        # Map the simplified policy_type name to the name expected by the Zscaler API
        mapped_policy_type = self.POLICY_MAP.get(policy_type, None)

        # If the user provided an incorrect name, raise an error
        if not mapped_policy_type:
            raise ValueError(
                f"Incorrect policy type provided: {policy_type}\n "
                f"Policy type must be 'access', 'timeout', 'client_forwarding' or 'siem'."
            )

        return BoxList(Iterator(self._api, f"policySet/rules/policyType/{mapped_policy_type}", **kwargs))

    def delete_rule(self, policy_type: str, rule_id: str) -> int:
        """
        Deletes the specified policy rule.

        Args:
            policy_type (str):
                The type of policy the rule belongs to. Accepted values are:

                 |  ``access``
                 |  ``timeout``
                 |  ``client_forwarding``
                 |  ``siem``
            rule_id (str):
                The unique identifier for the policy rule.

        Returns:
            :obj:`int`: The response code for the operation.

        Examples:
            >>> zpa.policies.delete_rule(policy_id='99999',
            ...    rule_id='88888')

        """

        # Get policy id for specified policy type
        policy_id = self.get_policy(policy_type).id

        return self._delete(f"policySet/{policy_id}/rule/{rule_id}").status_code

    def add_access_rule(self, name: str, action: str, **kwargs) -> Box:
        """
        Add a new Access Policy rule.

        See the `ZPA Access Policy API reference <https://help.zscaler.com/zpa/access-policy-use-cases>`_
        for further detail on optional keyword parameter structures.

        Args:
            name (str):
                The name of the new rule.
            action (str):
                The action for the policy. Accepted values are:

                |  ``allow``
                |  ``deny``
            **kwargs:
                Optional keyword args.

        Keyword Args:
            conditions (list):
                A list of conditional rule tuples. Tuples must follow the convention: `Object Type`, `LHS value`,
                `RHS value`. If you are adding multiple values for the same object type then you will need
                a new entry for each value.
                E.g.

                .. code-block:: python

                    [('app', 'id', '99999'),
                    ('app', 'id', '88888'),
                    ('app_group', 'id', '77777),
                    ('client_type', 'zpn_client_type_exporter', 'zpn_client_type_zapp'),
                    ('trusted_network', 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxx', True)]
            custom_msg (str):
                A custom message.
            description (str):
                A description for the rule.

        Returns:
            :obj:`Box`: The resource record of the newly created access policy rule.

        """

        # Initialise the payload
        payload = {
            "name": name,
            "action": action.upper(),
            "conditions": self._create_conditions(kwargs.pop("conditions", [])),
        }

        # Get the policy id of the provided policy type for the URL.
        policy_id = self.get_policy("access").id

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        return self._post(f"policySet/{policy_id}/rule", json=payload)

    def add_timeout_rule(self, name: str, **kwargs) -> Box:
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
            :obj:`Box`: The resource record of the newly created Timeout Policy rule.

        """

        # Initialise the payload
        payload = {
            "name": name,
            "action": "RE_AUTH",
            "conditions": self._create_conditions(kwargs.pop("conditions", [])),
        }

        # Get the policy id of the provided policy type for the URL.
        _policy_id = self.get_policy("timeout").id

        # Use specified timeouts or default to UI values
        payload["reauthTimeout"] = kwargs.get("re_auth_timeout", 172800)
        payload["reauthIdleTimeout"] = kwargs.get("re_auth_idle_timeout", 600)

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        return self._post(f"policySet/{_policy_id}/rule", json=payload)

    def add_client_forwarding_rule(self, name: str, action: str, **kwargs) -> Box:
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

                |  ``intercept``
                |  ``intercept_accessible``
                |  ``bypass``
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
            :obj:`Box`: The resource record of the newly created Client Forwarding Policy rule.

        """

        # Initialise the payload
        payload = {
            "name": name,
            "action": action.upper(),
            "conditions": self._create_conditions(kwargs.pop("conditions", [])),
        }

        # Get the policy id of the provided policy type for the URL.
        policy_id = self.get_policy("client_forwarding").id

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        return self._post(f"policySet/{policy_id}/rule", json=payload)

    def update_rule(self, policy_type: str, rule_id: str, **kwargs) -> Box:
        """
        Update an existing policy rule

        Args:
            policy_type (str):
                The policy type. Accepted values are:

                 |  ``access``
                 |  ``timeout``
                 |  ``client_forwarding``
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
            :obj:`Box`: The updated policy-rule resource record.

        Examples:
            Updates the name only for an Access Policy rule:

            >>> zpa.policies.update_rule('access', '99999', name='new_rule_name')

            Updates the action only for a Client Forwarding Policy rule:

            >>> zpa.policies.update_rule('client_forwarding', '888888', action='BYPASS')

        """
        # Get policy id for specified policy type
        policy_id = self.get_policy(policy_type).id

        payload = convert_keys(self.get_rule(policy_type, rule_id))

        # Add optional parameters to payload
        for key, value in kwargs.items():
            if key == "conditions":
                payload["conditions"] = self._create_conditions(value)
            else:
                payload[snake_to_camel(key)] = value

        resp = self._put(f"policySet/{policy_id}/rule/{rule_id}", json=payload, box=False).status_code

        if resp == 204:
            return self.get_rule(policy_type, rule_id)
