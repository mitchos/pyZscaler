import shutil
from datetime import datetime

from box import BoxList
from restfly.endpoint import APIEndpoint

from pyzscaler.utils import Iterator, convert_keys, zcc_param_map


class DevicesAPI(APIEndpoint):
    def download_devices(
        self,
        filename: str = None,
        os_types: list = None,
        registration_types: list = None,
    ):
        """
        Downloads the list of devices in the Client Connector Portal as a CSV file.

        By default, this method will create a file named `zcc-devices-YYmmDD-HH_MM_SS.csv`. This can be overridden by
        specifying the ``filename`` argument.

        Notes:
            This API endpoint is heavily rate-limited by Zscaler and as of NOV 2022 only 3 calls per-day are allowed.

        Args:
            filename (str):
                The name of the file that you want to save to disk.
            os_types (list):
                A list of OS Types to filter the device list. Omitting this argument will result in all OS types being
                matched.
                Valid options are:

                - ios
                - android
                - windows
                - macos
                - linux
            registration_types (list):
                A list of device registration states to filter the device list.
                Valid options are:

                - all (provides all states except for 'removed')
                - registered
                - removal_pending
                - unregistered
                - removed
                - quarantined

        Returns:
            :obj:`str`: The local filename for the CSV file that was downloaded.

        Examples:
            Create a CSV with all OS types and all registration types:

            >>> zcc.devices.download_devices(registration_types=["all", "removed"])

            Create a CSV for Windows and macOS devices that are in the `registered` state:

            >>> zcc.devices.download_devices(os_types=["windows", "macos"],
            ...     registration_types=["registered"])

            Create a CSV with filename `unregistered.csv` for devices in the unregistered state:

            >>> zcc.devices.download_devices(filename="unregistered.csv",
            ...     registration_types=["unregistered"])

        """

        if not filename:
            filename = f"zcc-devices-{datetime.now().strftime('%Y%m%d-%H_%M_%S')}.csv"

        payload = {
            "osTypes": [],
            "registrationTypes": [],
        }

        # Simplify the os_type argument, raise an error if the user supplies the wrong one.
        if os_types:
            for item in os_types:
                os_type = zcc_param_map["os"].get(item, None)
                if os_type:
                    payload["osTypes"].append(os_type)
                else:
                    raise ValueError(
                        "Invalid os_type specified. Check the pyZscaler documentation for valid os_type " "options."
                    )

        # Simplify the registration_type argument, raise an error if the user supplies the wrong one.
        if registration_types:
            for item in registration_types:
                reg_type = zcc_param_map["reg_type"].get(item, None)
                if reg_type:
                    payload["registrationTypes"].append(reg_type)
                else:
                    raise ValueError(
                        "Invalid registration_type specified. Check the pyZscaler documentation for valid "
                        "registration_type options."
                    )

        # Create the local file and stream the device list csv to it
        with self._get("public/v1/downloadDevices", params=payload, stream=True) as r:
            with open(filename, "wb") as f:
                shutil.copyfileobj(r.raw, f)

        return filename

    def list_devices(self, **kwargs) -> BoxList:
        """
        Returns the list of devices enrolled in the Client Connector Portal.

        Keyword Args:
            os_type (str):
                Filter by device operating system. Valid options are:

                - ios
                - android
                - windows
                - macos
                - linux
            page (int):
                Return a specific page number.
            page_size (int):
                Specify the number of devices per page, defaults to ``30``.
            user_name (str):
                Filter by the enrolled user for the device.

        Returns:
            :obj:`BoxList`: A list containing devices using ZCC enrolled in the Client Connector Portal.

        Examples:
            Prints all devices in the Client Connector Portal to the console:

            >>> for device in zcc.devices.list_devices():
            ...    print(device)

        """
        payload = convert_keys(dict(kwargs))

        # Simplify the os_type argument, raise an error if the user supplies the wrong one.
        if kwargs.get("os_type"):
            os_type = zcc_param_map["os"].get(payload["osType"], None)
            if os_type:
                payload["osType"] = os_type
            else:
                raise ValueError("Invalid os_type specified. Check the pyZscaler documentation for valid os_type " "options.")

        return BoxList(Iterator(self._api, "public/v1/getDevices", **payload))

    def remove_devices(self, force: bool = False, **kwargs):
        """
        Removes the specified devices from the Zscaler Client Connector Portal.

        Notes:
            You must be using API credentials with the `Write` role.
            You must specify at least one criterion from `Keyword Args` to remove devices.

        Args:
            force (bool):
                Setting force to ``True`` removes the enrolled device from the portal. You can only remove devices that are
                in the `registered` or `device removal pending` state.
            **kwargs:
                Optional keyword args.

        Keyword Args:
            client_connector_version (list):
                A list of client connector versions that will be removed. You must supply the exact version number, i.e.
                if the Client Connector version is `3.2.0.18` you must specify `3.2.0.18` and not `3.2`.
            os_type (str):
                The OS Type for the devices to be removed. Valid options are:

                - ios
                - android
                - windows
                - macos
                - linux
            udids (list):
                A list of Unique Device IDs.
            user_name (str):
                The username of the user whose devices will be removed.

        Returns:
            :obj:`Box`: Server response containing the total number of devices removed.

        Examples:
            Soft-remove devices using ZCC version 3.7.1.44 from the Client Connector Portal:

            >>> zcc.devices.remove_devices(client_connector_version=["3.7.1.44"])

            Soft-remove Android devices from the Client Connector Portal:

            >>> zcc.devices.remove_devices(os_type="android")

            Hard-remove devices from the Client Connector Portal by UDID:

            >>> zcc.devices.remove_devices(force=True, udids=["99999", "88888", "77777"])

            Hard-remove Android devices for johnno@widgets.co from the Client Connector Portal:

            >>> zcc.devices.remove_devices(force=True, os_type="android",
            ...     user_name="johnno@widgets.co")

        """
        payload = convert_keys(dict(kwargs))

        # Simplify the os_type argument, raise an error if the user supplies the wrong one.
        if kwargs.get("os_type"):
            os_type = zcc_param_map["os"].get(payload["osType"], None)
            if os_type:
                payload["osType"] = os_type
            else:
                raise ValueError("Invalid os_type specified. Check the pyZscaler documentation for valid os_type " "options.")

        if force:
            return self._post("public/v1/forceRemoveDevices", json=payload)
        else:
            return self._post("public/v1/removeDevices", json=payload)
