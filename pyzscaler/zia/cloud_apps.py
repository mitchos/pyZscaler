from restfly.endpoint import APIEndpoint

from pyzscaler.utils import convert_keys


class CloudAppsAPI(APIEndpoint):
    @staticmethod
    def _convert_ids_to_dict_list(id_list):
        """Helper function to convert a list of IDs into a list of dictionaries.

        Args:
            id_list (list): A list of IDs (str).

        Returns:
            list: A list of dictionaries, each with an 'id' key.
        """
        return [{"id": str(id)} for id in id_list]

    def bulk_update(self, sanction_state: str, **kwargs):
        """
        Updates application status and tag information for predefined or custom cloud applications based on the
        IDs specified.

        Args:
            sanction_state (str): The sanction state to apply to the cloud applications.

                Accepted values are:

                    ``sanctioned``: The cloud application is sanctioned.
                    ``unsanctioned``: The cloud application is unsanctioned.
                    ``any``: The cloud application is either sanctioned or unsanctioned.

            **kwargs:
                Optional keyword args

        Keyword Args:
            application_ids (list): A list of cloud application IDs to update.
            custom_tag_ids (list): A list of custom tag IDs to apply to the cloud applications.

        Returns:
            :obj:`dict`: The response from the ZIA API.

        Examples:
            Update the sanction state of a cloud application::

                zia.cloud_apps.bulk_update("sanctioned", application_ids=["12345"])

            Update the sanction state and custom tags of a cloud application::

                zia.cloud_apps.bulk_update("sanctioned", application_ids=["12345"], custom_tag_ids=["67890"])

        """
        # Mapping for user-friendly sanction state values to API-expected values
        sanction_state_mapping = {"sanctioned": "SANCTIONED", "unsanctioned": "UN_SANCTIONED", "any": "ANY"}

        # Convert user-friendly sanction state to ZIA API-expected value
        api_sanction_state = sanction_state_mapping.get(sanction_state.lower())
        if not api_sanction_state:
            raise ValueError(
                f"Invalid sanction state: {sanction_state}. Accepted values are 'sanctioned', 'unsanctioned', or 'any'."
            )

        payload = {"sanctionedState": api_sanction_state}

        # Process application_ids if provided in kwargs
        application_ids = kwargs.pop("application_ids", None)
        if application_ids is not None:
            payload["applicationIds"] = application_ids

        # Process custom_tag_ids if provided in kwargs
        custom_tag_ids = kwargs.pop("custom_tag_ids", None)
        if custom_tag_ids is not None:
            payload["customTags"] = self._convert_ids_to_dict_list(custom_tag_ids)

        return self._put("cloudApplications/bulkUpdate", json=payload).status_code

    def export_shadow_it_report(self, duration: str = "LAST_1_DAYS", **kwargs) -> str:
        """
        Export the Shadow IT Report (in CSV format) for the cloud applications recognized by Zscaler
        based on their usage in your organisation.

        Args:
            duration (str):
                Filters the data by using predefined time frames. Defaults to last day.

                Possible values: ``LAST_1_DAYS``, ``LAST_7_DAYS``, ``LAST_15_DAYS``, ``LAST_MONTH``, ``LAST_QUARTER``
            **kwargs:
                Arbitrary keyword arguments for filtering the report.

        Keyword Args:
            app_name (str): Filters the data based on the cloud application name that matches the specified string.
            order (dict):
                Sorts the list in increasing or decreasing order based on the specified attribute.

                Example format for this parameter:

                    ``order={"on": "RISK_SCORE", "by": "INCREASING"}``

                Possible values for ``on``:

                ``RISK_SCORE``, ``APPLICATION``, ``APPLICATION_CATEGORY``,
                ``SANCTIONED_STATE``, ``TOTAL_BYTES``, ``UPLOAD_BYTES``, ``DOWNLOAD_BYTES``, ``AUTHENTICATED_USERS``,
                ``TRANSACTION_COUNT``, ``UNAUTH_LOCATION``, ``LAST_ACCESSED``.

                Possible values for ``by``:

                ``INCREASING``, ``DECREASING``.
            application_category (str): Filters the data based on the cloud application category.

                Possible values: ``ANY``, ``NONE``, ``WEB_MAIL``, ``SOCIAL_NETWORKING``, ``STREAMING``, ``P2P``,
                ``INSTANT_MESSAGING``, ``WEB_SEARCH``, ``GENERAL_BROWSING``, ``ADMINISTRATION``, ``ENTERPRISE_COLLABORATION``,
                ``BUSINESS_PRODUCTIVITY``, ``SALES_AND_MARKETING``, ``SYSTEM_AND_DEVELOPMENT``, ``CONSUMER``, ``FILE_SHARE``,
                ``HOSTING_PROVIDER``, ``IT_SERVICES``, ``DNS_OVER_HTTPS``, ``HUMAN_RESOURCES``, ``LEGAL``, ``HEALTH_CARE``,
                ``FINANCE``, ``CUSTOM_CAPP``
            data_consumed (dict):
                Filters the data by cloud application usage in terms of total data uploaded and downloaded.

                Example format for this parameter:

                    data_consumed={"min": 100, "max": 1000}

                    ``min`` and ``max`` fields specify the range respectively.
            risk_index (int):
                Filters the data based on the risk index assigned to cloud applications.

                Possible values: ``1``, ``2``, ``3``, ``4``, ``5``
            sanctioned_state (str):
                Filters the data based on the status of cloud applications.

                Possible values: ``UN_SANCTIONED``, ``SANCTIONED``, ``ANY``
            employees (str):
                Filters the data based on the employee count of the cloud application vendor.

                Possible values: ``NONE``, ``RANGE_1_100``, ``RANGE_100_1000``, ``RANGE_1000_10000``,
                ``RANGE_10000_INF``
            supported_certifications (dict): Filters the cloud applications by security certifications.

                Example format for this parameter:

                    ``supported_certifications={"operation": "INCLUDE", "value": ["ISO_27001", "HIPAA"]}``

                Possible values for ``operation`` field: ``INCLUDE`` and ``EXCLUDE``.

                Possible values for ``value`` field: ``NONE``, ``CSA_STAR``, ``ISO_27001``, ``HIPAA``, ``FISMA``,
                ``FEDRAMP``, ``SOC2``, ``ISO_27018``, ``PCI_DSS``, ``ISO_27017``, ``SOC1``, ``SOC3``, ``GDPR``,
                ``CCPA``, ``FERPA``, ``COPPA``, ``HITECH``, ``EU_US_SWISS_PRIVACY_SHIELD``,
                ``EU_US_PRIVACY_SHIELD_FRAMEWORK``, ``CISP``, ``AICPA``, ``FIPS``, ``SAFE_BIOPHARMA``, ``ISAE_3000``,
                ``SSAE_18``, ``NIST``, ``ISO_14001``, ``SOC``, ``TRUSTE``, ``ISO_26262``, ``ISO_20252``, ``RGPD``,
                ``ISO_20243``, ``ISO_10002``, ``JIS_Q_15001_2017``, ``ISMAP``.
            source_ip_restriction (str):
                Filters the cloud applications based on whether they have source IP restrictions.

                Possible values: ``YES``, ``NO``, ``UNKNOWN``.
            mfa_support (str): Filters the cloud applications based on whether they support multi-factor authentication.

                Possible values: ``YES``, ``NO``, ``UNKNOWN``.
            admin_audit_logs (str): Filters the cloud applications based on whether they support admin audit logging.

                Possible values: ``YES``, ``NO``, ``UNKNOWN``.
            had_breach_in_last_3_years (str):
                Filters the cloud applications based on data breaches in the last three years.

                Possible values: ``YES``, ``NO``, ``UNKNOWN``.
            have_poor_items_of_service (str): Filters the cloud applications based on their terms of service.

                Possible values: ``YES``, ``NO``, ``UNKNOWN``.
            password_strength (str): Filters the cloud applications based on whether they require strong passwords.

                Possible values: ``YES``, ``NO``, ``UNKNOWN``.
            ssl_pinned (str): Filters the cloud applications based on whether they use SSL Pinning.

                Possible values: ``YES``, ``NO``, ``UNKNOWN``.
            evasive (str): Filters the cloud applications based on their capability to bypass traditional firewalls.

                Possible values: ``YES``, ``NO``, ``UNKNOWN``.
            have_http_security_header_support (str): Filters the cloud applications by the presence of security headers.

                Possible values: ``YES``, ``NO``, ``UNKNOWN``.
            dns_caa_policy (str): Filters the cloud applications by the presence of DNS CAA policy.

                Possible values: ``YES``, ``NO``, ``UNKNOWN``.
            have_weak_cipher_support (str): Filters the cloud applications based on the cryptographic keys used.

                Possible values: ``YES``, ``NO``, ``UNKNOWN``.
            ssl_certification_validity (str): Filters the cloud applications based on SSL certificate validity.

                Possible values: ``YES``, ``NO``, ``UNKNOWN``.
            file_sharing (str): Filters the cloud applications based on whether they include file-sharing provision.

                Possible values: ``YES``, ``NO``, ``UNKNOWN``.
            malware_scanning_content (str):
                Filters the cloud applications based on whether they include malware content.

                Possible values: ``YES``, ``NO``, ``UNKNOWN``.
            remote_access_screen_sharing (str):
                Filters the cloud applications based on whether they support remote access and screen sharing.

                Possible values: ``YES``, ``NO``, ``UNKNOWN``.
            sender_policy_framework (str):
                Filters the cloud applications based on whether they support Sender Policy Framework.

                Possible values: ``YES``, ``NO``, ``UNKNOWN``.
            domain_keys_identified_mail (str):
                Filters the cloud applications based on whether they support DomainKeys Identified Mail.

                Possible values: ``YES``, ``NO``, ``UNKNOWN``.
            domain_based_message_authentication (str):
                Filters the cloud applications based on whether they support Domain-based Message Authentication.

                Possible values: ``YES``, ``NO``, ``UNKNOWN``.
            vulnerable_disclosure_program (str):
                Filters the cloud applications based on whether they support Vulnerability Disclosure Policy.

                Possible values: ``YES``, ``NO``, ``UNKNOWN``.
            waf_support (str): Filters the cloud applications based on whether WAF is enabled for the applications.

                Possible values: ``YES``, ``NO``, ``UNKNOWN``.
            vulnerability (str):
                Filters the cloud applications based on whether they have published Common Vulnerabilities and
                Exposures (CVE).

                Possible values: ``YES``, ``NO``, ``UNKNOWN``.
            valid_ssl_certificate (str):
                Filters the cloud applications based on whether they have a valid SSL certificate.

                Possible values: ``YES``, ``NO``, ``UNKNOWN``.
            data_encryption_in_transit (str):
                Filters the cloud applications based on whether they support data encryption in transit.

                Possible values: ``YES``, ``NO``, ``UNKNOWN``.
            vulnerable_to_heart_bleed (str):
                Filters the cloud applications based on whether they are vulnerable to Heartbleed attack.

                Possible values: ``YES``, ``NO``, ``UNKNOWN``.
            vulnerable_to_poodle (str):
                Filters the cloud applications based on whether they are vulnerable to Poodle attack.

                Possible values: ``YES``, ``NO``, ``UNKNOWN``.
            vulnerable_to_log_jam (str):
                Filters the cloud applications based on whether they are vulnerable to Logjam attack.

                Possible values: ``YES``, ``NO``, ``UNKNOWN``.
            cert_key_size (dict):
                Filters the data by the size of the SSL certificate public keys used by the cloud applications.

                Example format for this parameter:

                    ``cert_key_size={"operation": "INCLUDE", "value": ["BITS_2048", "BITS_256"]}``

                Possible values for ``operation`` field:

                ``INCLUDE``, ``EXCLUDE``.

                Possible values for ``value`` field:

                ``NONE``, ``UN_KNOWN``, ``BITS_2048``, ``BITS_256``,
                ``BITS_3072``, ``BITS_384``, ``BITS_4096``, ``BITS_1024``.

        Returns:
            :obj:`str`: The Shadow IT Report in CSV format.

        Examples:
            Export the Shadow IT Report for the last 7 days::

                report = zia.shadow_it.export_shadow_it_report('LAST_7_DAYS')

        Notes:
            Zscaler has a rate limit of 1 report per-minute, ensure you take this into account when calling this method.

        """
        payload = {"duration": duration}
        convert_keys(payload.update(kwargs))

        return self._post("shadowIT/applications/export", json=payload).text

    def export_shadow_it_csv(self, application: str, entity: str, duration: str = "LAST_1_DAYS", **kwargs):
        """
        Export the Shadow IT Report (in CSV format) for the list of users or known locations
        identified with using the cloud applications specified in the request. The report
        includes details such as user interactions, application category, application usage,
        number of transactions, last accessed time, etc.

        You can customize the report using various filters.

        Args:
            application (str): The cloud application for which user or location data must be retrieved.
                Note: Only one cloud application can be specified at a time.
            duration (str): Filters the data using predefined timeframes. Defaults to last day.

            Possible values: ``LAST_1_DAYS``, ``LAST_7_DAYS``, ``LAST_15_DAYS``, ``LAST_MONTH``, ``LAST_QUARTER``.
            entity (str): The entity type that the Shadow IT Report will be generated for.

            Possible values: ``USER``, ``LOCATION``.

        Keyword Args:
            order (dict): Sorts the list in increasing or decreasing order based on the specified attribute.

                Example format for this parameter:

                    ``order={"on": "RISK_SCORE", "by": "INCREASING"}``

                Possible values for ``on``:

                ``RISK_SCORE``, ``APPLICATION``, ``APPLICATION_CATEGORY``,
                ``SANCTIONED_STATE``, ``TOTAL_BYTES``, ``UPLOAD_BYTES``, ``DOWNLOAD_BYTES``, ``AUTHENTICATED_USERS``,
                ``TRANSACTION_COUNT``, ``UNAUTH_LOCATION``, ``LAST_ACCESSED``.

                Possible values for ``by``:

                ``INCREASING``, ``DECREASING``.
            download_bytes (dict): Filters by the amount of data (in bytes) downloaded from the application.
                ``min`` and ``max`` fields specify the range.
            upload_bytes (dict): Filters by the amount of data (in bytes) uploaded to the application.
                ``min`` and ``max`` fields specify the range.
            data_consumed (dict): Filters by the total amount of data uploaded and downloaded from the application.
                ``min`` and ``max`` fields specify the range.
            users (dict): Filters by user.
                ``id`` and ``name`` fields specify the user information.
            locations (dict): Filters by location.
                ``id`` and ``name`` fields specify the location information.
            departments (dict): Filters by department.
                ``id`` and ``name`` fields specify the department information.

        Returns:
            :obj:`str`: The Shadow IT Report in CSV format.

        Examples:
            Export the Shadow IT Report for GitHub the last 15 days::

                report = zia.shadow_it.export_shadow_it_report(application="Github", duration="LAST_15_DAYS")

        Notes:
            Zscaler has a rate limit of 1 report per-minute, ensure you take this into account when calling this method.
        """

        payload = {"application": application, "duration": duration}

        # Process user_ids, location_ids, and department_ids if provided in kwargs
        for key in ["users", "locations", "departments"]:
            id_list = kwargs.pop(key, None)
            if id_list is not None:
                payload[key] = self._convert_ids_to_dict_list(id_list)

        convert_keys(payload.update(kwargs))

        return self._post(f"shadowIT/applications/{entity}/exportCsv", json=payload).text

    def list_apps(self):
        """
        List all predefined and custom cloud applications by name and id.

        Returns:
            :obj:`BoxList` of :obj:`Box`: A list of cloud applications.

        Examples:
            List all cloud applications::

                apps = zia.cloud_apps.list_apps()
                for app in apps:
                    print(app.name)

        """
        return self._get("cloudApplications/lite")

    def list_custom_tags(self):
        """
        List all custom tags by name and id.

        Returns:
            :obj:`BoxList` of :obj:`Box`: A list of custom tags available to assign to cloud applications.

        Examples:
            List all custom tags::

                tags = zia.cloud_apps.list_custom_tags()
                for tag in tags:
                    print(tag.name)

        """
        return self._get("customTags")
