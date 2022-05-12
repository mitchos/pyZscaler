from box import BoxList
from restfly import APISession
from restfly.endpoint import APIEndpoint


class DevicesAPI(APIEndpoint):
    def __init__(self, api: APISession):
        super().__init__(api)
        self.company_id = api.company_id

    def list_devices(self) -> BoxList:
        """
        Returns the list of devices enrolled in the Mobile Admin Portal.

        Returns:
            :obj:`BoxList`: A list containing devices using ZCC enrolled in the Mobile Admin Portal.

        Examples:
            Prints all devices in the Mobile Admin Portal to the console:

            >>> for device in zcc.devices.list_devices():
            ...    print(device)

        """
        payload = {"companyId": self.company_id}

        return self._get("public/v1/getDevices", json=payload)
