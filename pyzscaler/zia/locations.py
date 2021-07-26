from restfly.endpoint import APIEndpoint
from box import BoxList
from pyzscaler.utils import snake_to_camel


class LocationsAPI(APIEndpoint):
    def list_locations(self):
        """
        Returns a list of configured locations.

        Returns:
            :obj:`list`: List of configured locations.

        Examples:
            >>> locations = zia.locations.list_locations()

        """
        return self._get("locations", box=BoxList)

    def add_location(self, name: str, **kwargs):
        """
        Adds a new location.

        Args:
            name (str):
                Location name.

        Keyword Args:
            ip_addresses (list):
                For locations: IP addresses of the egress points that are provisioned in the Zscaler Cloud.
                Each entry is a single IP address (e.g., 238.10.33.9).

                For sub-locations: Egress, internal, or GRE tunnel IP addresses. Each entry is either a single
                IP address, CIDR (e.g., 10.10.33.0/24), or range (e.g., 10.10.33.1-10.10.33.10)).
            ports (:obj:`list` of :obj:`str`):
                List of whitelisted Proxy ports for the location.
            vpn_credentials (dict):
                VPN credentials for the location.

        Returns:
            :obj:`dict`: The newly created location resource record

        Examples:
            Add a new location with an IP address.

            >>> zia.locations.add_location(name='new_location',
            ...    ip_addresses=['203.0.113.10'])

        """
        payload = {
            "name": name,
        }

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        return self._post("locations", json=payload)

    def get_location(self, location_id: str):
        """
        Returns information for the specified location.

        Args:
            location_id (str):
                The unique identifier for the location.

        Returns:
            :obj:`dict`: The requested location resource record.

        Examples:
            >>> location = zia.locations.get_location('97456691')
        """
        return self._get(f"locations/{location_id}")

    def list_sub_locations(self, location_id: str):
        """
        Returns sub-location information for the specified location ID.

        Args:
            location_id (str):
                The unique identifier for the parent location.

        Returns:
            :obj:`list`: A list of sub-locations configured for the parent location.

        Examples:
            >>> for sub_location in zia.locations.list_sub_locations('97456691'):
            ...    pprint(sub_location)

        """
        return self._get(f"locations/{location_id}/sublocations", box=BoxList)

    def list_locations_lite(self):
        """
        Returns only the name and ID of all configured locations.

        Returns:
            :obj:`list`: A list of configured locations.

        Examples:
            >>> for location in zia.locations.list_locations_lite():
            ...    pprint(location)

        """
        return self._get("locations/lite", box=BoxList)

    def update_location(self, location_id: str, **kwargs):
        """
        Update the specified location.

        Note: Changes are not additive and will replace existing values.

        Args:
            location_id (str):
                The unique identifier for the location you are updating.
            **kwargs:
                Optional keyword args.

        Keyword Args:
            ip_addresses (:obj:`list` of :obj:`str`):
                List of updated ip addresses.
            ports (:obj:`list` of :obj:`str`):
                List of whitelisted Proxy ports for the location.
            vpn_credentials (dict):
                VPN credentials for the location.

        Returns:
            :obj:`dict`: The updated resource record.

        Examples:
            Update the name of a location:

            >>> zia.locations.update('97456691',
            ...    name='updated_location_name')

            Upodate the IP address of a location:

            >>> zia.locations.update('97456691',
            ...    ip_addresses=['203.0.113.20'])

        """
        location_record = self.get_location(location_id)

        payload = {}

        # Check if required params are provided, if not, add to payload from existing record.
        if not kwargs.get("ip_addresses") and "ip_addresses" in location_record:
            payload["ipAddresses"] = location_record["ip_addresses"]

        if not kwargs.get("ports") and "ports" in location_record:
            payload["ports"] = location_record["ports"]

        if not kwargs.get("vpn_credentials") and "vpnCredentials" in location_record:
            payload["vpnCredentials"] = location_record["vpn_credentials"]

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        return self._put(f"locations/{location_id}", json=payload)

    def delete_location(self, location_id: str):
        """
        Deletes the location or sub-location for the specified ID

        Args:
            location_id (str):
                The unique identifier for the location or sub-location.

        Returns:
            :obj:`str`: Response code for the operation.

        Examples:
            >>> zia.locations.delete_location('97456691')

        """
        return self._delete(f"locations/{location_id}", box=False).status_code
