from restfly.endpoint import APIEndpoint


class AppSegmentsAPI(APIEndpoint):

    def list(self):
        """Retrieve all configured application segments.

        Returns:
            :obj:`list`: List of application segments.

        Examples:
            >>> app_segments = zpa.app_segments.list()

        """
        return self._get('application').list

    def details(self, id: str):
        """Get information for an application segment.

        Args:
            id (str):
                The unique identifier for the application segment.

        Returns:
            :obj:`dict`: The application segment resource record.

        Examples:
            >>> app_segment = zpa.app_segments.details('234324234324')

        """
        return self._get(f'application/{id}')

    def delete(self, id: str):
        """Delete an application segment.

        Args:
            id (str):
                The unique identifier for the application segment.

        Returns:
            :obj:`str`: The operation response code.

        Examples:
            >>> zpa.app_segments.delete('234324234324')

        """
        return self._delete(f'application/{id}')

    def add(self, name: str, domain_names: list, segment_group_id: str, server_groups: list,
            tcp_ports=None, udp_ports=None, **kwargs):
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
            server_groups (:obj:`list` of :obj:`str`):
                The list of server group IDs that belong to this application segment.
            **kwargs:
                Optional params.

        Keyword Args:
            bypassType (str):
            clientlessApps (list):
            configSpace (str):
            defaultIdleTimeout (str):
            defaultMaxAge (str):
            description (str):
            doubleEncrypt (bool):
            enabled (bool):
            healthCheckType (str):
            healthReporting (str):
            ipAnchored (bool):
            isCnameEnabled (bool):
            passiveHealthEnabled (bool):

        Returns:
            :obj:`dict`: The newly created application segment resource record.

        Examples:
            Add a new application segment for example.com, ports 8080-8085.

            >>> zpa.app_segments.add('new_app_segment',
            ...    domain_names=['example.com'],
            ...    segment_group='232356567677776',
            ...    tcp_ports=['8080', '8085'],
            ...    server_groups=['234234234234324', '23121115151515'])

        """

        # Replace placeholders
        if udp_ports is None:
            udp_ports = []
        if tcp_ports is None:
            tcp_ports = []

        # Initialise payload
        payload = {
            'name': name,
            'domainNames': domain_names,
            'tcpPortRanges': tcp_ports,
            'udpPortRanges': udp_ports,
            'segmentGroupId': segment_group_id,
            'serverGroups': []
        }

        # Iterate through provided server group IDs and add to payload
        for server_group_id in server_groups:
            server_group = {
                'id': server_group_id
            }
            payload['serverGroups'].append(server_group)

        # Add optional params to payload
        for key, value in kwargs.items():
            payload[key] = value

        return self._post('application', json=payload)

    def update(self, id: str, domain_names: list, **kwargs):
        """Update an application segment.

        .. note:: The ZPA API requires domain names to be passed for all updates, even if they don't require modification.

        Args:
            id (str):
                The unique identifier for the application segment.
            domain_names (:obj:`list` of :obj:`str`):
                List of domain names or IP addresses for the application segment.
            **kwargs:
                Optional params.

        Keyword Args:
            bypassType (str):
            clientlessApps (list):
            configSpace (str):
            defaultIdleTimeout (str):
            defaultMaxAge (str):
            description (str):
            domainNames (list):
            doubleEncrypt (bool):
            enabled (bool):
            healthCheckType (str):
            healthReporting (str):
            ipAnchored (bool):
            isCnameEnabled (bool):
            name (str):
            passiveHealthEnabled (bool):
            segmentGroupId (str):
            serverGroups (list):
            tcpPortRanges (list):
            udpPortRanges (list):

        Returns:
            :obj:`dict`: The updated application segment resource record.

        Examples:
            Rename the application segment for example.com.

            >>> zpa.app_segments.update('2234234123234523',
            ...    name='new_app_name',
            ...    domain_names=['example.com'])

        """

        # Initialise payload
        payload = {
            'domainNames': domain_names
        }

        # Add optional params to payload
        for key, value in kwargs.items():
            payload[key] = value

        return self._put(f'application/{id}', json=payload)
