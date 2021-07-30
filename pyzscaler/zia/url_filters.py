from restfly.endpoint import APIEndpoint
from box import BoxList
from pyzscaler.utils import snake_to_camel


class URLFilteringAPI(APIEndpoint):
    # URL Filtering Policy rule keys that only require an ID to be provided.
    _key_id_list = [
        "departments",
        "groups",
        "locations",
        "location_groups",
        "override_users",
        "override_groups",
        "time_windows",
        "users",
    ]

    def list_rules(self):
        """
        Returns the list of URL Filtering Policy rules

        Returns:
            :obj:`list` of :obj:`dict`

        Examples:
            >>> for rule in zia.url_filters.list_rules():
            ...    pprint(rule)

        """
        return self._get("urlFilteringRules", box=BoxList)

    def get_rule(self, rule_id: str):
        """
        Returns information on the specified URL Filtering Policy rule.

        Args:
            rule_id (str): The unique ID for the URL Filtering Policy rule.

        Returns:
            :obj:`dict`: The URL Filtering Policy rule.

        Examples:
            >>> pprint(zia.url_filters.get_rule('977469'))

        """

        return self._get(f"urlFilteringRules/{rule_id}")

    def delete_rule(self, rule_id: str):
        """
        Deletes the specified URL Filtering Policy rule.

        Args:
            rule_id (str): The unique ID for the URL Filtering Policy rule.

        Returns:
            :obj:`str`: The status code for the operation.

        Examples:
            >>> zia.url_filters.delete_rule('977463')

        """
        return self._delete(f"urlFilteringRules/{rule_id}", box=False).status_code

    def add_rule(self, rank: str, name: str, action: str, protocols: list, **kwargs):
        """
        Adds a new URL Filtering Policy rule.

        Args:
            rank (str): The admin rank of the user who creates the rule.
            name (str): The name of the rule.
            action (str): Action taken when traffic matches rule criteria. Accepted values are:

                `ANY`, `NONE`, `BLOCK`, `CAUTION`, `ALLOW` and `ICAP_RESPONSE`

            protocols (list): The protocol criteria for the rule.
            **kwargs: Optional keyword args.

        Keyword Args:
            block_override (bool): When set to true, a 'BLOCK' action triggered by the rule could be overridden.
                Defaults to `False`.
            ciparule (bool): The CIPA compliance rule is enabled if this is set to `True`. Defaults to `False`.
            departments (list): The IDs for the departments that this rule applies to.
            description (str): Additional information about the URL Filtering rule.
            end_user_notification_url (str): URL of end user notification page to be displayed when the rule is matched.
                Not applicable if either ``override_users`` or ``override_groups`` is specified.
            enforce_time_validity (bool): Enforce a set validity time period for the URL Filtering rule.
            groups (list): The IDs for the groups that this rule applies to.
            locations (list): The IDs for the locations that this rule applies to.
            location_groups (list): The IDs for the location groups that this rule applies to.
            order (str): Order of execution of rule with respect to other URL Filtering rules. Defaults to placing rule
                at the bottom of the list.
            override_users (list): The IDs of users that this rule can be overridden for.
                Only applies if ``block_override`` is True, ``action`` is `BLOCK` and ``override_groups`` is not set.
            override_group (list): The IDs of groups that this rule can be overridden for.
                Only applies if ``block_override`` is True and ``action`` is `BLOCK`.
            request_methods (list): The request methods that this rule will apply to. If not specified, the rule will
                apply to all methods.
            size_quota (str): Size quota in KB for applying the URL Filtering rule.
            time_quota (str): Time quota in minutes elapsed after the URL Filtering rule is applied.
            time_windows (list): The IDs for the time windows that this rule applies to.
            url_categories (list): The names of URL categories that this rule applies to.
            users (list): The IDs for the users that this rule applies to.
            validity_start_time (str): Date and time the rule's effects will be valid from. ``enforce_time_validity``
                must be set to `True` for this to take effect.
            validity_end_time (str): Date and time the rule's effects will end. ``enforce_time_validity`` must be set to
                `True` for this to take effect.
            validity_time_zone_id (str): The URL Filter rule validity date and time will be based on the TZ provided.
                ``enforce_time_validity`` must be set to `True` for this to take effect.

        Returns:
            :obj:`dict`: The newly created URL Filtering Policy rule.

        Examples:
            Add a rule with the minimum required parameters:

            >>> zia.url_filters.add_rule(rank='7',
            ...    name="Empty URL Filter",
            ...    action="ALLOW",
            ...    protocols=['ANY_RULE']

            Add a rule to block HTTP POST to Social Media sites for the Finance department.

            >>> zia.url_filters.add_rule(rank='7',
            ...    name="Block POST to Social Media",
            ...    action="BLOCK",
            ...    protocols=["HTTP_PROXY", "HTTP_RULE", "HTTPS_RULE"],
            ...    request_methods=['POST'],
            ...    departments=["95022175"],
            ...    url_categories=["SOCIAL_NETWORKING"])

        """

        payload = {
            "rank": rank,
            "name": name,
            'action': action,
            'protocols': protocols,
            "order": kwargs.pop("order", len(self.list_rules()))
        }

        # Add optional parameters to payload
        for key, value in kwargs.items():
            if key in self._key_id_list:
                payload[snake_to_camel(key)] = []
                for item in value:
                    payload[snake_to_camel(key)].append({"id": item})
            else:
                payload[snake_to_camel(key)] = value

        return self._post("urlFilteringRules", json=payload)

    def update_rule(self, rule_id: str, **kwargs):
        """
        Updates the specified URL Filtering Policy rule.

        Args:
            rule_id: The unique ID of the URL Filtering Policy rule to be updated.
            **kwargs: Optional keyword args.

        Keyword Args:
            name (str): The name of the rule.
            action (str): Action taken when traffic matches rule criteria. Accepted values are:

                `ANY`, `NONE`, `BLOCK`, `CAUTION`, `ALLOW` and `ICAP_RESPONSE`

            protocols (list): The protocol criteria for the rule.
            block_override (bool): When set to true, a 'BLOCK' action triggered by the rule could be overridden.
                Defaults to `False`.
            ciparule (bool): The CIPA compliance rule is enabled if this is set to `True`. Defaults to `False`.
            departments (list): The IDs for the departments that this rule applies to.
            description (str): Additional information about the URL Filtering rule.
            end_user_notification_url (str): URL of end user notification page to be displayed when the rule is matched.
                Not applicable if either ``override_users`` or ``override_groups`` is specified.
            enforce_time_validity (bool): Enforce a set validity time period for the URL Filtering rule.
            groups (list): The IDs for the groups that this rule applies to.
            locations (list): The IDs for the locations that this rule applies to.
            location_groups (list): The IDs for the location groups that this rule applies to.
            order (str): Order of execution of rule with respect to other URL Filtering rules. Defaults to placing rule
                at the bottom of the list.
            override_users (list): The IDs of users that this rule can be overridden for.
                Only applies if ``block_override`` is True, ``action`` is `BLOCK` and ``override_groups`` is not set.
            override_group (list): The IDs of groups that this rule can be overridden for.
                Only applies if ``block_override`` is True and ``action`` is `BLOCK`.
            request_methods (list): The request methods that this rule will apply to. If not specified, the rule will
                apply to all methods.
            size_quota (str): Size quota in KB for applying the URL Filtering rule.
            time_quota (str): Time quota in minutes elapsed after the URL Filtering rule is applied.
            time_windows (list): The IDs for the time windows that this rule applies to.
            url_categories (list): The names of URL categories that this rule applies to.
            users (list): The IDs for the users that this rule applies to.
            validity_start_time (str): Date and time the rule's effects will be valid from. ``enforce_time_validity``
                must be set to `True` for this to take effect.
            validity_end_time (str): Date and time the rule's effects will end. ``enforce_time_validity`` must be set to
                `True` for this to take effect.
            validity_time_zone_id (str): The URL Filter rule validity date and time will be based on the TZ provided.
                ``enforce_time_validity`` must be set to `True` for this to take effect.

        Returns:
            :obj:`dict`: The updated URL Filtering Policy rule.

        Examples:
            Update the name of a URL Filtering Policy rule:

            >>> zia.url_filters.update_rule('977467',
            ...    name="Updated Name")

            Add GET to request methods and change action to ALLOW:

            >>> zia.url_filters.update_rule('977468',
            ...    request_methods=['POST', 'GET'],
            ...    action="ALLOW")

        """

        # Set payload to value of existing record
        payload = {snake_to_camel(k): v for k, v in self.get_rule(rule_id).items()}

        # Add optional parameters to payload
        for key, value in kwargs.items():
            if key in self._key_id_list:
                payload[snake_to_camel(key)] = []
                for item in value:
                    payload[snake_to_camel(key)].append({"id": item})
            else:
                payload[snake_to_camel(key)] = value

        return self._put(f"urlFilteringRules/{rule_id}", json=payload)
