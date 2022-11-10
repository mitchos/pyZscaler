import json

import requests
from box import Box, BoxList
from restfly.endpoint import APIEndpoint


class WebDLP(APIEndpoint):
    def get_all(self, **kwargs) -> BoxList:
        """
        Gets a list of DLP policy rules, excluding SaaS Security API DLP policy rules.

        Returns:
            BoxList of Web DLP items.
        """
        return self._get("webDlpRules")

    def get_item(self, item_id: str) -> Box:
        """
        Gets a DLP policy rule, excluding SaaS Security API DLP policy rules.

        Args:
            item_id: String of ID.

        Returns:
            Box of Web DLP item.
        """
        return self._get(f"webDlpRules/{item_id}")

    def lite(self) -> BoxList:
        """
        Gets name and ID dictionary for all DLP policy rules, excluding SaaS Security API DLP policy rules.

        Returns:
            BoxList of Web DLP name/ids.
        """
        return self._get("webDlpRules/lite")

    def post(self, payload: json) -> Box:
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
        """
        return self._post("webDlpRules", json=payload)

    def put(self, item_id: str, payload: json) -> Box:
        """
        Updates a DLP policy rule. This endpoint is not applicable to SaaS Security API DLP policy rules.

        Args:
            item_id: String of ID.
            payload: JSON of Web DLP Policy to PUT.

        Returns:
            Box item of resulting PUT.
        """
        return self._put(f"webDlpRules/{item_id}", json=payload)

    def delete(self, item_id: str) -> requests.Response:
        """
        Deletes a DLP policy rule. This endpoint is not applicable to SaaS Security API DLP policy rules.

        Args:
            item_id: String of ID.

        Returns:
                Requests.Response object.
        """
        return self._delete(f"webDlpRules/{item_id}")
