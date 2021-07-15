from restfly.endpoint import APIEndpoint


class SegmentGroupsAPI(APIEndpoint):

    def list_groups(self):
        """
        Returns a list of all configured segment groups.

        Returns:
            :obj:`list`: A list of all configured segment groups.

        Examples:
            >>> for segment_group in zpa.segment_groups.list_groups():
            ...    pprint(segment_group)

        """
        return self._get('segmentGroup').list

    def get_group(self, group_id: str):
        """
        Returns information on the specified segment group.

        Args:
            group_id (str):
                The unique identifier for the segment group.

        Returns:
            :obj:`dict`: The resource record for the segment group.

        Examples:
            >>> pprint(zpa.segment_groups.get_group('2342342342344433'))

        """

        return self._get(f'segmentGroup/{group_id}')

    def delete_group(self, group_id: str):
        """
        Deletes the specified segment group.

        Args:
            group_id (str):
                The unique identifier for the segment group to be deleted.

        Returns:
            :obj:`str`: The response code for the operation.

        Examples:
            >>> zpa.segment_groups.delete_group('2342342342343')

        """
        return self._delete(f'segmentGroup/{group_id}')

    def add_group(self, name: str, enabled=False, **kwargs):
        """
        Adds a new segment group.

        Args:
            name (str):
                The name of the new segment group.
            enabled (bool):
                Enable the segment group. Defaults to False.
            **kwargs:

        Keyword Args:
            applications (:obj:`list` of :obj:`dict`):
                Define an application object for the segment group.
            configSpace (str):
                The config space for the segment group. Can either be DEFAULT or SIEM.
            description (str):
                A description for the segment group.
            policyMigrated (bool):

        Returns:
            :obj:`dict`: The resource record for the newly created segment group.

        Examples:
            Creating a segment group with the minimum required parameters:

            >>> zpa.segment_groups.add_group('new_segment_group',
            ...    True)

        """
        payload = {
            'name': name,
            'enabled': enabled,
        }
        # Add optional params to payload
        for key, value in kwargs.items():
            payload[key] = value

        return self._post('segmentGroup', json=payload)

    def update_group(self, group_id: str, **kwargs):
        """
        Updates an existing segment group.

        Args:
            group_id (str):
                The unique identifier for the segment group to be updated.
            **kwargs:

        Keyword Args:
            name (str):
                The name of the new segment group.
            enabled (bool):
                Enable the segment group.
            applications (:obj:`list` of :obj:`dict`):
                Define an application object for the segment group.
            configSpace (str):
                The config space for the segment group. Can either be DEFAULT or SIEM.
            description (str):
                A description for the segment group.
            policyMigrated (bool):

        Returns:
            :obj:`dict`: The resource record for the updated segment group.

        Examples:
            Updating the name of a segment group:

            >>> zpa.segment_groups.update_group('23234234324234',
            ...    name='updated_name')

        """
        payload = {
            'id': group_id,
        }
        # Add optional params to payload
        for key, value in kwargs.items():
            payload[key] = value

        return self._put(f'segmentGroup/{group_id}', json=payload)
