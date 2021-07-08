from restfly.endpoint import APIEndpoint


class PolicySetsAPI(APIEndpoint):

    def list_bypass(self):
        """Returns a list of all configured bypass policies.

        Returns:
            :obj:`dict`: Resource record of configured bypass policies.

        Examples:
            >>> for bypass_policy in zpa.policies.list_bypass():
            ...    pprint(bypass_policy)

        """
        return self._get('policySet/bypass')

    def list_auth(self):
        """Returns a list of all configured authentication policies.

        Returns:
            :obj:`dict`: A resource record of all configured authentication policies.

        Examples:
            >>> for auth_policy in zpa.policies.list_auth():
            ...    pprint(auth_policy)

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

    def get_global(self):
        """Returns the global policy.

        Returns:
            :obj:`dict`: The resource record for the global policy.

        Examples:
            >>> global_policy = zpa.policies.get_global()

        """

        return self._get('policySet/global')

    def list_type(self, policy_type: str):
        """Returns policy rules for a given policy type.

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
