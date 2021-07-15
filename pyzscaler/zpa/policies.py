from restfly.endpoint import APIEndpoint


class PolicySetsAPI(APIEndpoint):

    def list_policies(self, policy_type: str = None):
        """Returns the policy and rule sets for the given policy type.

        Args:
            policy_type (str):
                The type of policy to be returned. Accepted values are 'access', 'timeout' and 'client_forwarding'.

        Returns:
            :obj:`dict`: Resource record of the specified policy.

        Examples:
            Request the specified Policy.

            >>> pprint(zpa.policies.list_policies('access'))

        """
        _policy_url = None

        if policy_type == 'access':
            _policy_url = 'global'
        elif policy_type == 'timeout':
            _policy_url = 'reauth'
        elif policy_type == 'client_forwarding':
            _policy_url = 'bypass'

        return self._get(f'policySet/{_policy_url}')

    def get_rule(self, policy_id: str, rule_id: str):
        """Returns the specified policy rule.

        Args:
            policy_id (str):
                The unique identifier for the policy.
            rule_id (str):
                The unique identifier for the policy rule.

        Returns:
            :obj:`dict`: The resource record for the requested rule.

        Examples:
            >>> policy_rule = zpa.policies.get_rule(policy_id='234234234344',
            ...    rule_id='23456546546456')

        """

        return self._get(f'policySet/{policy_id}/rule/{rule_id}')

    def list_rules(self, policy_type: str):
        """Returns policy rules for a given policy type.

        Args:
            policy_type (str):
                The policy type. Accepted values are:
                GLOBAL_POLICY - returns Access Policies
                REAUTH_POLICY - returns Timeout Policies
                BYPASS_POLICY - returns Client Forwarding Policies

        Returns:
            :obj:`list`: A list of all policy rules that match the requested type.

        Examples:
            >>> for policy in zpa.policies.list_type('type')
            ...    pprint(policy)

        """

        return self._get(f'policySet/rules/policyType/{policy_type}').list

    def delete_rule(self, policy_type: str, rule_id: str):
        """Deletes the specified policy rule.

        Args:
            policy_type (str):
                The type of policy the rule belongs to. Accepted values are 'access', 'timeout' and 'client_forwarding'.
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

        return self._delete(f'policySet/{_policy_id}/rule/{rule_id}')

    def add_access_rule(self, name: str, action: str = None, **kwargs):
        """Add a new Access Policy rule.

        See the `ZPA Access Policy API reference <https://help.zscaler.com/zpa/access-policy-use-cases>`_
        for further detail on optional keyword parameter structures.

        Args:
            name (str):
                The name of the new rule.
            action (str, optional):
                The action for the policy. Accepted values are:
                'ALLOW' (default) or 'DENY'.
            **kwargs:
                Optional parameters.

        Keyword Args:
            conditions (list:
                List of conditions.
            customMsg (str):
                A custom message.
            description (str):
                A description for the rule.

        Returns:
            :obj:`dict`: The resource record of the newly created access policy rule.

        """

        # Initialise the payload
        payload = {
            'name': name,
        }

        # Get the policy id for the provided policy type and configure payload accordingly.
        _policy_id = self.list_policies('access').id
        payload['action'] = kwargs.get('action', 'ALLOW')

        for key, value in kwargs.items():
            payload[key] = value

        return self._post(f'policySet/{_policy_id}/rule', json=payload)

    def add_timeout_rule(self, name: str, **kwargs):
        """Add a new Timeout Policy rule.

        See the `ZPA Timeout Policy API reference <https://help.zscaler.com/zpa/timeout-policy-use-cases>`_
        for further detail on optional keyword parameter structures.

        Args:
            name (str):
                The name of the new rule.
            **kwargs:
                Optional parameters.

        Keyword Args:
            conditions (list):
                List of conditions.
            customMsg (str):
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
            'name': name,
        }

        # Get the policy id for the provided policy type and configure payload accordingly.
        _policy_id = self.list_policies('timeout').id
        payload['action'] = 'RE_AUTH'
        payload['reauthTimeout'] = kwargs.get('re_auth_timeout', 172800)  # Default value in ZPA UI
        payload['reauthIdleTimeout'] = kwargs.get('re_auth_idle_timeout', 600)  # Default value in ZPA UI

        for key, value in kwargs.items():
            payload[key] = value

        return self._post(f'policySet/{_policy_id}/rule', json=payload)

    def add_client_forwarding_rule(self, name: str, action: str = None, **kwargs):
        """Add a new Client Forwarding Policy rule.

        See the `ZPA Client Forwarding Policy API reference <https://help.zscaler.com/zpa/client-forwarding-policy-use-cases>`_
        for further detail on optional keyword parameter structures.

        Args:
            name (str):
                The name of the new rule.
            action (str, optional):
                The action for the policy. Accepted values are:
                'INTERCEPT' (default), 'INTERCEPT_ACCESSIBLE' and 'BYPASS'.
            **kwargs:
                Optional parameters.

        Keyword Args:
            conditions (list:
                List of conditions.
            customMsg (str):
                A custom message.
            description (str):
                A description for the rule.

        Returns:
            :obj:`dict`: The resource record of the newly created Client Forwarding Policy rule.

        """

        # Initialise the payload
        payload = {
            'name': name,
        }

        # Get the policy id for the provided policy type and configure payload accordingly.
        _policy_id = self.list_policies('client_forwarding').id
        payload['action'] = kwargs.get('action', 'INTERCEPT')

        for key, value in kwargs.items():
            payload[key] = value

        return self._post(f'policySet/{_policy_id}/rule', json=payload)

    def update_rule(self, policy_type: str, rule_id: str = None, name: str = None, action: str = None, **kwargs):
        """Update an existing policy rule

        Passing only the policy_type and rule_id will result in a successful operation with no changes to the rule
        record. All other supplied params will result in a change.

        Args:
            policy_type:
                The policy type. Accepted values are 'access', 'timeout' and 'client_forwarding'
            rule_id:
                The unique identifier for the rule to be updated.
            name:
                The name of the rule. Defaults to existing name if omitted.
            action:
                The action of the rule. Defaults to existing action if omitted.
            **kwargs:

        Returns:
            :obj:`str`: The response code for the operation.

        Examples:

            Updates the name only for an Access Policy rule:

            >>> zpa.policies.update_rule('access', '72057615512764594', name='new_rule_name')

            Updates the action only for a Client Forwarding Policy rule:

            >>> zpa.policies.update_rule('client_forwarding', '72057615512764595', action='BYPASS')

        """

        # Get the policy id for the supplied policy_type
        _policy_id = self.list_policies(policy_type).id

        # Name required so use existing name from rule if not specified
        if not name:
            name = self.get_rule(_policy_id, rule_id).name

        # Action required so use existing action from rule if not specified
        if not action:
            action = self.get_rule(_policy_id, rule_id).action

        # Initialise payload
        payload = {
            'name': name,
            'action': action
        }

        # Add optional params to payload
        for key, value in kwargs.items():
            payload[key] = value

        return self._put(f'policySet/{_policy_id}/rule/{rule_id}', json=payload, box=False).status_code
