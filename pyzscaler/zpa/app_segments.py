from restfly.endpoint import APIEndpoint

from pyzscaler.utils import snake_to_camel, add_id_groups


class AppSegmentsAPI(APIEndpoint):
    # Params that need reformatting
    reformat_params = [
        ("clientless_app_ids", "clientlessApps"),
        ("server_group_ids", "serverGroups"),
    ]

    def list_segments(self):
        """
        Retrieve all configured application segments.

        Returns:
            :obj:`list`: List of application segments.

        Examples:
            >>> app_segments = zpa.app_segments.list_segments()

        """
        return self._get("application").list

    def get_segment(self, segment_id: str):
        """
        Get information for an application segment.

        Args:
            segment_id (str):
                The unique identifier for the application segment.

        Returns:
            :obj:`dict`: The application segment resource record.

        Examples:
            >>> app_segment = zpa.app_segments.details('234324234324')

        """
        return self._get(f"application/{segment_id}")

    def delete_segment(self, segment_id: str):
        """
        Delete an application segment.

        Args:
            segment_id (str):
                The unique identifier for the application segment.

        Returns:
            :obj:`str`: The operation response code.

        Examples:
            >>> zpa.app_segments.delete('234324234324')

        """
        return self._delete(f"application/{segment_id}")

    def add_segment(
        self,
        name: str,
        domain_names: list,
        segment_group_id: str,
        server_group_ids: list,
        tcp_ports: str = None,
        udp_ports: str = None,
        **kwargs,
    ):
        """Create an application segment.

        Args:
            segment_group_id (str):
                The unique identifer for the segment group this application segment belongs to.
            udp_ports (:obj:`list` of :obj:`str`):
                List of udp port range pairs, e.g. ['35000', '35000'] for port 35000.
            tcp_ports (:obj:`list` of :obj:`str`):
                List of tcp port range pairs, e.g. ['22', '22'] for port 22-22, ['80', '100'] for 80-100.
            domain_names (:obj:`list` of :obj:`str`):
                List of domain names or IP addresses for the application segment.
            name (str):
                The name of the application segment.
            server_group_ids (:obj:`list` of :obj:`str`):
                The list of server group IDs that belong to this application segment.
            **kwargs:
                Optional keyword args.

        Keyword Args:
            bypass_type (str):
                The type of bypass for the Application Segment. Accepted values are `ALWAYS`, `NEVER` and `ON_NET`.
            clientless_app_ids (:obj:`list`):
                List of unique IDs for clientless apps to associate with this Application Segment.
            config_space (str):
                The config space for this Application Segment. Accepted values are `DEFAULT` and `SIEM`.
            default_idle_timeout (int):
                The Default Idle Timeout for the Application Segment.
            default_max_age (int):
                The Default Max Age for the Application Segment.
            description (str):
                Additional information about this Application Segment.
            double_encrypt (bool):
                Double Encrypt the Application Segment micro-tunnel.
            enabled (bool):
                Enable the Application Segment.
            health_check_type (str):
                Set the Health Check Type. Accepted values are `DEFAULT` and `NONE`.
            health_reporting (str):
                Set the Health Reporting. Accepted values are `NONE`, `ON_ACCESS` and `CONTINUOUS`.
            ip_anchored (bool):
                Enable IP Anchoring for this Application Segment.
            is_cname_enabled (bool):
                Enable CNAMEs for this Application Segment.
            passive_health_enabled (bool):
                Enable Passive Health Checks for this Application Segment.

        Returns:
            :obj:`dict`: The newly created application segment resource record.

        Examples:
            Add a new application segment for example.com, ports 8080-8085.

            >>> zpa.app_segments.add_segment('new_app_segment',
            ...    domain_names=['example.com'],
            ...    segment_group_id='916196382959075421',
            ...    tcp_ports=['8080', '8085'],
            ...    server_group_ids=['234234234234324', '23121115151515'])

        """

        # Initialise payload
        payload = {
            "name": name,
            "domainNames": domain_names,
            "tcpPortRanges": tcp_ports,
            "udpPortRanges": udp_ports,
            "segmentGroupId": segment_group_id,
            "serverGroups": [{"id": group_id} for group_id in server_group_ids],
        }

        add_id_groups(self.reformat_params, kwargs, payload)

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        return self._post("application", json=payload)

    def update_segment(self, segment_id: str, **kwargs):
        """
        Update an application segment.

        Args:
            segment_id (str):
                The unique identifier for the application segment.
            **kwargs:
                Optional params.

        Keyword Args:
            bypass_type (str):
                The type of bypass for the Application Segment. Accepted values are `ALWAYS`, `NEVER` and `ON_NET`.
            clientless_app_ids (:obj:`list`):
                List of unique IDs for clientless apps to associate with this Application Segment.
            config_space (str):
                The config space for this Application Segment. Accepted values are `DEFAULT` and `SIEM`.
            default_idle_timeout (int):
                The Default Idle Timeout for the Application Segment.
            default_max_age (int):
                The Default Max Age for the Application Segment.
            description (str):
                Additional information about this Application Segment.
            domain_names (:obj:`list` of :obj:`str`):
                List of domain names or IP addresses for the application segment.
            double_encrypt (bool):
                Double Encrypt the Application Segment micro-tunnel.
            enabled (bool):
                Enable the Application Segment.
            health_check_type (str):
                Set the Health Check Type. Accepted values are `DEFAULT` and `NONE`.
            health_reporting (str):
                Set the Health Reporting. Accepted values are `NONE`, `ON_ACCESS` and `CONTINUOUS`.
            ip_anchored (bool):
                Enable IP Anchoring for this Application Segment.
            is_cname_enabled (bool):
                Enable CNAMEs for this Application Segment.
            name (str):
                The name of the application segment.
            passive_health_enabled (bool):
                Enable Passive Health Checks for this Application Segment.
            segment_group_id (str):
                The unique identifer for the segment group this application segment belongs to.
            server_group_ids (:obj:`list` of :obj:`str`):
                The list of server group IDs that belong to this application segment.
            tcp_ports (:obj:`list` of :obj:`str`):
                List of tcp port range pairs, e.g. ['22', '22'] for port 22-22, ['80', '100'] for 80-100.
            udp_ports (:obj:`list` of :obj:`str`):
                List of udp port range pairs, e.g. ['35000', '35000'] for port 35000.

        Returns:
            :obj:`dict`: The updated application segment resource record.

        Examples:
            Rename the application segment for example.com.

            >>> zpa.app_segments.update('2234234123234523',
            ...    name='new_app_name',

        """

        # Set payload to value of existing record
        payload = {
            snake_to_camel(k): v for k, v in self.get_segment(segment_id).items()
        }

        add_id_groups(self.reformat_params, kwargs, payload)

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        return self._put(f"application/{segment_id}", json=payload)
