from box import BoxList
from restfly.endpoint import APIEndpoint

from pyzscaler.utils import Iterator, snake_to_camel


class TrafficForwardingAPI(APIEndpoint):
    def list_gre_tunnels(self, **kwargs):
        """
        Returns the list of all configured GRE tunnels.

        Keyword Args:
            **max_items (int, optional):
                The maximum number of items to request before stopping iteration.
            **max_pages (int, optional):
                The maximum number of pages to request before stopping iteration.
            **page_size (int, optional):
                Specifies the page size. The default size is 100, but the maximum size is 1000.

        Returns:
            :obj:`list`: A list of GRE tunnels configured in ZIA.

        Examples:
            List GRE tunnels with default settings:

            >>> for tunnel in zia.traffic.list_gre_tunnels():
            ...    print(tunnel)

            List GRE tunnels, limiting to a maximum of 10 items:

            >>> for tunnel in zia.traffic.list_gre_tunnels(max_items=10):
            ...    print(tunnel)

            List GRE tunnels, returning 200 items per page for a maximum of 2 pages:

            >>> for tunnel in zia.traffic.list_gre_tunnels(page_size=200, max_pages=2):
            ...    print(tunnel)

        """
        return list(Iterator(self._api, "greTunnels", **kwargs))

    def get_gre_tunnel(self, tunnel_id: str):
        """
        Returns information for the specified GRE tunnel.

        Args:
            tunnel_id (str):
                The unique identifier for the GRE tunnel.

        Returns:
            :obj:`dict`: The GRE tunnel resource record.

        Examples:
            >>> gre_tunnel = zia.traffic.get_gre_tunnel('967134')

        """
        return self._get(f"greTunnels/{tunnel_id}")

    def list_gre_ranges(self, **kwargs):
        """
        Returns a list of available GRE tunnel ranges.

        Keyword Args:
            **internal_ip_range (str, optional):
                Internal IP range information.
            **static_ip (str, optional):
                Static IP information.
            **limit (int, optional):
                The maximum number of GRE tunnel IP ranges that can be added. Defaults to `10`.

        Returns:
            :obj:`list`: A list of available GRE tunnel ranges.

        Examples:
            >>> gre_tunnel_ranges = zia.traffic.list_gre_ranges()

        """
        payload = {snake_to_camel(key): value for key, value in kwargs.items()}

        return self._get("greTunnels/availableInternalIpRanges", params=payload, box=BoxList)

    def add_gre_tunnel(
        self,
        source_ip: str,
        primary_dest_vip_id: str = None,
        secondary_dest_vip_id: str = None,
        **kwargs,
    ):
        """
        Add a new GRE tunnel.

        Note: If the `primary_dest_vip_id` and `secondary_dest_vip_id` aren't specified then the closest recommended
        VIPs will be automatically chosen.

        Args:
            source_ip (str):
                The source IP address of the GRE tunnel. This is typically a static IP address in the organisation
                or SD-WAN.
            primary_dest_vip_id (str):
                The unique identifier for the primary destination virtual IP address (VIP) of the GRE tunnel.
                Defaults to the closest recommended VIP.
            secondary_dest_vip_id (str):
                The unique identifier for the secondary destination virtual IP address (VIP) of the GRE tunnel.
                Defaults to the closest recommended VIP that isn't in the same city as the primary VIP.

        Keyword Args:
             **comment (str):
                Additional information about this GRE tunnel
             **ip_unnumbered (bool):
                This is required to support the automated SD-WAN provisioning of GRE tunnels, when set to true
                gre_tun_ip and gre_tun_id are set to null
             **internal_ip_range (str):
                The start of the internal IP address in /29 CIDR range.
             **within_country (bool):
                Restrict the data center virtual IP addresses (VIPs) only to those within the same country as the
                source IP address.

        Returns:
            :obj:`dict`: The resource record for the newly created GRE tunnel.

        Examples:
            Add a GRE tunnel with closest recommended VIPs:

            >>> zia.traffic.add_gre_tunnel('203.0.113.10')

            Add a GRE tunnel with explicit VIPs:

            >>> zia.traffic.add_gre_tunnel('203.0.113.11',
            ...    primary_dest_vip_id='88088',
            ...    secondary_dest_vip_id='54590',
            ...    comment='GRE Tunnel for Manufacturing Plant')

        """

        # If primary/secondary VIPs not provided, add the closest diverse VIPs
        if primary_dest_vip_id is None and secondary_dest_vip_id is None:
            recommended_vips = self.get_closest_diverse_vip_ids(source_ip)
            primary_dest_vip_id = recommended_vips[0]
            secondary_dest_vip_id = recommended_vips[1]

        payload = {
            "sourceIp": source_ip,
            "primaryDestVip": {"id": primary_dest_vip_id},
            "secondaryDestVip": {"id": secondary_dest_vip_id},
        }

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        return self._post("greTunnels", json=payload)

    def list_static_ips(self, **kwargs):
        """
        Returns the list of all configured static IPs.

        Keyword Args:
            **available_for_gre_tunnel (bool, optional):
                Only return the static IP addresses that are not yet associated with a GRE tunnel if True.
                Defaults to False.
            **ip_address (str, optional):
                Filter based on IP address.
            **max_items (int, optional):
                The maximum number of items to request before stopping iteration.
            **max_pages (int, optional):
                The maximum number of pages to request before stopping iteration.
            **page_size (int, optional):
                Specifies the page size. The default size is 100, but the maximum size is 1000.

        Returns:
            :obj:`list`: A list of the configured static IPs

        Examples:
            List static IPs using default settings:

            >>> for ip_address in zia.traffic.list_static_ips():
            ...    print(ip_address)

            List static IPs, limiting to a maximum of 10 items:

            >>> for ip_address in zia.traffic.list_static_ips(max_items=10):
            ...    print(ip_address)

            List static IPs, returning 200 items per page for a maximum of 2 pages:

            >>> for ip_address in zia.traffic.list_static_ips(page_size=200, max_pages=2):
            ...    print(ip_address)

        """

        return list(Iterator(self._api, "staticIP", **kwargs))

    def get_static_ip(self, static_ip_id: str):
        """
        Returns information for the specified static IP.

        Args:
            static_ip_id (str):
                The unique identifier for the static IP.

        Returns:
            :obj:`dict`: The resource record for the static IP

        Examples:
            >>> static_ip = zia.traffic.get_static_ip('967134')

        """
        return self._get(f"staticIP/{static_ip_id}")

    def add_static_ip(self, ip_address: str, **kwargs):
        """
        Adds a new static IP.

        Args:
            ip_address (str):
                The static IP address

        Keyword Args:
            **comment (str):
                Additional information about this static IP address.
            **geo_override (bool):
                If not set, geographic coordinates and city are automatically determined from the IP address.
                Otherwise, the latitude and longitude coordinates must be provided.
            **routable_ip (bool):
                Indicates whether a non-RFC 1918 IP address is publicly routable. This attribute is ignored if there
                is no ZIA Private Service Edge associated to the organization.
            **latitude (float):
                Required only if the geoOverride attribute is set. Latitude with 7 digit precision after
                decimal point, ranges between -90 and 90 degrees.
            **longitude (float):
                Required only if the geoOverride attribute is set. Longitude with 7 digit precision after decimal
                point, ranges between -180 and 180 degrees.

        Returns:
            :obj:`dict`: The resource record for the newly created static IP.

        Examples:
            Add a new static IP address:

            >>> zia.traffic.add_static_ip(ip_address='203.0.113.10',
            ...    comment="Los Angeles Branch Office")

        """

        payload = {
            "ipAddress": ip_address,
        }

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        return self._post("staticIP", json=payload)

    def check_static_ip(self, ip_address: str, **kwargs):
        """
        Validates if a static IP object is correct.

        Args:
            ip_address (str):
                The static IP address
            **kwargs:
                Optional keyword args.

        Keyword Args:
            **comment (str):
                Additional information about this static IP address.
            **geo_override (bool):
                If not set, geographic coordinates and city are automatically determined from the IP address.
                Otherwise, the latitude and longitude coordinates must be provided.
            **routable_ip (bool):
                Indicates whether a non-RFC 1918 IP address is publicly routable. This attribute is ignored if there
                is no ZIA Private Service Edge associated to the organization.
            **latitude (float):
                Required only if the geoOverride attribute is set. Latitude with 7 digit precision after
                decimal point, ranges between -90 and 90 degrees.
            **longitude (float):
                Required only if the geoOverride attribute is set. Longitude with 7 digit precision after decimal
                point, ranges between -180 and 180 degrees.

        Returns:
            :obj:`str`: The operation response code.

        Examples:
            >>> zia.traffic.check_static_ip(ip_address='203.0.113.11',
            ...    routable_ip=True,
            ...    comment='San Francisco Branch Office')

        """
        payload = {
            "ipAddress": ip_address,
        }

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        return self._post("staticIP/validate", json=payload, box=False).status_code

    def update_static_ip(self, static_ip_id: str, **kwargs):
        """
        Updates information relating to the specified static IP.

        Args:
            static_ip_id (str):
                The unique identifier for the static IP
            **kwargs:
                Optional keyword args.

        Keyword Args:
            **comment (str):
                Additional information about this static IP address.
            **geo_override (bool):
                If not set, geographic coordinates and city are automatically determined from the IP address.
                Otherwise, the latitude and longitude coordinates must be provided.
            **routable_ip (bool):
                Indicates whether a non-RFC 1918 IP address is publicly routable. This attribute is ignored if there
                is no ZIA Private Service Edge associated to the organization.
            **latitude (float):
                Required only if the geoOverride attribute is set. Latitude with 7 digit precision after
                decimal point, ranges between -90 and 90 degrees.
            **longitude (float):
                Required only if the geoOverride attribute is set. Longitude with 7 digit precision after decimal
                point, ranges between -180 and 180 degrees.

        Returns:
            :obj:`dict`: The updated static IP resource record.

        Examples:
            >>> zia.traffic.update_static_ip('972494', comment='NY Branch Office')

        """

        payload = {
            "id": static_ip_id,
            "ipAddress": self.get_static_ip(
                static_ip_id
            ),  # ZIA API requires existing IP but can't be modified
        }

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        return self._put(f"staticIP/{static_ip_id}", json=payload)

    def delete_static_ip(self, static_ip_id: str):
        """
        Delete the specified static IP.

        Args:
            static_ip_id (str):
                The unique identifier for the static IP.

        Returns:
            :obj:`str`: The response code for the operation.

        Examples:
            >>> zia.traffic.delete_static_ip('972494')

        """

        return self._delete(f"staticIP/{static_ip_id}", box=False).status_code

    def list_vips(self, **kwargs):
        """
        Returns a list of virtual IP addresses (VIPs) available in the Zscaler cloud.

        Keyword Args:
            **dc (str, optional):
                Filter based on data center.
            **include (str, optional):
                Include all, private, or public VIPs in the list. Available choices are `all`, `private`, `public`.
                Defaults to `public`.
            **max_items (int, optional):
                The maximum number of items to request before stopping iteration.
            **max_pages (int, optional):
                The maximum number of pages to request before stopping iteration.
            **page_size (int, optional):
                Specifies the page size. The default size is 100, but the maximum size is 1000.
            **region (str, optional):
                Filter based on region.

        Returns:
            :obj:`list` of :obj:`dict`: List of VIP resource records.

        Examples:
            List VIPs using default settings:

            >>> for vip in zia.traffic.list_vips():
            ...    pprint(vip)

            List VIPs, limiting to a maximum of 10 items:

            >>> for vip in zia.traffic.list_vips(max_items=10):
            ...    print(vip)

            List VIPs, returning 200 items per page for a maximum of 2 pages:

            >>> for vip in zia.traffic.list_vips(page_size=200, max_pages=2):
            ...    print(vip)

        """
        return list(Iterator(self._api, "vips", **kwargs))

    def list_vips_recommended(self, **kwargs):
        """
        Returns a list of recommended virtual IP addresses (VIPs) based on parameters.

        Args:
            **kwargs:
                Optional keywords args.

        Keyword Args:
            routable_ip (bool):
                The routable IP address. Default: True.
            within_country_only (bool):
                Search within country only. Default: False.
            include_private_service_edge (bool):
                Include ZIA Private Service Edge VIPs. Default: True.
            include_current_vips (bool):
                Include currently assigned VIPs. Default: True.
            source_ip (str):
                The source IP address.
            latitude (str):
                Latitude coordinate of GRE tunnel source.
            longitude (str):
                Longitude coordinate of GRE tunnel source.
            geo_override (bool):
                Override the geographic coordinates. Default: False.

        Returns:
            :obj:`list` of :obj:`dict`: List of VIP resource records.

        Examples:
            Return recommended VIPs for a given source IP:

            >>> for vip in zia.traffic.list_vips_recommended(source_ip='203.0.113.30'):
            ...    pprint(vip)

        """
        payload = {snake_to_camel(key): value for key, value in kwargs.items()}

        return self._get("vips/recommendedList", params=payload, box=BoxList)

    def get_closest_diverse_vip_ids(self, ip_address: str):
        """
        Returns the closest diverse Zscaler destination VIPs for a given IP address.

        Args:
            ip_address (str):
                The IP address used for locating the closest diverse VIPs.

        Returns:
            :obj:`tuple` of :obj:`str`: Tuple containing the preferred and secondary VIP IDs.

        Examples:
            >>> closest_vips = zia.traffic.get_closest_diverse_vip_ids('203.0.113.20')

        """
        vips_list = self.list_vips_recommended(source_ip=ip_address)
        preferred_vip = vips_list[0]  # First entry is closest vip

        # Generator to find the next closest vip not in the same city as our preferred
        secondary_vip = next(
            (vip for vip in vips_list if vip.city != preferred_vip.city)
        )
        recommended_vips = (preferred_vip.id, secondary_vip.id)

        return recommended_vips

    def list_vpn_credentials(self, **kwargs):
        """
        Returns the list of all configured VPN credentials.

        Args:
            **kwargs:
                Optional keyword search filters.

        Keyword Args:
            **include_only_without_location (bool, optional):
                Include VPN credential only if not associated to any location.
            **location_id (int, optional):
                Gets the VPN credentials for the specified location ID.

                **NOTE**: Included for completeness as per documentation, but the ZIA API does not respond with
                filtered results.
            **max_items (int, optional):
                The maximum number of items to request before stopping iteration.
            **max_pages (int, optional):
                The maximum number of pages to request before stopping iteration.
            **page_size (int, optional):
                Specifies the page size. The default size is 100, but the maximum size is 1000.
            **search (str, optional):
                The search string used to match against a VPN credential's commonName, fqdn, ipAddress,
                comments, or locationName
            **type (str, optional):
                Only gets VPN credentials for the specified type (CN, IP, UFQDN, XAUTH)

        Returns:
            :obj:`list` of :obj:`dict`: List containing the VPN credential resource records.

        Examples:
            List VPN credentials using default settings:

            >>> for credential in zia.traffic.list_vpn_credentials:
            ...    pprint(credential)

            List VPN credentials, limiting to a maximum of 10 items:

            >>> for credential in zia.traffic.list_vpn_credentials(max_items=10):
            ...    print(credential)

            List VPN credentials, returning 200 items per page for a maximum of 2 pages:

            >>> for credential in zia.traffic.list_vpn_credentials(page_size=200, max_pages=2):
            ...    print(credential)

        """
        return list(Iterator(self._api, "vpnCredentials", **kwargs))

    def add_vpn_credential(
        self, authentication_type: str, pre_shared_key: str, **kwargs
    ):
        """
        Add new VPN credentials.

        Args:
            authentication_type (str):
                VPN authentication type (i.e., how the VPN credential is sent to the server). It is not modifiable
                after VpnCredential is created.

                Only IP and UFQDN supported via API.
            pre_shared_key (str):
                Pre-shared key. This is a required field for UFQDN and IP auth type.

        Keyword Args:
            ip_address (str):
                The static IP address associated with these VPN credentials.
            fqdn (str):
                Fully Qualified Domain Name. Applicable only to UFQDN auth type. This must be provided in the format
                `userid@fqdn`, where the `fqdn` is an authorised domain for your tenancy.
            comments (str):
                Additional information about this VPN credential.
            location_id (str):
                Associate the VPN credential with an existing location.

        Returns:
            :obj:`dict`: The newly created VPN credential resource record.

        Examples:
            Add a VPN credential using IP authentication type before location has been defined:

            >>> zia.traffic.add_vpn_credential(authentication_type='IP',
            ...    pre_shared_key='MyInsecurePSK',
            ...    ip_address='203.0.113.40',
            ...    comments='NY Branch Office')

            Add a VPN credential using UFQDN authentication type and associate with location:

            >>> zia.traffic.add_vpn_credential(authentication_type='UFQDN',
            ...    pre_shared_key='MyInsecurePSK',
            ...    fqdn='london_branch@example.com',
            ...    comments='London Branch Office',
            ...    location_id='94963682')

        """

        payload = {
            "type": authentication_type,
            "preSharedKey": pre_shared_key,
        }

        # Add location ID to payload if specified.
        if kwargs.get("location_id"):
            payload["location"] = {"id": kwargs.pop("location_id")}

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        return self._post("vpnCredentials", json=payload)

    def bulk_delete_vpn_credentials(self, credential_ids: list):
        """
        Bulk delete VPN credentials.

        Args:
            credential_ids (list):
                List of credential IDs that will be deleted.

        Returns:
            :obj:`str`: Response code for operation.

        Examples:
            >>> zia.traffic.bulk_delete_vpn_credentials(['94963984', '97679232'])

        """

        payload = {"ids": credential_ids}

        return self._post(
            "vpnCredentials/bulkDelete", json=payload, box=False
        ).status_code

    def get_vpn_credential(self, credential_id: str = None, fqdn: str = None):
        """
        Get VPN credentials for the specified ID.

        Args:
            credential_id (str, optional):
                The unique identifier for the VPN credentials.
            fqdn (str, optional):
                The unique FQDN for the VPN credentials.

        Returns:
            :obj:`dict`: The resource record for the requested VPN credentials.

        Examples:
            >>> pprint(zia.traffic.get_vpn_credential('97679391'))

            >>> pprint(zia.traffic.get_vpn_credential(fqdn='userid@fqdn'))

        """
        if credential_id and fqdn:
            raise ValueError(
                "TOO MANY ARGUMENTS: Expected either a credential_id or an fqdn. Both were provided."
            )
        elif fqdn:
            credential = (
                record
                for record in self.list_vpn_credentials(search=fqdn)
                if record.fqdn == fqdn
            )
            return next(credential, None)

        return self._get(f"vpnCredentials/{credential_id}")

    def update_vpn_credential(self, credential_id: str, **kwargs):
        """
        Update VPN credentials with the specified ID.

        Args:
            credential_id (str):
                The unique identifier for the credential that will be updated.

        Keyword Args:
            pre_shared_key (str):
                Pre-shared key. This is a required field for UFQDN and IP auth type.
            comments (str):
                Additional information about this VPN credential.
            location_id (str):
                The unique identifier for an existing location.

        Returns:
            :obj:`dict`: The newly updated VPN credential resource record.

        Examples:
            Add a comment:

            >>> zia.traffic.update_vpn_credential('94963984',
            ...    comments='Adding a comment')

            Update the pre-shared key:

            >>> zia.traffic.update_vpn_credential('94963984',
            ...    pre_shared_key='MyNewInsecureKey',
            ...    comments='Pre-shared key rotated on 21 JUL 21')

        """

        # Cache the credential record
        credential_record = self.get_vpn_credential(credential_id)

        payload = {"type": credential_record.type}

        # Provide required params depending on the record type
        if credential_record.type == "IP":
            payload["ipAddress"] = credential_record.ipAddress
        elif credential_record.type == "UFQDN":
            payload["fqdn"] = credential_record.fqdn

        # Add location ID to payload if specified.
        if kwargs.get("location_id"):
            payload["location"] = {"id": kwargs.pop("location_id")}

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        return self._put(f"vpnCredentials/{credential_id}", json=payload)

    def delete_vpn_credential(self, credential_id: str):
        """
        Delete VPN credentials for the specified ID.

        Args:
            credential_id (str):
                The unique identifier for the VPN credentials that will be deleted.

        Returns:
            :obj:`str`: Response code for the operation.

        Examples:
            >>> zia.traffic.delete_vpn_credential('97679391')

        """
        return self._delete(f"vpnCredentials/{credential_id}", box=False).status_code
