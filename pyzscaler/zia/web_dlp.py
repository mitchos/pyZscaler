from restfly.endpoint import APIEndpoint


class WebDLP(APIEndpoint):
    def get_all(self, **kwargs):
        """Gets a list of DLP policy rules, excluding SaaS Security API DLP policy rules."""
        return self._get("webDlpRules")

    def get_item(self, item_id):
        """Gets a DLP policy rule, excluding SaaS Security API DLP policy rules."""
        return self._get(f"webDlpRules/{item_id}")

    def lite(self):
        """Gets name and ID dictionary for all DLP policy rules, excluding SaaS Security API DLP policy rules."""
        return self._get("webDlpRules/lite")

    def post(self, payload):
        """Adds a new DLP policy rule."""
        """
        {
          "id": 0,
          "order": 0,
          "protocols": [
            "ANY_RULE"
          ],
          "rank": 0,
          "description": "string",
          "locations": [
            {
              "id": 0,
              "extensions": {
                "additionalProp1": "string",
                "additionalProp2": "string",
                "additionalProp3": "string"
              }
            }
          ],
          "locationGroups": [
            {
              "id": 0,
              "extensions": {
                "additionalProp1": "string",
                "additionalProp2": "string",
                "additionalProp3": "string"
              }
            }
          ],
          "groups": [
            {
              "id": 0,
              "extensions": {
                "additionalProp1": "string",
                "additionalProp2": "string",
                "additionalProp3": "string"
              }
            }
          ],
          "departments": [
            {
              "id": 0,
              "extensions": {
                "additionalProp1": "string",
                "additionalProp2": "string",
                "additionalProp3": "string"
              }
            }
          ],
          "users": [
            {
              "id": 0,
              "extensions": {
                "additionalProp1": "string",
                "additionalProp2": "string",
                "additionalProp3": "string"
              }
            }
          ],
          "urlCategories": [
            {
              "id": 0,
              "extensions": {
                "additionalProp1": "string",
                "additionalProp2": "string",
                "additionalProp3": "string"
              }
            }
          ],
          "dlpEngines": [
            {
              "id": 0,
              "extensions": {
                "additionalProp1": "string",
                "additionalProp2": "string",
                "additionalProp3": "string"
              }
            }
          ],
          "fileTypes": [
            "ANY"
          ],
          "cloudApplications": [
            "ANY"
          ],
          "minSize": 0,
          "action": "ANY",
          "state": "DISABLED",
          "timeWindows": [
            {
              "id": 0,
              "extensions": {
                "additionalProp1": "string",
                "additionalProp2": "string",
                "additionalProp3": "string"
              }
            }
          ],
          "auditor": {
            "id": 0,
            "extensions": {
              "additionalProp1": "string",
              "additionalProp2": "string",
              "additionalProp3": "string"
            }
          },
          "externalAuditorEmail": "string",
          "notificationTemplate": {
            "id": 0,
            "extensions": {
              "additionalProp1": "string",
              "additionalProp2": "string",
              "additionalProp3": "string"
            }
          },
          "matchOnly": true,
          "lastModifiedTime": 0,
          "lastModifiedBy": {
            "id": 0,
            "extensions": {
              "additionalProp1": "string",
              "additionalProp2": "string",
              "additionalProp3": "string"
            }
          },
          "icapServer": {
            "id": 0,
            "extensions": {
              "additionalProp1": "string",
              "additionalProp2": "string",
              "additionalProp3": "string"
            }
          },
          "withoutContentInspection": true,
          "name": "string",
          "labels": [
            {
              "id": 0,
              "extensions": {
                "additionalProp1": "string",
                "additionalProp2": "string",
                "additionalProp3": "string"
              }
            }
          ],
          "ocrEnabled": true,
          "excludedGroups": [
            {
              "id": 0,
              "extensions": {
                "additionalProp1": "string",
                "additionalProp2": "string",
                "additionalProp3": "string"
              }
            }
          ],
          "excludedDepartments": [
            {
              "id": 0,
              "extensions": {
                "additionalProp1": "string",
                "additionalProp2": "string",
                "additionalProp3": "string"
              }
            }
          ],
          "excludedUsers": [
            {
              "id": 0,
              "extensions": {
                "additionalProp1": "string",
                "additionalProp2": "string",
                "additionalProp3": "string"
              }
            }
          ],
          "zscalerIncidentReciever": true
        }
        """
        return self._post("webDlpRules", json=payload)

    def put(self, item_id, payload):
        return self._put(f"webDlpRules/{item_id}", json=payload)

    def delete(self, item_id):
        return self._delete(f"webDlpRules/{item_id}")
