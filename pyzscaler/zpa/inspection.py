from box import BoxList
from restfly.endpoint import APIEndpoint

from pyzscaler.utils import Iterator, snake_to_camel


class InspectionControllerAPI(APIEndpoint):
    def list_predef_controls_versions(self) -> BoxList:
        """
        Returns a list of Predefined Control versions

        Returns:
            :obj:`BoxList`: A list containing all Predefined Control versions.

        Examples:
            >>> for version in zpa.inspection.list_predef_controls_versions():
            ...    print(version)

        """
        return self._get("inspectionControls/predefined/versions")

    def list_predef_controls(self, version: str, **kwargs) -> BoxList:
        """
        Returns a list of ZPA Inspection Predefined Controls.

        Args:
            version (str): The version of the Predefined Controls to return.

        Keyword Args:
            search (str): The string used to search for Inspection Controls by features and fields.

        Returns:
            :obj:`BoxList`: A list containing all Predefined Controls that match the Version and Search string.

        Examples:
            Return all ZPA Inspection Controls for the given version.

            >>> for control in zpa.inspection.list_predefined_controls(version="OWASP_CRS/3.3.0")
            ...    print(control)

            Return ZPA Inspection Controls matching a search string.

            >>> for control in zpa.inspection.list_predefined_controls(search="", version="OWASP_CRS/3.3.0")
            ...    print(control)

        """
        payload = {
            "version": version,
        }

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        return self._get("inspectionControls/predefined", params=payload)

    def list_control_types(self) -> BoxList:
        """
        Returns a list of ZPA Inspection Custom Control Types.

        Returns:
            :obj:`BoxList`: A list containing ZPA Inspection Control Types

        Examples:

            >>> for control_type in zpa.inspection.list_control_types():
            ...    print(control_type)

        """
        return self._get("inspectionControls/controlTypes")

    def list_custom_http_methods(self) -> BoxList:
        """
        Returns a list of ZPA Custom Inspection Control HTTP Methods.

        Returns:
            :obj:`BoxList`: A list containing Custom Inspection Control HTTP Methods.

        Examples:
            >>> for method in zpa.inspection.list_custom_http_methods():
            ...    print(method)

        """
        return self._get("inspectionControls/custom/httpMethods")

    def list_custom_controls(self, **kwargs):
        """
        Returns a list of all ZPA Custom Inspection Controls.

        Args:
            **kwargs:

        Keyword Args:
            search (str): The string used to search for a custom control by features and fields.
            sortdir (str): Specifies the sorting order (ascending/descending) for the search results.
                Accepted values are:

                    - ASC
                    - DESC

        Returns:
            :obj:`BoxList`: A list containing all ZPA Custom Inspection Controls.

        Examples:


        """
        BoxList(Iterator(self._api, "inspectionControls/custom", **kwargs))

    def add_custom_control(self):

        payload = {}

        return self._post("inspectionControls/custom", json=payload)

    def list_control_severity_types(self):
        """
        Returns a list of Inspection Control Severity Types.

        Returns:
            :obj:`BoxList`: A list containing all valid Inspection Control Severity Types.
        """
        return self._get("inspectionControls/severityTypes")

    def list_custom_control_types(self):
        return self._get("inspectionControls/customControlTypes")

    def get_custom_control(self, control_id: str):
        return self._get(f"inspectionControls/custom/{control_id}")

    def update_custom_control(self, control_id: str):
        payload = {}
        return self._put(f"inspectionControls/custom/{control_id}", json=payload)

    def delete_custom_control(self, control_id: str):
        return self._delete(f"inspectionControls/custom/{control_id}")

    def get_control_action_types(self):
        return self._get("inspectionControls/actionTypes")

    def get_profile_by_control(self, control_id: str):
        """
        Returns the Inspection Profile name for the Inspection Control id specified.
        """
        return self._get(f"inspectionControls/predefined/{control_id}")

    def list_profiles(self, **kwargs) -> BoxList:
        return BoxList(Iterator(self._api, "inspectionProfile", **kwargs))

    def get_profile(self, profile_id: str):
        return self._get(f"inspectionProfile/{profile_id}")

    def add_profile(self, name: str, paranoia_level: int, predefined_controls_version: str, **kwargs):
        """
        Adds a ZPA Inspection Profile
        """

        # Inspection Profiles require the default predefined controls to be added. pyZscaler adds these in
        # automatically for our users.

        predef_controls = self.list_predefined_controls("OWASP_CRS/3.3.0")
        default_controls = []
        for group in predef_controls:
            if group.default_group:
                default_controls = group.predefined_inspection_controls

        payload = {
            "name": name,
            "paranoiaLevel": paranoia_level,
            "predefinedControls": default_controls,
            "predefinedControlsVersion": predefined_controls_version,
        }

        # Extend existing list of default predefined controls if the user supplies more
        if kwargs.get("predefined_controls"):
            payload["predefinedControls"].extend(kwargs.pop("predefined_controls"))

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        return self._post("inspectionProfile", json=payload)

    def update_profile(self, profile_id: str):
        payload = {}
        return self._put(f"inspectionProfile/{profile_id}")

    def delete_profile(self, profile_id: str):
        """
        Deletes the specified Inspection Profile.

        Args:
            profile_id (str): The unique id for the Inspection Profile that will be deleted.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            Delete an Inspection Profile with an id of *999999*.

            >>> zia.inspection.delete_profile('999999')

        """
        return self._delete(f"inspectionProfile/{profile_id}").status_code

    def update_profile_and_controls(self, profile_id: str):
        return self._patch(f"inspectionProfile/{profile_id}/patch")

    def profile_control_attach(self, profile_id: str, action: str):
        """
        Attaches or detaches all predefined Inspection Controls to an Inspection Profile.

        """
        if action == "attach":
            return self._put(f"inspectionProfile/{profile_id}/associateAllPredefinedControls")
        elif action == "detach":
            return self._put(f"inspectionProfile/{profile_id}/deAssociateAllPredefinedControls")
        else:
            raise ValueError("Unknown action provided. Valid actions are 'attach' or 'detach'.")
