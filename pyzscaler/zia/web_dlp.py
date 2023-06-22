import json

from box import Box, BoxList
from restfly.endpoint import APIEndpoint


class WebDLPAPI(APIEndpoint):
    def list_rules(self, **kwargs) -> BoxList:
        """
        Returns a list of DLP policy rules, excluding SaaS Security API DLP policy rules.

        Returns:
            :obj:`BoxList`: List of Web DLP items.

        Examples:
            Get a list of all Web DLP Items

            >>> results = zia.web_dlp.list_rules()
            ... for item in results:
            ...    print(item)

        """
        return self._get("webDlpRules")

    def get_rule(self, rule_id: str) -> Box:
        """
        Returns a DLP policy rule, excluding SaaS Security API DLP policy rules.

        Args:
            rule_id (str): The unique id for the Web DLP rule.

        Returns:
            :obj:`Box`: The Web DLP Rule resource record.

        Examples:
            Get information on a Web DLP item by ID

            >>> results = zia.web_dlp.get_rule(rule_id='9999')
            ... print(results)

        """
        return self._get(f"webDlpRules/{rule_id}")

    def list_rules_lite(self) -> BoxList:
        """
        Returns the name and ID for all DLP policy rules, excluding SaaS Security API DLP policy rules.

        Returns:
            :obj:`BoxList`: List of Web DLP name/ids.

        Examples:
            Get Web DLP Lite results

            >>> results = zia.web_dlp.list_rules_lite()
            ... for item in results:
            ...    print(item)

        """
        return self._get("webDlpRules/lite")

    def add_rule(self, payload: json) -> Box:
        """
        Adds a new DLP policy rule.

        Args:
            payload (dict): Dictionary containing the Web DLP Policy rule to be added.

        Returns:
            :obj:`Box`: The newly added Web DLP Policy Rule resource record.

        Payload:
            Minimum items required in payload::

                payload = {
                    'order': 1, # A number greater than 0.
                    'rank': 0,
                    'name': "Dax testing pyZscaler post.",
                    'protocols': ["ANY_RULE"],
                    'action': "ALLOW",
                }

        Examples:
            Add a Web DLP Policy rule with the minimum required parameters::

                payload = {
                    'order': 1,
                    'rank': 0,
                    'name': "Dax testing pyZscaler post.",
                    'protocols': ["ANY_RULE"],
                    'action': "ALLOW",
                }

                 # Add new Web DLP item
                 print(zia.web_dlp.add_rule(payload=payload))

        """
        return self._post("webDlpRules", json=payload)

    def update_rule(self, rule_id: str, payload: dict) -> Box:
        """
        Updates a DLP policy rule. This endpoint is not applicable to SaaS Security API DLP policy rules.

        Args:
            rule_id (str): String of ID.
            payload (dict): Dictionary containing the updated Web DLP Policy Rule.

        Returns:
            :obj:`Box`: The updated Web DLP Policy Rule resource record.

        Examples:
            Update a Web DLP Policy Rule::

                 payload = zia.web_dlp.get_rule('9999')
                 payload['name'] = "daxm updated name."
                 results = zia.web_dlp.update_rule(rule_id=9999, payload=payload)
                 print(results)

        """
        return self._put(f"webDlpRules/{rule_id}", json=payload)

    def delete_rule(self, rule_id: str) -> Box:
        """
        Deletes a DLP policy rule. This endpoint is not applicable to SaaS Security API DLP policy rules.

        Args:
            rule_id (str): Unique id of the Web DLP Policy Rule that will be deleted.

        Returns:
            :obj:`Box`: Response message from the ZIA API endpoint.

        Examples:
            Delete a rule with an id of 9999.

            >>> results = zia.web_dlp.delete_rule(rule_id=9999)
            ... print(results)


        """
        return self._delete(f"webDlpRules/{rule_id}")
