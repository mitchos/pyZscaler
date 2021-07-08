from restfly.endpoint import APIEndpoint


class PolicySetsAPI(APIEndpoint):

    def list_client_forward(self):
        """Returns a list of all configured Client Forwarding policies.

        Returns:
            :obj:`dict`: Resource record of configured Client Forwarding policies.

        Examples:
            >>> for client_forward_policy in zpa.policies.list_client_forward():
            ...    pprint(client_forward_policy)

        """
        return self._get('policySet/bypass')

    def list_timeout(self):
        """Returns a list of all configured Timeout policies.

        Returns:
            :obj:`dict`: A resource record of all configured timeout policies.

        Examples:
            >>> for timeout_policy in zpa.policies.list_timeout():
            ...    pprint(timeout_policy)

        """

        return self._get('policySet/reauth')

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

    def list_access(self):
        """Returns all configured access policies.

        'Access Policy' in the ZPA UI is referred to as 'Global Policy' in the API documentation.

        Returns:
            :obj:`dict`: The resource record for the Access policy.

        Examples:
            >>> global_policy = zpa.policies.get_global()

        """

        return self._get('policySet/global')

    def list_type(self, policy_type: str):
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

    def delete_rule(self, policy_id: str, rule_id: str):
        """Deletes the specified policy rule.

        Args:
            policy_id (str):
                The unique identifier for the policy.
            rule_id (str):
                The unique identifier for the policy rule.

        Returns:
            :obj:`str`: The response code for the operation.

        Examples:
            >>> zpa.policies.delete_rule(policy_id='2342567567355535',
            ...    rule_id='23322646655778')

        """
        return self._delete(f'policySet/{policy_id}/rule/{rule_id}')

    def add_rule(self, policy_type: str, name: str, action: str = None, **kwargs):
        """Add a new policy rule.

        See the `ZPA API reference <https://help.zscaler.com/zpa/api-reference#/policy-set-controller/addRuleToPolicySet>`_
        for further detail on optional keyword parameter structures.

        Args:
            policy_type (str):
                The policy type for the new rule. Accepted values are 'access', 'timeout' and 'client_forward'.
            name (str):
                The name of the new rule.
            action (str, optional):
                The action for the policy. Accepted values are:
                 Access Policy: 'ALLOW' (default) or 'DENY'.
                 Timeout Policy: 'RE_AUTH' (default)
                 Client Forwarding Policy: 'INTERCEPT' (default), 'INTERCEPT_ACCESSIBLE' and 'BYPASS'.
            **kwargs:
                Optional parameters.

        Keyword Args:
            appServerGroups (list):
                List of application server groups.
            appConnectorGroups (list):
                List of application connector groups.
            conditions (list:
                List of conditions.
            customMsg (str):
                A custom message.
            description (str):
                A description for the rule.
            operator (str):
                The operator for a rule. Accepted values are 'AND' or 'OR'.
            priority (int):
                The rule priority.
            re_auth_idle_timeout (int):
                The re-authentication idle timeout value in seconds.
            re_auth_timeout (int):
                The re-authentication timeout value in seconds.
            ruleOrder (int):
                The rule order.
            zpnCbiProfileId (str):
                The CBI profile ID.

        Returns:
            :obj:`dict`: The resource record of the newly created policy rule.

        """

        # Initialise the payload
        payload = {
            'name': name,
        }

        # Get the policy id for the provided policy type and configure payload accordingly.
        if policy_type == 'access':
            _policy_id = self.list_access().id
            payload['action'] = kwargs.get('action', 'ALLOW')
        elif policy_type == 'timeout':
            _policy_id = self.list_timeout().id
            payload['action'] = 'RE_AUTH'
            payload['reauthTimeout'] = kwargs.get('re_auth_timeout', 172800)  # Default value in ZPA UI
            payload['reauthIdleTimeout'] = kwargs.get('re_auth_idle_timeout', 600)  # Default value in ZPA UI
        elif policy_type == 'client_forward':
            _policy_id = self.list_client_forward().id
            payload['action'] = kwargs.get('action', 'INTERCEPT')
        else:
            _policy_id = None

        return self._post(f'policySet/{_policy_id}/rule', json=payload)
