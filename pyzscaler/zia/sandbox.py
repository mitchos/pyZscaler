from restfly.endpoint import APIEndpoint
from box import BoxList


class CloudSandboxAPI(APIEndpoint):
    def get_quota(self):
        """
        Returns the Cloud Sandbox API quota information for the organisation.

        Returns:
            :obj:`dict`: The Cloud Sandbox quota report.

        Examples:
            >>> pprint(zia.sandbox.get_quota())

        """
        return self._get("sandbox/report/quota", box=BoxList)[0]

    def get_report(self, md5_hash: str, report_details: str = "summary"):
        """
        Returns the Cloud Sandbox Report for the provided hash.

        Args:
            md5_hash (str):
                The MD5 hash of the file that was analysed by Cloud Sandbox.
            report_details (str):
                The type of report. Accepted values are 'full' or 'summary'. Defaults to 'summary'.

        Returns:
            :obj:`dict`: The cloud sandbox report.

        Examples:
            Get a summary report:

            >>> zia.sandbox.get_report('8350dED6D39DF158E51D6CFBE36FB012')

            Get a full report:

            >>> zia.sandbox.get_report('8350dED6D39DF158E51D6CFBE36FB012', 'full')

        """

        return self._get(f"sandbox/report/{md5_hash}?details={report_details}")
