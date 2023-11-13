from box import Box, BoxList
from restfly.endpoint import APIEndpoint

from pyzscaler.utils import Iterator, snake_to_camel


class LocationsAPI(APIEndpoint):
    def list_locations(self, **kwargs) -> BoxList:
        """
        Returns a list of locations.

        Keyword Args:
            **auth_required (bool, optional):
                Filter based on whether the Enforce Authentication setting is enabled or disabled for a location.
            **bw_enforced (bool, optional):
                Filter based on whether Bandwith Control is being enforced for a location.
            **max_items (int, optional):
                The maximum number of items to request before stopping iteration.
            **max_pages (int, optional):
                The maximum number of pages to request before stopping iteration.
            **page_size (int, optional):
                Specifies the page size. The default size is 100, but the maximum size is 1000.
            **search (str, optional):
                The search string used to partially match against a location's name and port attributes.
            **xff_enabled (bool, optional):
                Filter based on whether the Enforce XFF Forwarding setting is enabled or disabled for a location.

        Returns:
            :obj:`BoxList`: List of configured locations.

        Examples:
            List locations using default settings:

            >>> for location in zia.locations.list_locations():
            ...    print(location)

            List locations, limiting to a maximum of 10 items:

            >>> for location in zia.locations.list_locations(max_items=10):
            ...    print(location)

            List locations, returning 200 items per page for a maximum of 2 pages:

            >>> for location in zia.locations.list_locations(page_size=200, max_pages=2):
            ...    print(location)

        """
        return BoxList(Iterator(self._api, "locations", **kwargs))

    def add_location(self, name: str, **kwargs) -> Box:
        """
        Adds a new location.

        Args:
            name (str):
                Location name.

        Keyword Args:
            parent_id (int, optional):
                Parent Location ID. If this ID does not exist or is 0, it is implied that it is a parent location.
            up_bandwidth (int, optional):
                Upload bandwidth in kbps. The value 0 implies no Bandwidth Control enforcement. Default: 0.
            dn_bandwidth (int, optional):
                Download bandwidth in kbps. The value 0 implies no Bandwidth Control enforcement. Default: 0.
            country (str, optional):
                Country.
            tz (str, optional):
                Timezone of the location. If not specified, it defaults to GMT.
            ip_addresses (list[str], optional):
                For locations: IP addresses of the egress points that are provisioned in the Zscaler Cloud.
                Each entry is a single IP address (e.g., 238.10.33.9).

                For sub-locations: Egress, internal, or GRE tunnel IP addresses. Each entry is either a single
                IP address, CIDR (e.g., 10.10.33.0/24), or range (e.g., 10.10.33.1-10.10.33.10)).
            ports (list[int], optional):
                IP ports that are associated with the location.
            vpn_credentials (list, optional):
                VPN User Credentials that are associated with the location.
            auth_required (bool, optional):
                Enforce Authentication. Required when ports are enabled, IP Surrogate is enabled, or Kerberos
                Authentication is enabled. Default: False.
            ssl_scan_enabled (bool, optional):
                Enable SSL Inspection. Set to true in order to apply your SSL Inspection policy to HTTPS traffic in
                the location and inspect HTTPS transactions for data leakage, malicious content, and viruses.
                Default: False.
            zapp_ssl_scan_enabled (bool, optional):
                Enable Zscaler App SSL Setting. When set to true, the Zscaler App SSL Scan Setting takes effect,
                irrespective of the SSL policy that is configured for the location. Default: False.
            xff_forward_enabled (bool, optional):
                Enable XFF Forwarding for a location. When set to true, traffic is passed to Zscaler Cloud via the
                X-Forwarded-For (XFF) header. Default: False.
            other_sub_location (bool, optional):
                If set to true, indicates that this is a default sub-location created by the Zscaler service to
                accommodate IPv4 addresses that are not part of any user-defined sub-locations. Default: False.
            other6_sub_location (bool, optional):
                If set to true, indicates that this is a default sub-location created by the Zscaler service to
                accommodate IPv6 addresses that are not part of any user-defined sub-locations. Default: False.
            surrogate_ip (bool, optional):
                Enable Surrogate IP. When set to true, users are mapped to internal device IP addresses. Default: False.
            idle_time_in_minutes (int, optional):
                Idle Time to Disassociation. The user mapping idle time (in minutes) is required if Surrogate IP is
                enabled.
            display_time_unit (str, optional):
                Display Time Unit. The time unit to display for IP Surrogate idle time to disassociation.
            surrogate_ip_enforced_for_known_browsers (bool, optional):
                Enforce Surrogate IP for Known Browsers. When set to true, IP Surrogate is enforced for all known
                browsers. Default: False.
            surrogate_refresh_time_in_minutes (int, optional):
                Refresh Time for re-validation of Surrogacy. The surrogate refresh time (in minutes) to re-validate
                the IP surrogates.
            surrogate_refresh_time_unit (str, optional):
                Display Refresh Time Unit. The time unit to display for refresh time for re-validation of surrogacy.
            ofw_enabled (bool, optional):
                Enable Firewall. When set to true, Firewall is enabled for the location. Default: False.
            ips_control (bool, optional):
                Enable IPS Control. When set to true, IPS Control is enabled for the location if Firewall is enabled.
                Default: False.
            aup_enabled (bool, optional):
                Enable AUP. When set to true, AUP is enabled for the location. Default: False.
            caution_enabled (bool, optional):
                Enable Caution. When set to true, a caution notification is enabled for the location. Default: False.
            aup_block_internet_until_accepted (bool, optional):
                For First Time AUP Behavior, Block Internet Access. When set, all internet access (including non-HTTP
                traffic) is disabled until the user accepts the AUP. Default: False.
            aup_force_ssl_inspection (bool, optional):
                For First Time AUP Behavior, Force SSL Inspection. When set, Zscaler forces SSL Inspection in order
                to enforce AUP for HTTPS traffic. Default: False.
            ipv6_enabled (bool, optional):
                If set to true, IPv6 is enabled for the location and IPv6 traffic from the location can be forwarded
                to the Zscaler service to enforce security policies.
            ipv6_dns64_prefix (str, optional):
                Name-ID pair of the NAT64 prefix configured as the DNS64 prefix for the location.
            aup_timeout_in_days (int, optional):
                Custom AUP Frequency. Refresh time (in days) to re-validate the AUP.
            managed_by (str, optional):
                SD-WAN Partner that manages the location. If a partner does not manage the location, this is set to
                Self.
            profile (str, optional):
                Profile tag that specifies the location traffic type. If not specified, this tag defaults to
                "Unassigned".
            description (str, optional):
                Additional notes or information regarding the location or sub-location. The description cannot
                exceed 1024 characters.

        Returns:
            :obj:`Box`: The newly created location resource record

        Examples:
            Add a new location with an IP address.

            >>> zia.locations.add_location(name='new_location',
            ...    ip_addresses=['203.0.113.10'])

            Add a location with VPN credentials.

            >>> zia.locations.add_location(name='new_location',
            ...    vpn_credentials=[{'id': '99999', 'type': 'UFQDN'}])

        """
        payload = {
            "name": name,
        }

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        return self._post("locations", json=payload)

    def get_location(self, location_id: str = None, location_name: str = None) -> Box:
        """
        Returns information for the specified location based on the location id or location name.

        Args:
            location_id (str, optional):
                The unique identifier for the location.
            location_name (str, optional):
                The unique name for the location.

        Returns:
            :obj:`Box`: The requested location resource record.

        Examples:
            >>> location = zia.locations.get_location('97456691')

            >>> location = zia.locations.get_location_name(name='stockholm_office')
        """
        if location_id and location_name:
            raise ValueError("TOO MANY ARGUMENTS: Expected either location_id or location_name. Both were provided.")
        elif location_name:
            location = (record for record in self.list_locations(search=location_name) if record.name == location_name)
            return next(location, None)

        return self._get(f"locations/{location_id}")

    def list_sub_locations(self, location_id: str, **kwargs) -> BoxList:
        """
        Returns sub-location information for the specified location ID.

        Args:
            location_id (str):
                The unique identifier for the parent location.
            **kwargs:
                Optional keyword args.

        Keyword Args:
            **auth_required (bool, optional):
                Filter based on whether the Enforce Authentication setting is enabled or disabled for a location.
            **bw_enforced (bool, optional):
                Filter based on whether Bandwith Control is being enforced for a location.
            **enable_firewall (bool, optional):
                Filter based on whether Enable Firewall setting is enabled or disabled for a sub-location.
            **enforce_aup (bool, optional):
                Filter based on whether Enforce AUP setting is enabled or disabled for a sub-location.
            **max_items (int, optional):
                The maximum number of items to request before stopping iteration.
            **max_pages (int, optional):
                The maximum number of pages to request before stopping iteration.
            **page_size (int, optional):
                Specifies the page size. The default size is 100, but the maximum size is 1000.
            **search (str, optional):
                The search string used to partially match against a location's name and port attributes.
            **xff_enabled (bool, optional):
                Filter based on whether the Enforce XFF Forwarding setting is enabled or disabled for a location.

        Returns:
            :obj:`BoxList`: A list of sub-locations configured for the parent location.

        Examples:
            >>> for sub_location in zia.locations.list_sub_locations('97456691'):
            ...    pprint(sub_location)

        """
        return BoxList(Iterator(self._api, f"locations/{location_id}/sublocations", max_pages=1, **kwargs))

    def list_locations_lite(self, **kwargs) -> BoxList:
        """
        Returns only the name and ID of all configured locations.

        Keyword Args:
            **include_parent_locations (bool, optional):
                Only locations with sub-locations will be included in the response if `True`.
            **include_sub_locations (bool, optional):
                Sub-locations will be included in the response if `True`.
            **max_items (int, optional):
                The maximum number of items to request before stopping iteration.
            **max_pages (int, optional):
                The maximum number of pages to request before stopping iteration.
            **page_size (int, optional):
                Specifies the page size. The default size is 100, but the maximum size is 1000.
            **search (str, optional):
                The search string used to partially match against a location's name and port attributes.

        Returns:
            :obj:`BoxList`: A list of configured locations.

        Examples:
            List locations with default settings:

            >>> for location in zia.locations.list_locations_lite():
            ...    print(location)

            List locations, limiting to a maximum of 10 items:

            >>> for location in zia.locations.list_locations_lite(max_items=10):
            ...    print(location)

            List locations, returning 200 items per page for a maximum of 2 pages:

            >>> for location in zia.locations.list_locations_lite(page_size=200, max_pages=2):
            ...    print(location)

        """
        return BoxList(Iterator(self._api, "locations/lite", **kwargs))

    def update_location(self, location_id: str, **kwargs) -> Box:
        """
        Update the specified location.

        Note: Changes are not additive and will replace existing values.

        Args:
            location_id (str):
                The unique identifier for the location you are updating.
            **kwargs:
                Optional keyword arguments.

        Keyword Args:
            name (str, optional):
                Location name.
            parent_id (int, optional):
                Parent Location ID. If this ID does not exist or is 0, it is implied that it is a parent location.
            up_bandwidth (int, optional):
                Upload bandwidth in kbps. The value 0 implies no Bandwidth Control enforcement.
            dn_bandwidth (int, optional):
                Download bandwidth in kbps. The value 0 implies no Bandwidth Control enforcement.
            country (str, optional):
                Country.
            tz (str, optional):
                Timezone of the location. If not specified, it defaults to GMT.
            ip_addresses (list[str], optional):
                For locations: IP addresses of the egress points that are provisioned in the Zscaler Cloud.
                Each entry is a single IP address (e.g., 238.10.33.9).

                For sub-locations: Egress, internal, or GRE tunnel IP addresses. Each entry is either a single
                IP address, CIDR (e.g., 10.10.33.0/24), or range (e.g., 10.10.33.1-10.10.33.10)).
            ports (list[int], optional):
                IP ports that are associated with the location.
            vpn_credentials (list, optional):
                VPN User Credentials that are associated with the location.
            auth_required (bool, optional):
                Enforce Authentication. Required when ports are enabled, IP Surrogate is enabled, or Kerberos
                 Authentication is enabled.
            ssl_scan_enabled (bool, optional):
                Enable SSL Inspection. Set to true in order to apply your SSL Inspection policy to HTTPS traffic in the
                location and inspect HTTPS transactions for data leakage, malicious content, and viruses.
            zapp_ssl_scan_enabled (bool, optional):
                Enable Zscaler App SSL Setting. When set to true, the Zscaler App SSL Scan Setting takes effect,
                irrespective of the SSL policy that is configured for the location.
            xff_forward_enabled (bool, optional):
                Enable XFF Forwarding for a location. When set to true, traffic is passed to Zscaler Cloud via the
                X-Forwarded-For (XFF) header.
            other_sub_location (bool, optional):
                If set to true, indicates that this is a default sub-location created by the Zscaler service to
                accommodate IPv4 addresses that are not part of any user-defined sub-locations.
            other6_sub_location (bool, optional):
                If set to true, indicates that this is a default sub-location created by the Zscaler service to
                accommodate IPv6 addresses that are not part of any user-defined sub-locations.
            surrogate_ip (bool, optional):
                Enable Surrogate IP. When set to true, users are mapped to internal device IP addresses.
            idle_time_in_minutes (int, optional):
                Idle Time to Disassociation. The user mapping idle time (in minutes) is required if a Surrogate IP is
                enabled.
            display_time_unit (str, optional):
                Display Time Unit. The time unit to display for IP Surrogate idle time to disassociation.
            surrogate_ip_enforced_for_known_browsers (bool, optional):
                Enforce Surrogate IP for Known Browsers. When set to true, IP Surrogate is enforced for all known
                browsers.
            surrogate_refresh_time_in_minutes (int, optional):
                Refresh Time for re-validation of Surrogacy. The surrogate refresh time (in minutes) to re-validate
                the IP surrogates.
            surrogate_refresh_time_unit (str, optional):
                Display Refresh Time Unit. The time unit to display for refresh time for re-validation of surrogacy.
            ofw_enabled (bool, optional):
                Enable Firewall. When set to true, Firewall is enabled for the location.
            ips_control (bool, optional):
                Enable IPS Control. When set to true, IPS Control is enabled for the location if Firewall is enabled.
            aup_enabled (bool, optional):
                Enable AUP. When set to true, AUP is enabled for the location.
            caution_enabled (bool, optional):
                Enable Caution. When set to true, a caution notification is enabled for the location.
            aup_block_internet_until_accepted (bool, optional):
                For First Time AUP Behavior, Block Internet Access. When set, all internet access (including non-HTTP
                traffic) is disabled until the user accepts the AUP.
            aup_force_ssl_inspection (bool, optional):
                For First Time AUP Behavior, Force SSL Inspection. When set, Zscaler forces SSL Inspection in order to
                enforce AUP for HTTPS traffic.
            ipv6_enabled (bool, optional):
                If set to true, IPv6 is enabled for the location and IPv6 traffic from the location can be forwarded
                to the Zscaler service to enforce security policies.
            ipv6_dns64_prefix (str, optional):
                Name-ID pair of the NAT64 prefix configured as the DNS64 prefix for the location.
            aup_timeout_in_days (int, optional):
                Custom AUP Frequency. Refresh time (in days) to re-validate the AUP.
            managed_by (str, optional):
                SD-WAN Partner that manages the location. If a partner does not manage the location, this is set to
                Self.
            profile (str, optional):
                Profile tag that specifies the location traffic type. If not specified, this tag defaults to
                "Unassigned".
            description (str, optional):
                Additional notes or information regarding the location or sub-location. The description cannot exceed
                1024 characters.

        Returns:
            :obj:`Box`: The updated resource record.

        Examples:
            Update the name of a location:

            >>> zia.locations.update_location('99999',
            ...    name='updated_location_name')

            Update the IP address of a location:

            >>> zia.locations.update_location('99999',
            ...    ip_addresses=['203.0.113.20'])

            Update the VPN credentials of a location:

            >>> zia.locations.update_location('99999',
            ...    vpn_credentials=[{'id': '88888', 'type': 'UFQDN'}])

        """
        # Set payload to value of existing record
        payload = {snake_to_camel(k): v for k, v in self.get_location(location_id).items()}

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        # Fixes edge case where the sublocation object is missing displayTimeUnit, which will result in a 500 error.
        if not payload.get("displayTimeUnit"):
            payload["displayTimeUnit"] = "MINUTE"

        return self._put(f"locations/{location_id}", json=payload)

    def delete_location(self, location_id: str) -> int:
        """
        Deletes the location or sub-location for the specified ID

        Args:
            location_id (str):
                The unique identifier for the location or sub-location.

        Returns:
            :obj:`int`: Response code for the operation.

        Examples:
            >>> zia.locations.delete_location('97456691')

        """
        return self._delete(f"locations/{location_id}", box=False).status_code

    def get_geo_by_coordinates(self, latitude: int, longitude: int) -> Box:
        """
        Retrieves the geographical data of the region or city that is located in the specified latitude and longitude
        coordinates. The geographical data includes the city name, state, country, geographical ID of the city and
        state, etc.

        Args:
            latitude (int): The latitude of the location.
            longitude (int): The longitude of the location.

        Returns:
            :obj:`Box`: The geographical data of the region or city that is located in the specified coordinates.

        Examples:
            Get the geographical data of the region or city that is located in the specified coordinates::

                print(zia.locations.get_geo_by_coordinates(37.3860517, -122.0838511))

        """
        payload = {"latitude": latitude, "longitude": longitude}
        return self._get("region/byGeoCoordinates", params=payload)

    def get_geo_by_ip(self, ip: str) -> Box:
        """
        Retrieves the geographical data of the region or city that is located in the specified IP address. The
        geographical data includes the city name, state, country, geographical ID of the city and state, etc.

        Args:
            ip (str): The IP address of the location.

        Returns:
            :obj:`Box`: The geographical data of the region or city that is located in the specified IP address.

        Examples:
            Get the geographical data of the region or city that is located in the specified IP address::

                print(zia.locations.get_geo_by_ip("8.8.8.8")
        """
        return self._get(f"region/byIPAddress/{ip}")

    def list_cities_by_name(self, **kwargs) -> BoxList:
        """
        Retrieves the list of cities (along with their geographical data) that match the prefix search. The geographical
         data includes the latitude and longitude coordinates of the city, geographical ID of the city and state,
         country, postal code, etc.

        Args:
            **kwargs: Optional keyword arguments.

        Keyword Args:
            prefix (str): The prefix string to search for cities.
            page (int): The page number of the results.
            page_size (int): The number of results per page.

        Returns:
            :obj:`BoxList`: The list of cities (along with their geographical data) that match the prefix search.

        Examples:
            Get the list of cities (along with their geographical data) that match the prefix search::

                for city in zia.locations.list_cities_by_name(prefix="San Jose"):
                    print(city)

        Notes:
            Very broad or generic search terms may return a large number of results which can take a long time to be
            returned. Ensure you narrow your search result as much as possible to avoid this.

        """
        return BoxList(Iterator(self._api, "region/search", **kwargs))
