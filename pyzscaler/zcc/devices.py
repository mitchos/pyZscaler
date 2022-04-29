from box import Box
from restfly.endpoint import APIEndpoint


class DevicesAPI(APIEndpoint):
    def list_devices(self) -> Box:
        """ """
        payload = {
            "companyId": 5117,
        }

        parameters = {"page": 1, "pageSize": 100, "search": ""}

        resp = self._get("public/v1/getDevices", json=payload, params=parameters)
        return resp
