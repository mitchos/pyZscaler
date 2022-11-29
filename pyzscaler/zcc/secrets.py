from restfly.endpoint import APIEndpoint

from pyzscaler.utils import zcc_param_map


class SecretsAPI(APIEndpoint):
    def get_otp(self, device_id: str):
        """
        Returns the OTP code for the specified device id.

        Args:
            device_id (str): The unique id for the enrolled device that the OTP will be obtained for.

        Returns:
            :obj:`Box`: A dictionary containing the requested OTP code for the specified device id.

        Examples:
            Obtain the OTP code for a device and print it to console:

            >>> otp_code = zcc.secrets.get_otp('System-Serial-Number:1234ABCDEF')
            ... print(otp_code.otp)

        """

        payload = {"udid": device_id}

        return self._get("public/v1/getOtp", params=payload)

    def get_passwords(self, username: str, os_type: str = "windows"):
        """
        Return passwords for the specified username and device OS type.

        Args:
            username (str): The username that the device belongs to.
            os_type (str): The OS Type for the device, defaults to `windows`. Valid options are:

                - ios
                - android
                - windows
                - macos
                - linux

        Returns:
            :obj:`Box`: Dictionary containing passwords for the specified username's device.

        Examples:
            Print macOS device passwords for username test@example.com:

            >>> print(zcc.secrets.get_passwords(username='test@example.com',
            ...    os_type='macos'))

        """

        # Simplify the os_type argument, raise an error if the user supplies the wrong one.
        os_type = zcc_param_map["os"].get(os_type, None)
        if not os_type:
            raise ValueError("Invalid os_type specified. Check the pyZscaler documentation for valid os_type options.")

        params = {
            "username": username,
            "osType": os_type,
        }

        return self._get("public/v1/getPasswords", params=params)
