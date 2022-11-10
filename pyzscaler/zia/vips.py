from box import Box, BoxList
from restfly.endpoint import APIEndpoint


class DataCenterVIPSAPI(APIEndpoint):
    def list_public_se(self, cloud: str, continent: str = None) -> Box:
        """
        Returns a list of the Zscaler Public Service Edge information for the specified cloud.

        Args:
            cloud (str): The ZIA cloud that this request applies to.
            continent (str, opt):
                Filter entries by the specified continent. Accepted values are `apac`, `emea` and `amer`.

        Returns:
            :obj:`Box`: The Public Service Edge VIPs

        Examples:
            Print all Public Service Edge information for ``zscaler.net``:

            >>> pprint(zia.vips.list_public_se('zscaler'))

            Print all Public Service Edge information for ``zscalerthree.net`` in ``apac``:

            >>> pprint(zia.vips.list_public_se('zscalerthree',
            ...    continent='apac')

        """

        if continent is not None:
            if continent == "amer":
                # This return is an edge-case to handle the JSON structure for _americas which is in the format
                # continent :_americas. All other continents have whitespace, e.g. continent : emea.
                return self._get(f"https://api.config.zscaler.com/{cloud}.net/cenr/json")[f"{cloud}.net"][
                    "continent :_americas"
                ]

            return self._get(f"https://api.config.zscaler.com/{cloud}.net/cenr/json")[f"{cloud}.net"][
                f"continent : {continent}"
            ]

        return self._get(f"https://api.config.zscaler.com/{cloud}.net/cenr/json")[f"{cloud}.net"]

    def list_ca(self, cloud: str) -> BoxList:
        """
        Returns a list of Zscaler Central Authority server IPs for the specified cloud.

        Args:
            cloud (str):  The ZIA cloud that this request applies to.

        Returns:
            :obj:`BoxList`: A list of CA server IPs.

        Examples:
            Print the IP address of Central Authority servers in `zscalertwo.net`:

            >>> for ip in zia.vips.list_ca('zscalertwo'):
            ...    print(ip)

        """
        return self._get(f"https://api.config.zscaler.com/{cloud}.net/ca/json")["ranges"]

    def list_pac(self, cloud: str) -> BoxList:
        """
        Returns a list of Proxy Auto-configuration (PAC) server IPs for the specified cloud.

        Args:
            cloud (str): The ZIA cloud that this request applies to.

        Returns:
            :obj:`BoxList`: A list of PAC server IPs.

        Examples:
            Print the IP address of PAC servers in `zscloud.net`:

            >>> for ip in zia.vips.list_pac('zscloud'):
            ...    print(ip)

        """
        return self._get(f"https://api.config.zscaler.com/{cloud}.net/pac/json")["ip"]
