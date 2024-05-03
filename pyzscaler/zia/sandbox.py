from box import Box
from restfly import APISession
from restfly.endpoint import APIEndpoint


class CloudSandboxAPI(APIEndpoint):
    def __init__(self, api: APISession):
        super().__init__(api)

        self.sandbox_token = api.sandbox_token
        self.env_cloud = api.env_cloud

    def submit_file(self, file: str, force: bool = False) -> Box:
        """
        Submits a file to the ZIA Advanced Cloud Sandbox for analysis.

        Args:
            file (str): The filename that will be submitted for sandbox analysis.
            force (bool): Force ZIA to analyse the file even if it has been submitted previously.

        Returns:
            :obj:`Box`: The Cloud Sandbox submission response information.

        Examples:
            Submit a file in the current directory called malware.exe to the cloud sandbox, forcing analysis.

            >>> zia.sandbox.submit_file('malware.exe', force=True)

        """
        with open(file, "rb") as f:
            data = f.read()

        params = {
            "api_token": self.sandbox_token,
            "force": int(force),  # convert boolean to int for ZIA
        }

        return self._post(f"https://csbapi.{self.env_cloud}.net/zscsb/submit", params=params, data=data)

    def get_quota(self) -> Box:
        """
        Returns the Cloud Sandbox API quota information for the organisation.

        Returns:
            :obj:`Box`: The Cloud Sandbox quota report.

        Examples:
            >>> pprint(zia.sandbox.get_quota())

        """
        return self._get("sandbox/report/quota")[0]

    def get_report(self, md5_hash: str, report_details: str = "summary") -> Box:
        """
        Returns the Cloud Sandbox Report for the provided hash.

        Args:
            md5_hash (str):
                The MD5 hash of the file that was analysed by Cloud Sandbox.
            report_details (str):
                The type of report. Accepted values are 'full' or 'summary'. Defaults to 'summary'.

        Returns:
            :obj:`Box`: The cloud sandbox report.

        Examples:
            Get a summary report:

            >>> zia.sandbox.get_report('8350dED6D39DF158E51D6CFBE36FB012')

            Get a full report:

            >>> zia.sandbox.get_report('8350dED6D39DF158E51D6CFBE36FB012', 'full')

        """

        return self._get(f"sandbox/report/{md5_hash}?details={report_details}")

    def submit_file_oob(self, filename: str) -> Box:
        """
        Submits a file to the ZIA Advanced Cloud Sandbox for out-of-band (oob) analysis.

        Args:
            filename (str): The filename that will be submitted for sandbox analysis.

        Returns:
            :obj:`Box`: The Cloud Sandbox submission response information.

        Examples:
            Submit a file in the current directory called malware.exe to the cloud sandbox for oob analysis.

            >>> zia.sandbox.submit_file_oob('malware.exe')

        """
        with open(filename, "rb") as f:
            data = f.read()

        params = {
            "api_token": self.sandbox_token,
        }

        return self._post(f"https://csbapi.{self.env_cloud}.net/zscsb/discan", params=params, data=data)
