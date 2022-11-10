from box import Box, BoxList
from restfly.endpoint import APIEndpoint

from pyzscaler.utils import Iterator, snake_to_camel


def simplify_key_type(key_type):
    # Simplify the key type for our users
    if key_type == "connector":
        return "CONNECTOR_GRP"
    elif key_type == "service_edge":
        return "SERVICE_EDGE_GRP"
    else:
        raise ValueError("Unexpected key type.")


class ProvisioningAPI(APIEndpoint):
    def list_provisioning_keys(self, key_type: str, **kwargs) -> BoxList:
        """
        Returns a list of all configured provisioning keys that match the specified ``key_type``.

        Args:
            key_type (str): The type of provisioning key, accepted values are:

                ``connector`` and ``service_edge``.
            **kwargs: Optional keyword args.

        Keyword Args:
            **max_items (int, optional):
                The maximum number of items to request before stopping iteration.
            **max_pages (int, optional):
                The maximum number of pages to request before stopping iteration.
            **pagesize (int, optional):
                Specifies the page size. The default size is 20, but the maximum size is 500.
            **search (str, optional):
                The search string used to match against features and fields.

        Returns:
            :obj:`BoxList`: A list containing the requested provisioning keys.

        Examples:
            List all App Connector provisioning keys.

            >>> for key in zpa.provisioning.list_provisioning_keys(key_type="connector"):
            ...    print(key)

            List all Service Edge provisioning keys.

            >>> for key in zpa.provisioning.list_provisioning_keys(key_type="service_edge"):
            ...    print(key)

        """

        return BoxList(Iterator(self._api, f"associationType/{simplify_key_type(key_type)}/provisioningKey", **kwargs))

    def get_provisioning_key(self, key_id: str, key_type: str) -> Box:
        """
        Returns information on the specified provisioning key.

        Args:
            key_id (str): The unique id of the provisioning key.
            key_type (str): The type of provisioning key, accepted values are:

                ``connector`` and ``service_edge``.

        Returns:
            :obj:`Box`: The requested provisioning key resource record.

        Examples:
            Get the specified App Connector key.

            >>> provisioning_key = zpa.provisioning.get_provisioning_key("999999",
            ...    key_type="connector")

            Get the specified Service Edge key.

            >>> provisioning_key = zpa.provisioning.get_provisioning_key("888888",
            ...    key_type="service_edge")

        """

        return self._get(f"associationType/{simplify_key_type(key_type)}/provisioningKey/{key_id}")

    def add_provisioning_key(
        self,
        key_type: str,
        name: str,
        max_usage: str,
        enrollment_cert_id: str,
        component_id: str,
        **kwargs,
    ) -> Box:
        """
        Adds a new provisioning key to ZPA.

        Args:
            key_type (str): The type of provisioning key, accepted values are:

                ``connector`` and ``service_edge``.
            name (str): The name of the provisioning key.
            max_usage (int): The maximum amount of times this key can be used.
            enrollment_cert_id (str):
                The unique id of the enrollment certificate that will be used for this provisioning key.
            component_id (str):
                The unique id of the component that this provisioning key will be linked to. For App Connectors, this
                will be the App Connector Group Id. For Service Edges, this will be the Service Edge Group Id.
            **kwargs: Optional keyword args.

        Keyword Args:
            enabled (bool): Enable the provisioning key. Defaults to ``True``.

        Returns:
            :obj:`Box`: The newly created Provisioning Key resource record.

        Examples:
            Add a new App Connector Provisioning Key that can be used a maximum of 2 times.

            >>> key = zpa.provisioning.add_provisioning_key(key_type="connector",
            ...    name="Example App Connector Provisioning Key",
            ...    max_usage=2,
            ...    enrollment_cert_id="99999",
            ...    component_id="888888")

            Add a new Service Edge Provisioning Key in the disabled state that can be used once.

            >>> key = zpa.provisioning.add_provisioning_key(key_type="service_edge",
            ...    name="Example Service Edge Provisioning Key",
            ...    max_usage=1,
            ...    enrollment_cert_id="99999",
            ...    component_id="777777"
            ...    enabled=False)

        """

        payload = {
            "name": name,
            "maxUsage": max_usage,
            "enrollmentCertId": enrollment_cert_id,
            "zcomponentId": component_id,
        }

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        return self._post(f"associationType/{simplify_key_type(key_type)}/provisioningKey", json=payload)

    def update_provisioning_key(self, key_id: str, key_type: str, **kwargs) -> Box:
        """
        Updates the specified provisioning key.

        Args:
            key_id (str): The unique id of the Provisioning Key being updated.
            key_type (str): The type of provisioning key, accepted values are:

                ``connector`` and ``service_edge``.
            **kwargs: Optional keyword args.

        Keyword Args:
            name (str): The name of the provisioning key.
            max_usage (int): The maximum amount of times this key can be used.
            enrollment_cert_id (str):
                The unique id of the enrollment certificate that will be used for this provisioning key.
            component_id (str):
                The unique id of the component that this provisioning key will be linked to. For App Connectors, this
                will be the App Connector Group Id. For Service Edges, this will be the Service Edge Group Id.

        Returns:
            :obj:`Box`: The updated Provisioning Key resource record.

        Examples:
            Update the name of an App Connector provisioning key:

            >>> updated_key = zpa.provisioning.update_provisioning_key('999999',
            ...    key_type="connector",
            ...    name="Updated Name")

            Change the max usage of a Service Edge provisioning key:

            >>> updated_key = zpa.provisioning.update_provisioning_key('888888',
            ...    key_type="service_edge",
            ...    max_usage=10)

        """

        # Get the provided provisioning key record
        payload = {snake_to_camel(k): v for k, v in self.get_provisioning_key(key_id, key_type=key_type).items()}

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        resp = self._put(f"associationType/{simplify_key_type(key_type)}/provisioningKey/{key_id}", json=payload).status_code

        if resp == 204:
            return self.get_provisioning_key(key_id, key_type=key_type)

    def delete_provisioning_key(self, key_id: str, key_type: str) -> int:
        """
        Deletes the specified provisioning key from ZPA.

        Args:
            key_id (str): The unique id of the provisioning key that will be deleted.
            key_type (str): The type of provisioning key, accepted values are:

                ``connector`` and ``service_edge``.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            Delete an App Connector provisioning key:

            >>> zpa.provisioning.delete_provisioning_key(key_id="999999",
            ...    key_type="connector")

            Delete a Service Edge provisioning key:

            >>> zpa.provisioning.delete_provisioning_key(key_id="888888",
            ...    key_type="service_edge")

        """

        return self._delete(f"associationType/{simplify_key_type(key_type)}/provisioningKey/{key_id}", box=False).status_code
