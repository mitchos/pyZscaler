from box import Box, BoxList
from restfly import APISession
from restfly.endpoint import APIEndpoint

from pyzscaler.utils import Iterator, convert_keys, keys_exists, snake_to_camel


class LSSConfigControllerAPI(APIEndpoint):
    source_log_map = {
        "app_connector_metrics": "zpn_ast_comprehensive_stats",
        "app_connector_status": "zpn_ast_auth_log",
        "audit_logs": "zpn_audit_log",
        "browser_access": "zpn_http_trans_log",
        "private_svc_edge_status": "zpn_sys_auth_log",
        "user_activity": "zpn_trans_log",
        "user_status": "zpn_auth_log",
        "web_inspection": "zpn_waf_http_exchanges_log",
    }

    def __init__(self, api: APISession):
        super().__init__(api)

        self.v2_url = api.v2_url
        self.v2_admin_url = "https://config.private.zscaler.com/mgmtconfig/v2/admin/lssConfig"

    def _create_policy(self, conditions: list) -> list:
        """
        Creates a dict template for feeding conditions into the ZPA Policies API when adding or updating a policy.

        Args:
            conditions (list): List of condition tuples.

        Returns:
            :obj:`dict`: Dictionary containing the LSS Log Receiver Policy conditions template.

        """

        template = []

        for condition in conditions:
            # Template for SAML Policy Rule objects
            if isinstance(condition, tuple) and len(condition) == 2 and condition[0] == "saml":
                operand = {"operands": [{"objectType": "SAML", "entryValues": []}]}
                for item in condition[1]:
                    entry_values = {
                        "lhs": item[0],
                        "rhs": item[1],
                    }
                    operand["operands"][0]["entryValues"].append(entry_values)
            # Template for client_type Policy Rule objects
            elif condition[0] == "client_type":
                operand = {
                    "operands": [
                        {
                            "objectType": condition[0].upper(),
                            "values": [self.get_client_types()[item] for item in condition[1]],
                        }
                    ]
                }
            # Template for all other object types
            else:
                operand = {
                    "operands": [
                        {
                            "objectType": condition[0].upper(),
                            "values": condition[1],
                        }
                    ]
                }
            template.append(operand)

        return template

    def get_client_types(self) -> Box:
        """
        Returns all available LSS Client Types.

        Client Types are used when creating LSS Receiver configs. ZPA uses an internal code for Client Types, e.g.
        ``zpn_client_type_ip_anchoring`` is the Client Type for a ZIA Service Edge. pyZscaler inverts the key/value so
        that you can perform a lookup using a human-readable name in your code (e.g. ``cloud_connector``).

        Returns:
            :obj:`Box`: Dictionary containing all LSS Client Types with human-readable name as the key.

        Examples:
            Print all LSS Client Types:

            >>> print(zpa.lss.get_client_types())

        """
        # ZPA returns a dictionary of client types but the keys are the internal ZPA codes, which our users probably
        # won't know. This method reverses the dictionary, converts the 'normalised' Client Type name to snake_case
        # before returning it so that a lookup can be easily performed using the Client Type name in plain english.
        #
        # Example before:
        # {'zpn_client_type_exporter': 'Web Browser'}
        # Example after:
        # {'web_browser': 'zpn_client_type_exporter'}

        resp = self._get(f"{self.v2_admin_url}/clientTypes")
        reverse_map = {v.lower().replace(" ", "_"): k for k, v in resp.items()}
        return Box(reverse_map)

    def list_configs(self, **kwargs) -> BoxList:
        """
        Returns all configured LSS receivers.

        Keyword Args:
            **max_items (int):
                The maximum number of items to request before stopping iteration.
            **max_pages (int):
                The maximum number of pages to request before stopping iteration.
            **pagesize (int):
                Specifies the page size. The default size is 20, but the maximum size is 500.
            **search (str, optional):
                The search string used to match against features and fields.

        Returns:
            :obj:`BoxList`: List of all configured LSS receivers.

        Examples:
            Print all configured LSS Receivers.

            >>> for lss_config in zpa.lss.list_configs():
            ...    print(config)
        """
        return BoxList(Iterator(self._api, f"{self.v2_url}/lssConfig", **kwargs))

    def get_config(self, lss_id: str) -> Box:
        """
        Returns information on the specified LSS Receiver config.

        Args:
            lss_id (str):
                The unique identifier for the LSS Receiver config.

        Returns:
            :obj:`Box`: The resource record for the LSS Receiver config.

        Examples:
            Print information on the specified LSS Receiver config.

            >>> print(zpa.lss.get_config('99999'))

        """
        return self._get(f"{self.v2_url}/lssConfig/{lss_id}")

    def get_log_formats(self) -> Box:
        """
        Returns all available pre-configured LSS Log Formats.

        LSS Log Formats are provided as either CSV, JSON or TSV. LSS Log Format values can be used when
        creating or updating LSS Log Receiver configs.

        Returns:
            :obj:`Box`: Dictionary containing pre-configured LSS Log Formats.

        Examples:
            >>> for item in zpa.lss.get_log_formats():
            ...    print(item)

        """
        return self._get(f"{self.v2_admin_url}/logType/formats")

    def get_status_codes(self, log_type: str = "all") -> Box:
        """
        Returns a list of LSS Session Status Codes.

        The LSS Session Status codes are used to filter the messages received by LSS. LSS Session Status Codes can be
        used when adding or updating the filters for an LSS Log Receiver.

        Args:
            log_type (str):
                Filter the LSS Session Status Codes by Log Type, accepted values are:

                - ``all``
                - ``app_connector_status``
                - ``private_svc_edge_status``
                - ``user_activity``
                - ``user_status``

                `Defaults to all.`

        Returns:
            :obj:`Box`: Dictionary containing all LSS Session Status Codes.

        Examples:
            Print all LSS Session Status Codes.

            >>> for item in zpa.lss.get_status_codes():
            ...    print(item)

            Print LSS Session Status Codes for `User Activity` log types.

            >>> for item in zpa.lss.get_status_codes(log_type="user_activity"):
            ...    print(item)

        """
        if log_type == "all":
            return self._get(f"{self.v2_admin_url}/statusCodes")
        elif log_type in ["user_activity", "user_status", "private_svc_edge_status", "app_connector_status"]:
            return self._get(f"{self.v2_admin_url}/statusCodes")[self.source_log_map[log_type]]
        else:
            raise ValueError("Incorrect log_type provided.")

    def add_lss_config(
        self,
        lss_host: str,
        lss_port: str,
        name: str,
        source_log_type: str,
        app_connector_group_ids: list = None,
        enabled: bool = True,
        source_log_format: str = "csv",
        use_tls: bool = False,
        **kwargs,
    ) -> Box:
        """
        Adds a new LSS Receiver Config to ZPA.

        Args:
            app_connector_group_ids (list): A list of unique IDs for the App Connector Groups associated with this
                LSS Config. `Defaults to None.`
            enabled (bool): Enable the LSS Receiver. `Defaults to True`.
            lss_host (str): The IP address of the LSS Receiver.
            lss_port (str): The port number for the LSS Receiver.
            name (str): The name of the LSS Config.
            source_log_format (str):
                The format for the logs. Must be one of the following options:

                - ``csv`` - send logs in CSV format
                - ``json`` - send logs in JSON format
                - ``tsv`` - send logs in TSV format

                `Defaults to csv.`
            source_log_type (str):
                The type of logs that will be sent to the receiver as part of this config. Must be one of the following
                options:

                - ``app_connector_metrics``
                - ``app_connector_status``
                - ``audit_logs``
                - ``browser_access``
                - ``private_svc_edge_status``
                - ``user_activity``
                - ``user_status``
            use_tls (bool):
                Enable to use TLS on the log traffic between LSS components. `Defaults to False.`

        Keyword Args:
            description (str):
                Additional information about the LSS Config.
            filter_status_codes (list):
                A list of Session Status Codes that will be excluded by LSS.
            log_stream_content (str):
                Formatter for the log stream content that will be sent to the LSS Host. Only pass this parameter if you
                intend on using custom log stream content.
            policy_rules (list):
                A list of policy rule tuples. Tuples must follow the convention:

                 (`object_type`, [`object_id`]).

                E.g.

                .. code-block:: python

                    ('app_segment_ids', ['11111', '22222']),
                    ('segment_group_ids', ['88888']),
                    ('idp_ids', ['99999']),
                    ('client_type', ['zia_service_edge'])
                    ('saml', [('33333', 'value')])

        Returns:
            :obj:`Box`: The newly created LSS Config resource record.

        Examples:

            Add an LSS Receiver config that receives App Connector Metrics logs.

            .. code-block:: python

                zpa.lss.add_config(
                    app_connector_group_ids=["app_conn_group_id"],
                    lss_host="192.0.2.100,
                    lss_port="8080",
                    name="app_con_metrics_to_siem",
                    source_log_type="app_connector_metrics")

            Add an LSS Receiver config that receives User Activity logs.

            .. code-block:: python

                zpa.lss.add_config(
                    app_connector_group_ids=["app_conn_group_id"],
                    lss_host="192.0.2.100,
                    lss_port="8080",
                    name="user_activity_to_siem",
                    policy_rules=[
                        ("idp", ["idp_id"]),
                        ("app", ["app_seg_id"]),
                        ("app_group", ["app_seg_group_id"]),
                        ("saml", [("saml_attr_id", "saml_attr_value")]),
                    ],
                    source_log_type="user_activity")

            Add an LSS Receiver config that receives User Status logs.

            .. code-block:: python

                zpa.lss.add_config(
                    app_connector_group_ids=["app_conn_group_id"],
                    lss_host="192.0.2.100,
                    lss_port="8080",
                    name="user_activity_to_siem",
                    policy_rules=[
                        ("idp", ["idp_id"]),
                        ("client_type", ["web_browser", "client_connector"]),
                        ("saml", [("attribute_id", "test3")]),
                    ],
                    source_log_type="user_status")

        """
        source_log_type = self.source_log_map[source_log_type]

        # If the user has supplied custom log stream content formatting then we'll use that. Otherwise map the log
        # type to internal ZPA log codes and get the preformatted log stream content formatting directly from ZPA.
        if kwargs.get("log_stream_content"):
            log_stream_content = kwargs.pop("log_stream_content")
        else:
            log_stream_content = self.get_log_formats()[source_log_type][source_log_format]

        payload = {
            "config": {
                "enabled": enabled,
                "lssHost": lss_host,
                "lssPort": lss_port,
                "name": name,
                "format": log_stream_content,
                "sourceLogType": source_log_type,
                "useTls": use_tls,
            },
            "connectorGroups": [{"id": group_id} for group_id in app_connector_group_ids],
        }

        # Convert tuple list to dict and add to payload
        if kwargs.get("policy_rules"):
            payload["policyRuleResource"] = {
                "conditions": self._create_policy(kwargs.pop("policy_rules")),
                "name": kwargs.get("policy_name", "placeholder"),
            }

        # Add Session Status Codes to filter if provided
        if kwargs.get("filter_status_codes"):
            payload["config"]["filter"] = kwargs.pop("filter_status_codes")

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        # return payload
        return self._post(f"{self.v2_url}/lssConfig", json=payload)

    def update_lss_config(self, lss_config_id: str, **kwargs):
        """
        Update the LSS Receiver Config.

        Args:
            lss_config_id (str): The unique id for the LSS Receiver config.
            **kwargs: Optional keyword args.

        Keyword Args:
            description (str):
                Additional information about the LSS Config.
            enabled (bool):
                Enable the LSS host. Defaults to ``True``.
            filter_status_codes (list):
                A list of Session Status Codes that will be excluded by LSS. If you would like to filter all error codes
                then pass the string "all".
            log_stream_content (str):
                Formatter for the log stream content that will be sent to the LSS Host.
            policy_rules (list):
                A list of policy rule tuples. Tuples must follow the convention:

                 (`object_type`, [`object_id`]).

                E.g.

                .. code-block:: python

                    ('app_segment_ids', ['11111', '22222']),
                    ('segment_group_ids', ['88888']),
                    ('idp_ids', ['99999']),
                    ('client_type', ['zpn_client_type_exporter'])
                    ('saml_attributes', [('33333', 'value')])
            source_log_format (str):
                The format for the logs. Must be one of the following options:

                - ``csv`` - send logs in CSV format
                - ``json`` - send logs in JSON format
                - ``tsv`` - send logs in TSV format
            source_log_type (str):
                The type of logs that will be sent to the receiver as part of this config. Must be one of the following
                options:

                - ``app_connector_metrics``
                - ``app_connector_status``
                - ``audit_logs``
                - ``browser_access``
                - ``private_svc_edge_status``
                - ``user_activity``
                - ``user_status``
            use_tls (bool):
                Enable to use TLS on the log traffic between LSS components. Defaults to ``False``.

        Examples:

            Update an LSS Log Receiver config to change from user activity to user status.

            Note that the ``policy_rules`` will need to be modified to be compatible with the chosen
            ``source_log_type``.

            .. code-block:: python

                zpa.lss.update_config(
                    name="user_status_to_siem",
                    policy_rules=[
                        ("idp", ["idp_id"]),
                        ("client_type", ["machine_tunnel"]),
                        ("saml", [("attribute_id", "11111")]),
                    ],
                    source_log_type="user_status")


        """

        # Set payload to value of existing record
        payload = convert_keys(self.get_config(lss_config_id))

        # If the user has supplied custom log stream content formatting then we'll use that. Otherwise, map the log
        # type to internal ZPA log codes and get the preformatted log stream content formatting directly from ZPA.
        if kwargs.get("log_stream_content"):
            payload["config"]["format"] = kwargs.pop("log_stream_content")
        elif kwargs.get("source_log_type"):
            source_log_type = self.source_log_map[kwargs.pop("source_log_type")]
            payload["config"]["sourceLogType"] = source_log_type
            payload["config"]["format"] = self.get_log_formats()[source_log_type][kwargs.pop("source_log_format", "csv")]

        # Iterate kwargs and update payload for keys that we've renamed.
        for k in list(kwargs):
            if k in ["name", "lss_host", "lss_port", "enabled", "use_tls"]:
                payload["config"][snake_to_camel(k)] = kwargs.pop(k)
            elif k == "filter_status_codes":
                payload["config"]["filter"] = kwargs.pop(k)

        # Convert tuple list to dict and add to payload
        if kwargs.get("policy_rules"):
            if keys_exists(payload, "policyRuleResource", "name"):
                policy_name = payload["policyRuleResource"]["name"]
            else:
                policy_name = "placeholder"
            payload["policyRuleResource"] = {
                "conditions": self._create_policy(kwargs.pop("policy_rules")),
                "name": kwargs.pop("policy_name", policy_name),
            }

        # Add additional provided parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        resp = self._put(f"{self.v2_url}/lssConfig/{lss_config_id}", json=payload).status_code

        if resp == 204:
            return self.get_config(lss_config_id)

    def delete_lss_config(self, lss_id: str) -> int:
        """
        Delete the specified LSS Receiver Config.

        Args:
            lss_id (str): The unique identifier for the LSS Receiver Config to be deleted.

        Returns:
            :obj:`int`:
                The response code for the operation.

        Examples:
            Delete an LSS Receiver config.

            >>> zpa.lss.delete_config('99999')

        """
        return self._delete(f"{self.v2_url}/lssConfig/{lss_id}").status_code
