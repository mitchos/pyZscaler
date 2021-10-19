from restfly.endpoint import APIEndpoint

from pyzscaler.utils import Iterator, snake_to_camel


class LocationsAPI(APIEndpoint):
    def list_locations(self, **kwargs):
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
            :obj:`list`: List of configured locations.

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
        return list(Iterator(self._api, "locations", **kwargs))

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

    def get_location(self, location_id: str = None, location_name: str = None):
        """
        Returns information for the specified location based on the location id or location name.

        Args:
            location_id (str, optional):
                The unique identifier for the location.
            location_name (str, optional):
                The unique name for the location.

        Returns:
            :obj:`dict`: The requested location resource record.

        Examples:
            >>> location = zia.locations.get_location('97456691')

            >>> location = zia.locations.get_location_name(name='stockholm_office')
        """
        if location_id and location_name:
            raise ValueError(
                "TOO MANY ARGUMENTS: Expected either a location_id or a location_name. Both were provided."
            )
        elif location_name:
            location = (
                record
                for record in self.list_locations(search=location_name)
                if record.name == location_name
            )
            return next(location, None)

        return self._get(f"locations/{location_id}")

    def list_sub_locations(self, location_id: str, **kwargs):
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
            :obj:`list`: A list of sub-locations configured for the parent location.

        Examples:
            >>> for sub_location in zia.locations.list_sub_locations('97456691'):
            ...    pprint(sub_location)

        """
        return list(
            Iterator(self._api, f"locations/{location_id}/sublocations", **kwargs)
        )

    def list_locations_lite(self, **kwargs):
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
            :obj:`list`: A list of configured locations.

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
        return list(Iterator(self._api, "locations/lite", **kwargs))

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
        # Set payload to value of existing record
        payload = {
            snake_to_camel(k): v for k, v in self.get_location(location_id).items()
        }

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
