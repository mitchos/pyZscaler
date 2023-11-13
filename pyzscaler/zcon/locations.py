from box import Box, BoxList
from restfly import APIEndpoint

from pyzscaler.utils import convert_keys


class ZCONLocationsAPI(APIEndpoint):
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

                - ``NONE``
                - ``CORPORATE``
                - ``SERVER``
                - ``GUESTWIFI``
                - ``IOT``
                - ``WORKLOAD``
            page (int): The page number to return.
            page_size (int): The number of items to return per page.

        Returns:
            :obj:`BoxList`: The list of connector locations.

        Examples:
            List all locations::

                for location in zcon.locations.list_locations():
                    print(location)

            List only IOT locations::

                for location in zcon.locations.list_locations(location_type="IOT"):
                    print(location)

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
            Get details of a specific location::

                print(zcon.locations.get_location("123456789"))

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
            List all location templates::

                for template in zcon.locations.list_location_templates():
                    print(template)

        """
        return self._get("locationTemplate", params=kwargs)

    def get_location_template(self, template_id: str) -> Box:
        """
        Get details for a specific location template.

        Args:
            template_id (str): The ID of the location template to retrieve.

        Returns:
            :obj:`Box`: The location template details.

        Examples:
            Get details of a specific location template::

                print(zcon.locations.get_location_template("123456789"))

        """
        return self._get(f"locationTemplate/{template_id}")

    def add_location_template(self, name: str, template: dict = None, **kwargs) -> Box:
        """
        Add a new location template.

        Args:
            name (str): The name of the location template.
            template (dict, optional): A dictionary containing the template settings. Possible keys include:

                - ``template_prefix`` (str): Prefix of Cloud & Branch Connector location template.
                - ``xff_forward_enabled`` (bool): Enable to use the X-Forwarded-For headers.
                - ``auth_required`` (bool): Enable if "Authentication Required" is needed.
                - ``caution_enabled`` (bool): Enable to display an end user notification for unauthenticated traffic.
                - ``aup_enabled`` (bool): Enable to display an Acceptable Use Policy (AUP) for unauthenticated traffic.
                - ``aup_timeout_in_days`` (int): Frequency in days for displaying the AUP, if enabled.
                - ``ofw_enabled`` (bool): Enable the service's firewall controls.
                - ``ips_control`` (bool): Enable IPS controls, if firewall is enabled.
                - ``enforce_bandwidth_control`` (bool): Enable to specify bandwidth limits.
                - ``up_bandwidth`` (int): Upload bandwidth in Mbps, if bandwidth control is enabled.
                - ``dn_bandwidth`` (int): Download bandwidth in Mbps, if bandwidth control is enabled.
                - ``display_time_unit`` (str): Time unit for IP Surrogate idle time to disassociation.
                - ``idle_time_in_minutes`` (int): User mapping idle time in minutes for IP Surrogate.
                - ``surrogate_ip_enforced_for_known_browsers`` (bool): Enforce IP Surrogate for all known browsers.
                - ``surrogate_refresh_time_unit`` (str): Time unit for refresh time for re-validation of surrogacy.
                - ``surrogate_refresh_time_in_minutes`` (int): Refresh time in minutes for re-validation of surrogacy.
                - ``surrogate_ip`` (bool): Enable the IP Surrogate feature.

        Keyword Args:
            description (str): The description of the location template.

        Returns:
            :obj:`Box`: The location template details.

        Examples:
            Add a new location template with minimal settings::

                print(zcon.locations.add_location_template(name="MyTemplate"))

            Add a new location template with additional settings::

                template_settings = {
                    "surrogate_ip": True,
                    "surrogate_ip_enforced_for_known_browsers": False,
                    "template_prefix": "office",
                    "aup_enabled": True,
                    "aup_timeout_in_days": 30,
                    "ofw_enabled": True,
                    "idle_time_in_minutes": 35,
                    "auth_required": True,
                    "display_time_unit": "MINUTE",
                }
                print(zcon.locations.add_location_template(name="MyTemplate", template=template_settings))
        """
        # Rename 'description' to 'desc' if it exists
        if "description" in kwargs:
            kwargs["desc"] = kwargs.pop("description")

        payload = {"name": name, "template": template if template is not None else {}}

        # Add optional parameters to payload
        payload.update({k: v for k, v in kwargs.items() if v is not None})

        # Convert snake to camelcase
        payload = convert_keys(payload)

        return self._post("locationTemplate", json=payload)

    def update_location_template(self, template_id: str, **kwargs) -> Box:
        """
        Update an existing location template.

        Args:
            template_id (str): The ID of the location template to update.

        Keyword Args:
            name (str): The name of the location template.
            template (dict): A dictionary containing the template settings. Possible keys include:

                - ``template_prefix`` (str): Prefix of Cloud & Branch Connector location template.
                - ``xff_forward_enabled`` (bool): Enable to use the X-Forwarded-For headers.
                - ``auth_required`` (bool): Enable if "Authentication Required" is needed.
                - ``caution_enabled`` (bool): Enable to display an end user notification for unauthenticated traffic.
                - ``aup_enabled`` (bool): Enable to display an Acceptable Use Policy (AUP) for unauthenticated traffic.
                - ``aup_timeout_in_days`` (int): Frequency in days for displaying the AUP, if enabled.
                - ``ofw_enabled`` (bool): Enable the service's firewall controls.
                - ``ips_control`` (bool): Enable IPS controls, if firewall is enabled.
                - ``enforce_bandwidth_control`` (bool): Enable to specify bandwidth limits.
                - ``up_bandwidth`` (int): Upload bandwidth in Mbps, if bandwidth control is enabled.
                - ``dn_bandwidth`` (int): Download bandwidth in Mbps, if bandwidth control is enabled.
                - ``display_time_unit`` (str): Time unit for IP Surrogate idle time to disassociation.
                - ``idle_time_in_minutes`` (int): User mapping idle time in minutes for IP Surrogate.
                - ``surrogate_ip_enforced_for_known_browsers`` (bool): Enforce IP Surrogate for all known browsers.
                - ``surrogate_refresh_time_unit`` (str): Time unit for refresh time for re-validation of surrogacy.
                - ``surrogate_refresh_time_in_minutes`` (int): Refresh time in minutes for re-validation of surrogacy.
                - ``surrogate_ip`` (bool): Enable the IP Surrogate feature.
            description (str): A description for the location template.

        Returns:
            :obj:`Box`: The updated location template details.

        Note:
            - Any provided keys will update existing keys.
            - The template dictionary does not support partial updates. Any provided template will completely overwrite
                the existing template.

        Examples:
            Update the name of a location template::

                print(zcon.locations.update_location_template(template_id="123456789", name="MyTemplate"))

            Update the template details of a location template::

                template_settings = {
                    "surrogate_ip": True,
                    "surrogate_ip_enforced_for_known_browsers": False,
                    "template_prefix": "office",
                    "aup_enabled": True,
                    "aup_timeout_in_days": 30,
                    "ofw_enabled": True,
                    "idle_time_in_minutes": 4, # <-- changed to 4 hours
                    "auth_required": True,
                    "display_time_unit": "HOUR", # <-- changed from minutes to hours
                }
                print(zcon.locations.update_location_template(template_id="123456789", template=template_settings))
        """

        # Rename 'description' to 'desc' if it exists
        if "description" in kwargs:
            kwargs["desc"] = kwargs.pop("description")

        # Retrieve existing location template
        payload = self.get_location_template(template_id)

        # Merge all kwargs into payload
        payload.update(convert_keys(kwargs))

        return self._put(f"locationTemplate/{template_id}", json=payload)

    def delete_location_template(self, template_id: str):
        """
        Delete an existing location template.

        Args:
            template_id (str): The ID of the location template to delete.

        Returns:
            :obj:`int`: The status code of the operation.

        Examples:
            Delete a location template::

                print(zcon.locations.delete_location_template("123456789"))
        """
        return self._delete(f"locationTemplate/{template_id}").status_code
