from restfly.endpoint import APIEndpoint

from pyzscaler.utils import convert_keys


class ReportsAPI(APIEndpoint):
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

                Possible values for ``on`` field: ``RISK_SCORE``, ``APPLICATION``, ``APPLICATION_CATEGORY``,
                ``SANCTIONED_STATE``, ``TOTAL_BYTES``, ``UPLOAD_BYTES``, ``DOWNLOAD_BYTES``, ``AUTHENTICATED_USERS``,
                ``TRANSACTION_COUNT``, ``UNAUTH_LOCATION``, ``LAST_ACCESSED``
                Possible values for ``by`` field:``INCREASING``, ``DECREASING``
            application_category (str): Filters the data based on the cloud application category.

                Possible values: ``ANY``, ``NONE``, ``WEB_MAIL``, ``SOCIAL_NETWORKING``, ``STREAMING``, ``P2P``,
                ``INSTANT_MESSAGING``, ``WEB_SEARCH``, ``GENERAL_BROWSING``, ``ADMINISTRATION``, ``ENTERPRISE_COLLABORATION``,
                ``BUSINESS_PRODUCTIVITY``, ``SALES_AND_MARKETING``, ``SYSTEM_AND_DEVELOPMENT``, ``CONSUMER``, ``FILE_SHARE``,
                ``HOSTING_PROVIDER``, ``IT_SERVICES``, ``DNS_OVER_HTTPS``, ``HUMAN_RESOURCES``, ``LEGAL``, ``HEALTH_CARE``,
                ``FINANCE``, ``CUSTOM_CAPP``
            data_consumed (dict):
                Filters the data by cloud application usage in terms of total data uploaded and downloaded.
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
            domainBasedMessageAuthentication (str):
                Filters the cloud applications based on whether they support Domain-based Message Authentication.

                Possible values: ``YES``, ``NO``, ``UNKNOWN``.
            vulnerableDisclosureProgram (str):
                Filters the cloud applications based on whether they support Vulnerability Disclosure Policy.

                Possible values: ``YES``, ``NO``, ``UNKNOWN``.
            wafSupport (str): Filters the cloud applications based on whether WAF is enabled for the applications.

                Possible values: ``YES``, ``NO``, ``UNKNOWN``.
            vulnerability (str):
                Filters the cloud applications based on whether they have published Common Vulnerabilities and
                Exposures (CVE).

                Possible values: ``YES``, ``NO``, ``UNKNOWN``.
            validSSLCertificate (str):
                Filters the cloud applications based on whether they have a valid SSL certificate.

                Possible values: ``YES``, ``NO``, ``UNKNOWN``.
            dataEncryptionInTransit (str):
                Filters the cloud applications based on whether they support data encryption in transit.

                Possible values: ``YES``, ``NO``, ``UNKNOWN``.
            vulnerableToHeartBleed (str):
                Filters the cloud applications based on whether they are vulnerable to Heartbleed attack.

                Possible values: ``YES``, ``NO``, ``UNKNOWN``.
            vulnerableToPoodle (str):
                Filters the cloud applications based on whether they are vulnerable to Poodle attack.

                Possible values: ``YES``, ``NO``, ``UNKNOWN``.
            vulnerableToLogJam (str):
                Filters the cloud applications based on whether they are vulnerable to Logjam attack.

                Possible values: ``YES``, ``NO``, ``UNKNOWN``.
            certKeySize (dict):
                Filters the data by the size of the SSL certificate public keys used by the cloud applications.
                ``operation`` field indicates whether the specified security certifications are included or excluded.

                Possible values for ``operation`` field: ``INCLUDE``, ``EXCLUDE``.
                ``value`` field specifies the list of security certifications.

                Possible values for ``value`` field: ``NONE``, ``UN_KNOWN``, ``BITS_2048``, ``BITS_256``,
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
            entity (str): The entity for which the Shadow IT Report should be generated.

            Possible values: ``USER``, ``LOCATION``.

        Keyword Args:
            order (dict): Sorts the list by the specified attribute.

                Possible values for ``on``: ``RISK_SCORE``, ``APPLICATION``, ``APPLICATION_CATEGORY``,
                ``SANCTIONED_STATE``, ``TOTAL_BYTES``, ``UPLOAD_BYTES``, ``DOWNLOAD_BYTES``, ``AUTHENTICATED_USERS``,
                ``TRANSACTION_COUNT``, ``UNAUTH_LOCATION``, ``LAST_ACCESSED``.

                Possible values for ``by``: ``INCREASING``, ``DECREASING``.
            downloadBytes (dict): Filters by the amount of data (in bytes) downloaded from the application.
                ``min`` and ``max`` fields specify the range.
            uploadBytes (dict): Filters by the amount of data (in bytes) uploaded to the application.
                ``min`` and ``max`` fields specify the range.
            dataConsumed (dict): Filters by the total amount of data uploaded and downloaded from the application.
                ``min`` and ``max`` fields specify the range.
            users (dict): Filters by user.
                ``id`` and ``name`` fields specify the user information.
            locations (dict): Filters by location.
                ``id`` and ``name`` fields specify the location information.
            departments (dict): Filters by department.
                ``id`` and ``name`` fields specify the department information.

        Returns:
            :obj:`str`: The Shadow IT Report in CSV format.
        """

        payload = {"application": application, "duration": duration}

        convert_keys(payload.update(kwargs))

        return self._post(f"shadowIT/applications/{entity}/exportCsv", json=payload).text
