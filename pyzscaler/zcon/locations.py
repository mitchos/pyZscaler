from box import Box, BoxList
from restfly import APIEndpoint


class LocationsAPI(APIEndpoint):
    def list_locations(self, **kwargs) -> BoxList:
        """
        List all existing locations.

        Keyword Args:
            group_id (str): The ID of the connector group.
            search (str): The search string to filter the results.
            state (str): The geographical state of the location.
            ssl_scan_enabled (bool): Include / exclude locations with SSL scanning enabled.
            xff_enabled (bool): Include / exclude locations with XFF enabled.
            auth_required (bool): Include / exclude locations with authentication required.
            bw_enforced (bool): Include / exclude locations with bandwidth enforcement enabled.
            partner_id (str): The ID of the partner. Not used for Cloud/Branch connector
            enforce_aup (bool): Include / exclude locations with AUP enforcement enabled.
            enable_firewall (bool): Include / exclude locations with firewall enabled.
            location_type (str): The type of location, accepted values are:
                - "NONE"
                - "CORPORATE"
                - "SERVER"
                - "GUESTWIFI"
                - "IOT"
                - "WORKLOAD"
            page (int): The page number to return.
            page_size (int): The number of items to return per page.

        Returns:
            :obj:`BoxList`: The list of connector locations.

        Examples:
            >>> print(zcon.locations.list_locations()

            List only IOT locations:
            >>> print(zcon.locations.list_locations(location_type="IOT")

        """
        return self._get("location")

    def get_location(self, location_id: str) -> Box:
        """
        Get details for a specific location.

        Args:
            location_id (str): The ID of the location to retrieve.

        Returns:
            :obj:`Box`: The location details.

        Examples:
            >>> print(zcon.locations.get_location("123456789")

        """
        return self._get(f"adminRoles/{location_id}")

    def list_location_templates(self, **kwargs) -> BoxList:
        """
        List all existing location templates.

        Args:
            **kwargs: Optional keyword args to filter the results.

        Keyword Args:
            page (int): The page number to return.
            page_size (int): The number of items to return per page.

        Returns:
            :obj:`BoxList`: The list of location templates.

        Examples:
            >>> print(zcon.locations.list_location_templates()

        """
        return self._get("locationTemplate")

    def get_location_template(self, template_id: str) -> Box:
        """
        Get details for a specific location template.

        Args:
            template_id (str): The ID of the location template to retrieve.

        Returns:
            :obj:`Box`: The location template details.

        Examples:
            >>> print(zcon.locations.get_location_template("123456789")

        """
        return self._get(f"locationTemplate/{template_id}")
