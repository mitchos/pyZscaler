import json

from box import Box, BoxList
from restfly.endpoint import APIEndpoint


class WebDLP(APIEndpoint):
    def get_all_rules(self, **kwargs) -> BoxList:
        """
        Gets a list of DLP policy rules, excluding SaaS Security API DLP policy rules.

        Returns:
            BoxList of Web DLP items.

        Examples:
            # Get all Web DLP Items
            results = zia.web_dlp.get_all_rules()
            for item in results:
                logging.info(item)

        """
        return self._get("webDlpRules")

    def get_rule(self, rule_id: str) -> Box:
        """
        Gets a DLP policy rule, excluding SaaS Security API DLP policy rules.

        Args:
            rule_id: String of ID.

        Returns:
            Box of Web DLP item.

        Examples:
            # Get Web DLP item by ID
            results = zia.web_dlp.get_rule(rule_id='2671')
            logging.info(results)

        """
        return self._get(f"webDlpRules/{rule_id}")

    def get_rules_lite(self) -> BoxList:
        """
        Gets name and ID dictionary for all DLP policy rules, excluding SaaS Security API DLP policy rules.

        Returns:
            BoxList of Web DLP name/ids.

        Examples:
            # Get Web DLP Lite results
            results = zia.web_dlp.get_rules_lite()
            for item in results:
                logging.info(item)

        """
        return self._get("webDlpRules/lite")

    def add_rule(self, payload: json) -> Box:
        """Adds a new DLP policy rule.

        Args:
            payload: JSON of Web DLP Policy to POST.

        Returns:
            Box item of resulting POST.

        Minimum items required in payload:
            payload = {
                'order': 1, # A number greater than 0.
                'rank': 0,
                'name': "Dax testing pyZscaler post.",
                'protocols': ["ANY_RULE"],
                'action': "ALLOW",
            }

        Examples:
            # Build minimum info for POST
            payload = {
                'order': 1,
                'rank': 0,
                'name': "Dax testing pyZscaler post.",
                'protocols': ["ANY_RULE"],
                'action': "ALLOW",
            }

            # Post new Web DLP item
            results = zia.web_dlp.add_rule(payload=payload)
            logging.info(results)
            post_id = results['id']
            logging.info(f"Posted payload result has id: {post_id}.")

        """
        return self._post("webDlpRules", json=payload)

    def update_rule(self, rule_id: str, payload: json) -> Box:
        """
        Updates a DLP policy rule. This endpoint is not applicable to SaaS Security API DLP policy rules.

        Args:
            rule_id: String of ID.
            payload: JSON of Web DLP Policy to PUT.

        Returns:
            Box item of resulting PUT.

        Examples:
            # Update Web DLP item.
            payload['name'] = "daxm updated name."
            results = zia.web_dlp.update_rule(rule_id=post_id, payload=payload)
            logging.info(results)

        """
        return self._put(f"webDlpRules/{rule_id}", json=payload)

    def delete_rule(self, rule_id: str) -> int:
        """
        Deletes a DLP policy rule. This endpoint is not applicable to SaaS Security API DLP policy rules.

        Args:
            rule_id: String of ID.

        Returns:
            Requests.Response object.

        Examples:
            # Delete Web DLP item.
            results = zia.web_dlp.delete_rule(rule_id=post_id)
            logging.info(results)

        """
        return self._delete(f"webDlpRules/{rule_id}").status_code
