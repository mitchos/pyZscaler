from box import BoxList
from restfly import APISession
from restfly.endpoint import APIEndpoint

from pyzscaler.utils import Iterator, convert_keys, zcc_os_map


class DevicesAPI(APIEndpoint):
    def __init__(self, api: APISession):
        super().__init__(api)
        self.company_id = api.company_id

    def list_devices(self, **kwargs) -> BoxList:
        """
        Returns the list of devices enrolled in the Mobile Admin Portal.

        Keyword Args:
            os_type (str):
                Filter by device operating system.
            page (int):
                Return a specific page number.
            page_size (int):
                Specify the number of devices per page, defaults to 30.
            username (str):
                Filter by the enrolled user for the device.

        Returns:
            :obj:`BoxList`: A list containing devices using ZCC enrolled in the Mobile Admin Portal.

        Examples:
            Prints all devices in the Mobile Admin Portal to the console:

            >>> for device in zcc.devices.list_devices():
            ...    print(device)

        """
        payload = convert_keys(dict(kwargs))

        # Simplify the os_type argument, raise an error if the user supplies the wrong one.
        if kwargs.get("os_type"):
            os_type = zcc_os_map.get(payload["osType"], None)
            if not os_type:
                raise ValueError("Invalid os_type specified. Check the pyZscaler documentation for valid os_type options.")
            else:
                payload["osType"] = os_type

        return BoxList(Iterator(self._api, "public/v1/getDevices", **payload))
