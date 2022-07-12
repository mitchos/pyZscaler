from box import Box, BoxList
from restfly.endpoint import APIEndpoint

from pyzscaler.utils import Iterator, convert_keys, snake_to_camel


class InspectionControllerAPI(APIEndpoint):
    @staticmethod
    def _create_rule(rule: dict) -> dict:
        """
        Creates a rule template for the ZPA Inspection Control API when adding or updating a custom control.

        Args:
            rule (dict): Custom Control rule.

        Returns:
            :obj:`dict`: The Custom Control Rule template.

        """

        rule_set = {
            "names": rule["names"],
            "type": rule["type"],
            "conditions": [],
        }
        for condition in rule["conditions"]:
            rule_set["conditions"].append(
                {
                    "lhs": condition[0],
                    "op": condition[1],
                    "rhs": condition[2],
                }
            )

        return rule_set

    def add_custom_control(
        self,
        name: str,
        default_action: str,
        severity: str,
        type: str,
        rules: list,
        **kwargs,
    ) -> Box:
        """
        Adds a new ZPA Inspection Custom Control.

        Args:
            name (str):
                The name of the custom control.
            default_action (str):
                The default action to take for matches against this custom control. Valid options are:

                - ``PASS``
                - ``BLOCK``
                - ``REDIRECT``
            severity (str):
                The severity for events that match this custom control. Valid options are:

                - ``CRITICAL``
                - ``ERROR``
                - ``WARNING``
                - ``INFO``
            type (str):
                The type of HTTP message this control matches. Valid options are:

                - ``REQUEST``
                - ``RESPONSE``
            rules (list):
                A list of Inspection Control rule objects, with each object using the format::

                    {
                        "names": ["name1", "name2"],
                        "type": "rule_type",
                        "conditions": [
                            ("LHS", "OP", "RHS"),
                            ("LHS", "OP", "RHS"),
                        ],
                    }
            **kwargs: Optional keyword args.

        Keyword Args:
            **description (str):
                Additional information about the custom control.
            **paranoia_level (int):
                The paranoia level for the custom control.

        Returns:
            :obj:`Box`: The newly created custom Inspection Control resource record.

        Examples:
            Create a new custom Inspection Control with the minimum required parameters

            .. code-block:: python

                print(
                    zpa.inspection.add_custom_control(
                        "test8",
                        severity="INFO",
                        description="test descr",
                        paranoia_level="3",
                        type="REQUEST",
                        default_action="BLOCK",
                        rules=[
                            {
                                "names": ["test"],
                                "type": "REQUEST_HEADERS",
                                "conditions": [("SIZE", "GE", "10"), ("VALUE", "CONTAINS", "test")],
                            }
                        ],
                    )
                )

        """

        payload = {
            "name": name,
            "defaultAction": default_action,
            "severity": severity,
            "rules": [],
            "type": type,
        }

        # Use the create_rule method to restructure the Inspection Control rule and add to the payload.
        for rule in rules:
            payload["rules"].append(self._create_rule(rule))

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[key] = value

        # Convert snake to camelcase
        payload = convert_keys(payload)

        return self._post("inspectionControls/custom", json=payload)

    def add_profile(self, name: str, paranoia_level: int, predef_controls_version: str, **kwargs):
        """
        Adds a ZPA Inspection Profile.

        Args:
            name (str):
                The name of the Inspection Profile.
            paranoia_level (int):
                The paranoia level for the Inspection Profile.
            predef_controls_version (str):
                The version of the predefined controls that will be added.
            **kwargs:
                Additional keyword args.

        Keyword Args:
            **description (str):
                Additional information about the Inspection Profile.
            **custom_controls (list):
                A tuple list of custom controls to be added to the Inspection profile.

                Custom control tuples must follow the convention below:

                ``(control_id, action)``

                e.g.

                .. code-block:: python

                    custom_controls = [(99999, "BLOCK"), (88888, "PASS")]
            **predef_controls (list):
                A tuple list of predefined controls to be added to the Inspection profile.

                Predefined control tuples must follow the convention below:

                ``(control_id, action)``

                e.g.

                .. code-block:: python

                    predef_controls = [(77777, "BLOCK"), (66666, "PASS")]

        Returns:
            :obj:`Box`: The newly created Inspection Profile resource record.

        Examples:
            Add a new ZPA Inspection Profile with the minimum required parameters, printing the object to
            console after creation:

            .. code-block:: python

                print(
                    zpa.inspection.add_profile(
                        name="predefined_controls",
                        paranoia_level=3,
                        predef_controls_version="OWASP_CRS/3.3.0",
                    )
                )

            Add a new ZPA Inspection Profile that uses additional predefined controls and custom controls, printing the
            object to console after creation:

            .. code-block:: python

                print(
                    zpa.inspection.add_profile(
                        name="block_common_xss",
                        paranoia_level=2,
                        predefined_controls=[("99999", "BLOCK")],
                        predef_controls_version="OWASP_CRS/3.3.0",
                        custom_controls=[("88888", "BLOCK")],
                    )
                )

        """

        # Inspection Profiles require the default predefined controls to be added. pyZscaler adds these in
        # automatically for our users.

        predef_controls = self.list_predef_controls("OWASP_CRS/3.3.0")
        default_controls = []
        for group in predef_controls:
            if group.default_group:
                default_controls = group.predefined_inspection_controls

        payload = {
            "name": name,
            "paranoiaLevel": paranoia_level,
            "predefinedControls": default_controls,
            "predefinedControlsVersion": predef_controls_version,
        }

        # Extend existing list of default predefined controls if the user supplies more
        if kwargs.get("predef_controls"):
            controls = kwargs.pop("predef_controls")
            for control in controls:
                payload["predefinedControls"].append({"id": control[0], "action": control[1]})

        # Add custom controls if provided
        if kwargs.get("custom_controls"):
            controls = kwargs.pop("custom_controls")
            payload["customControls"] = [{"id": control[0], "action": control[1]} for control in controls]

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[key] = value

        payload = convert_keys(payload)

        return self._post("inspectionProfile", json=payload)

    def delete_custom_control(self, control_id: str) -> int:
        """
        Deletes the specified custom ZPA Inspection Control.

        Args:
            control_id (str):
                The unique id for the custom control that will be deleted.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            Delete a custom ZPA Inspection Control with an id of `99999`.

            .. code-block:: python

                zpa.inspection.delete_custom_control("99999")

        """
        return self._delete(f"inspectionControls/custom/{control_id}").status_code

    def delete_profile(self, profile_id: str):
        """
        Deletes the specified Inspection Profile.

        Args:
            profile_id (str):
                The unique id for the Inspection Profile that will be deleted.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            Delete an Inspection Profile with an id of *999999*:

            .. code-block:: python

                zpa.inspection.delete_profile("999999")

        """
        return self._delete(f"inspectionProfile/{profile_id}").status_code

    def get_custom_control(self, control_id: str) -> Box:
        """
        Returns the specified custom ZPA Inspection Control.

        Args:
            control_id (str):
                The unique id of the custom ZPA Inspection Control to be returned.

        Returns:
            :obj:`Box`: The custom ZPA Inspection Control resource record.

        Examples:
            Print the Custom Inspection Control with an id of `99999`:

            .. code-block:: python

                print(zpa.inspection.get_custom_control("99999"))

        """
        return self._get(f"inspectionControls/custom/{control_id}")

    def get_predef_control(self, control_id: str):
        """
        Returns the specified predefined ZPA Inspection Control.

        Args:
            control_id (str):
                The unique id of the predefined ZPA Inspection Control to be returned.

        Returns:
            :obj:`Box`: The ZPA Inspection Predefined Control resource record.

        Examples:
            Print the ZPA Inspection Predefined Control with an id of `99999`:

            .. code-block:: python

                print(zpa.inspection.get_predef_control("99999"))

        """
        return self._get(f"inspectionControls/predefined/{control_id}")

    def get_profile(self, profile_id: str) -> Box:
        """
        Returns the specified ZPA Inspection Profile.

        Args:
            profile_id (str):
                The unique id of the ZPA Inspection Profile

        Returns:
            :obj:`Box`: The specified ZPA Inspection Profile resource record.

        Examples:
            Print the ZPA Inspection Profile with an id of `99999`:

            .. code-block:: python

                print(zpa.inspection.get_profile("99999"))

        """
        return self._get(f"inspectionProfile/{profile_id}")

    def list_control_action_types(self) -> Box:
        """
        Returns a list of ZPA Inspection Control Action Types.

        Returns:
            :obj:`BoxList`: A list containing the ZPA Inspection Control Action Types.

        Examples:
            Iterate over the ZPA Inspection Control Action Types and print each one:

            .. code-block:: python

                for action_type in zpa.inspection.list_control_action_types():
                    print(action_type)

        """
        return self._get("inspectionControls/actionTypes")

    def list_control_severity_types(self) -> BoxList:
        """
        Returns a list of Inspection Control Severity Types.

        Returns:
            :obj:`BoxList`: A list containing all valid Inspection Control Severity Types.

        Examples:
            Print all Inspection Control Severity Types

            .. code-block:: python

                for severity in zpa.inspection.list_control_severity_types():
                    print(severity)

        """
        return self._get("inspectionControls/severityTypes")

    def list_control_types(self) -> BoxList:
        """
        Returns a list of ZPA Inspection Control Types.

        Returns:
            :obj:`BoxList`: A list containing ZPA Inspection Control Types.

        Examples:
            Print all ZPA Inspection Control Types:

            .. code-block:: python

                for control_type in zpa.inspection.list_control_types():
                    print(control_type)

        """
        return self._get("inspectionControls/controlTypes")

    def list_custom_control_types(self) -> BoxList:
        """
        Returns a list of custom ZPA Inspection Control Types.

        Returns:
            :obj:`BoxList`: A list containing custom ZPA Inspection Control Types.

        Examples:

            Print all custom ZPA Inspection Control Types

            .. code-block:: python

                for control_type in zpa.inspection.list_custom_control_types():
                    print(control_type)

        """
        return self._get("https://config.private.zscaler.com/mgmtconfig/v1/admin/inspectionControls/customControlTypes")

    def list_custom_controls(self, **kwargs) -> BoxList:
        """
        Returns a list of all custom ZPA Inspection Controls.

        Args:
            **kwargs: Optional keyword arguments.

        Keyword Args:
            **search (str):
                The string used to search for a custom control by features and fields.
            **sortdir (str):
                Specifies the sorting order for the search results.

                Accepted values are:

                - ``ASC`` - ascending order
                - ``DESC`` - descending order

        Returns:
            :obj:`BoxList`: A list containing all custom ZPA Inspection Controls.

        Examples:
            Print a list of all custom ZPA Inspection Controls:

            .. code-block:: python

                for control in zpa.inspection.list_custom_controls():
                    print(control)

        """
        return BoxList(Iterator(self._api, "inspectionControls/custom", **kwargs))

    def list_custom_http_methods(self) -> BoxList:
        """
        Returns a list of custom ZPA Inspection Control HTTP Methods.

        Returns:
            :obj:`BoxList`: A list containing custom ZPA Inspection Control HTTP Methods.

        Examples:

            Print all custom ZPA Inspection Control HTTP Methods:

            .. code-block:: python

                for method in zpa.inspection.list_custom_http_methods():
                    print(method)

        """
        return self._get("inspectionControls/custom/httpMethods")

    def list_predef_control_versions(self) -> BoxList:
        """
        Returns a list of predefined ZPA Inspection Control versions.

        Returns:
            :obj:`BoxList`: A list containing all predefined ZPA Inspection Control versions.

        Examples:
            Print all predefined ZPA Inspection Control versions::

                for version in zpa.inspection.list_predef_control_versions():
                    print(version)

        """
        return self._get("inspectionControls/predefined/versions")

    def list_predef_controls(self, version: str, **kwargs) -> BoxList:
        """
        Returns a list of predefined ZPA Inspection Controls.

        Args:
            version (str):
                The version of the predefined controls to return.
            **kwargs:
                Optional keyword args.

        Keyword Args:
            **search (str):
                The string used to search for predefined inspection controls by features and fields.

        Returns:
            :obj:`BoxList`: A list containing all predefined ZPA Inspection Controls that match the Version and Search
            string.

        Examples:
            Return all predefined ZPA Inspection Controls for the given version:

            .. code-block:: python

                for control in zpa.inspection.list_predef_controls(version="OWASP_CRS/3.3.0"):
                    print(control)

            Return predefined ZPA Inspection Controls matching a search string:

            .. code-block:: python

                for control in zpa.inspection.list_predef_controls(search="new_control", version="OWASP_CRS/3.3.0"):
                    print(control)

        """
        payload = {
            "version": version,
        }

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[key] = value

        # Convert snake to camelcase
        payload = convert_keys(payload)

        return self._get("inspectionControls/predefined", params=payload)

    def list_profiles(self, **kwargs) -> BoxList:
        """
        Returns the list of ZPA Inspection Profiles.

        Args:
            **kwargs:
                Optional keyword args.

        Keyword Args:
            **pagesize (int):
                Specifies the page size. The default size is 20 and the maximum size is 500.
            **search (str, optional):
                The search string used to match against features and fields.

        Returns:
            :obj:`BoxList`: The list of ZPA Inspection Profile resource records.

        Examples:
            Iterate over all ZPA Inspection Profiles and print them:

            .. code-block:: python

                for profile in zpa.inspection.list_profiles():
                    print(profile)

        """
        return BoxList(Iterator(self._api, "inspectionProfile", **kwargs))

    def profile_control_attach(self, profile_id: str, action: str, **kwargs) -> Box:
        """
        Attaches or detaches all predefined ZPA Inspection Controls to a ZPA Inspection Profile.

        Args:
            profile_id (str):
                The unique id for the ZPA Inspection Profile that will be modified.
            action (str):
                The association action that will be taken, accepted values are:

                * ``attach``: Attaches all predefined controls to the Inspection Profile with the specified version.
                * ``detach``: Detaches all predefined controls from the Inspection Profile.
            **kwargs:
                Additional keyword arguments.

        Keyword Args:
            profile_version (str):
                The version of the Predefined Controls to attach. Only required when using the
                attach action. Defaults to ``OWASP_CRS/3.3.0``.

        Returns:
            :obj:`Box`: The updated ZPA Inspection Profile resource record.

        Examples:
            Attach all predefined controls to a ZPA Inspection Profile with an id of 99999:

            .. code-block:: python

                updated_profile = zpa.inspection.profile_control_attach("99999", action="attach")

            Attach all predefined controls to a ZPA Inspection Profile with an id of 99999 and specified version:

            .. code-block:: python

                updated_profile = zpa.inspection.profile_control_attach(
                    "99999",
                    action="attach",
                    profile_version="OWASP_CRS/3.2.0",
                )

            Detach all predefined controls from a ZPA Inspection Profile with an id of 99999:

            .. code-block:: python

                updated_profile = zpa.inspection.profile_control_attach(
                    "99999",
                    action="detach",
                )

        Raises:
            ValueError: If an incorrect value is supplied for `action`.

        """
        if action == "attach":
            payload = {"version": kwargs.pop("profile_version", "OWASP_CRS/3.3.0")}
            resp = self._put(f"inspectionProfile/{profile_id}/associateAllPredefinedControls", params=payload)
            return self.get_profile(profile_id) if resp.status_code == 204 else resp.status_code
        elif action == "detach":
            resp = self._put(f"inspectionProfile/{profile_id}/deAssociateAllPredefinedControls")
            return self.get_profile(profile_id) if resp.status_code == 204 else resp.status_code
        else:
            raise ValueError("Unknown action provided. Valid actions are 'attach' or 'detach'.")

    def update_custom_control(self, control_id: str, **kwargs) -> Box:
        """
        Updates the specified custom ZPA Inspection Control.

        Args:
            control_id (str):
                The unique id for the custom control that will be updated.
            **kwargs:
                Optional keyword args.

        Keyword Args:
            **description (str):
                Additional information about the custom control.
            **default_action (str):
                The default action to take for matches against this custom control. Valid options are:

                - ``PASS``
                - ``BLOCK``
                - ``REDIRECT``
            **name (str):
                The name of the custom control.
            **paranoia_level (int):
                The paranoia level for the custom control.
            **rules (list):
                A list of Inspection Control rule objects, with each object using the format::

                    {
                        "names": ["name1", "name2"],
                        "type": "rule_type",
                        "conditions": [
                            ("LHS", "OP", "RHS"),
                            ("LHS", "OP", "RHS"),
                        ],
                    }
            **severity (str):
                The severity for events that match this custom control. Valid options are:

                - ``CRITICAL``
                - ``ERROR``
                - ``WARNING``
                - ``INFO``
            **type (str):
                The type of HTTP message this control matches. Valid options are:

                - ``REQUEST``
                - ``RESPONSE``

        Returns:
            :obj:`Box`: The updated custom ZPA Inspection Control resource record.

        Examples:
            Update the description of a custom ZPA Inspection Control with an id of 99999:

            .. code-block:: python

                print(
                    zpa.inspection.update_custom_control(
                        "99999",
                        description="Updated description",
                    )
                )

            Update the rules of a custom ZPA Inspection Control with an id of 88888:

            .. code-block:: python

                print(
                    zpa.inspection.update_custom_control(
                        "88888",
                        rules=[
                            {
                                "names": ["xforwardedfor_ge_20"],
                                "type": "REQUEST_HEADERS",
                                "conditions": [
                                    ("SIZE", "GE", "20"),
                                    ("VALUE", "CONTAINS", "X-Forwarded-For"),
                                ],
                            }
                        ],
                    )
                )


        """

        # Set payload to value of existing record and recursively convert nested dict keys from snake_case
        # to camelCase.
        payload = convert_keys(self.get_custom_control(control_id))

        # If the user provides rules for an update, clear the current rules then use the create_rule method to
        # restructure the Inspection Control rule and add to the payload.
        if kwargs.get("rules"):
            payload["rules"] = []
            for rule in kwargs.pop("rules"):
                payload["rules"].append(self._create_rule(rule))

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        resp = self._put(f"inspectionControls/custom/{control_id}", json=payload).status_code

        # Return the object if it was updated successfully
        if resp == 204:
            return self.get_custom_control(control_id)

    def update_profile(self, profile_id: str, **kwargs):
        """
        Updates the specified ZPA Inspection Profile.

        Args:
            profile_id (str):
                The unique id for the ZPA Inspection Profile that will be updated.
            predef_controls_version (str):
                The predefined controls version for the ZPA Inspection Profile. Defaults to `OWASP_CRS/3.3.0`.
            **kwargs:
                Optional keyword args.

        Keyword Args:
            **custom_controls (list):
                A tuple list of custom controls to be added to the Inspection profile.

                Custom control tuples must follow the convention below:

                ``(control_id, action)``

                e.g.

                .. code-block:: python

                    custom_controls = [(99999, "BLOCK"), (88888, "PASS")]
            **description (str):
                Additional information about the Inspection Profile.
            **name (str):
                The name of the Inspection Profile.
            **paranoia_level (int):
                The paranoia level for the Inspection Profile.
            **predef_controls (list):
                A tuple list of predefined controls to be added to the Inspection profile.

                Predefined control tuples must follow the convention below:

                ``(control_id, action)``

                e.g.

                .. code-block:: python

                    predef_controls = [(77777, "BLOCK"), (66666, "PASS")]
            **predef_controls_version (str):
                The version of the predefined controls that will be added.

        Returns:
            :obj:`Box`: The updated ZPA Inspection Profile resource record.

        Examples:
            Update the name and description of a ZPA Inspection Profile with the id 99999:

            .. code-block:: python

                print(
                    zpa.inspection.update_profile(
                        "99999",
                        name="inspect_common_predef_controls",
                        description="Inspects common controls from the Predefined set.",
                    )
                )

            Add a custom control to the ZPA Inspection Profile with the id 88888:

            .. code-block:: python

                print(
                    zpa.inspection.update_profile(
                        "88888",
                        custom_controls=[("2", "BLOCK")],
                    )
                )

        """
        # Set payload to value of existing record
        payload = self.get_profile(profile_id)
        payload["predefinedControlsVersion"] = kwargs.get("predef_controls_version", "OWASP_CRS/3.3.0")

        # Extend existing list of default predefined controls if the user supplies more
        if kwargs.get("predef_controls"):
            controls = kwargs.pop("predef_controls")
            for control in controls:
                payload["predefined_controls"] = [{"id": control[0], "action": control[1]} for control in controls]

        # Add custom controls if provided
        if kwargs.get("custom_controls"):
            controls = kwargs.pop("custom_controls")
            payload["custom_controls"] = [{"id": control[0], "action": control[1]} for control in controls]

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[key] = value

        # Convert from snake case to camel case
        payload = convert_keys(payload)

        resp = self._put(f"inspectionProfile/{profile_id}", json=payload).status_code

        # Return the object if it was updated successfully
        if resp == 204:
            return self.get_profile(profile_id)

    def update_profile_and_controls(self, profile_id: str, inspection_profile: dict, **kwargs):
        """
        Updates the inspection profile and controls for the specified ID.

        Note:
            This method has not been fully implemented and will not be maintained. There seems to be functionality
            duplication with the default Inspection Profile update API call. `**kwargs` has been provided as a parameter
            for you to be able to add any additional args that Zscaler may add.

            If you feel that this is in error and that this functionality should be correctly implemented by pyZscaler,
            `raise an issue <https://github.com/mitchos/pyZscaler/issues>`_ in the pyZscaler Github repo.

        Args:
            profile_id (str):
                The unique id of the inspection profile.
            inspection_profile (dict):
                The new inspection profile object.
            **kwargs:
                Additional keyword args.

        """

        payload = {
            "inspection_profile_id": profile_id,
            "inspection_profile": inspection_profile,
        }

        payload = convert_keys(payload)

        return self._patch(f"inspectionProfile/{profile_id}/patch", json=payload).status_code
