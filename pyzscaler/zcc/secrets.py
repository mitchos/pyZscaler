from restfly import APISession
from restfly.endpoint import APIEndpoint


class SecretsAPI(APIEndpoint):
    os_map = {
        "ios": 1,
        "android": 2,
        "windows": 3,
        "macos": 4,
        "linux": 5,
    }

    def __init__(self, api: APISession):
        super().__init__(api)
        self.company_id = api.company_id

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
            Print macos device passwords for username test@example.com:

            >>> print(zcc.secrets.get_passwords(username='test@example.com',
            ...    os_type='macos'))

        """

        payload = {
            "companyId": self.company_id,
        }

        # Simplify the os_type argument, raise an error if the user supplies the wrong one.
        os_type = self.os_map.get(os_type, None)
        if not os_type:
            raise ValueError("Invalid os_type specified. Check the pyZscaler documentation for valid os_type options.")

        params = {
            "username": username,
            "osType": os_type,
        }

        return self._get("public/v1/getPasswords", data=payload, params=params)
