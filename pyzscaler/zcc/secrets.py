from restfly import APISession
from restfly.endpoint import APIEndpoint

from pyzscaler.utils import snake_to_camel


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

    def get_passwords(self, username: str, os_type: str = "windows", **kwargs):
        """
        Return passwords for the specified username and device OS type.

        Args:
            username:
            os_type:
            **kwargs:

        Returns:

        """

        payload = {
            "companyId": self.company_id,
        }

        # Simplify the os_type argument, raise an error if the user supplies the wrong one.
        os_type = self.os_map.get(os_type, None)
        if not os_type:
            raise ValueError("Invalid os_type specified. Check the pyZscaler documentation for valid os_type options.")

        params = {"username": username, "osType": os_type}

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        return self._get("public/v1/getPasswords", data=payload, params=params)
