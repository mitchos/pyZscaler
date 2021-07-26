from restfly.endpoint import APIEndpoint


class AuditLogsAPI(APIEndpoint):
    def status(self):
        """
        Get the status of a request for an audit log report.

        Returns:
            :obj:`dict`: Audit log report request status.

        Examples:
            >>> print(zia.audit_logs.status())

        """
        return self._get("auditlogEntryReport")

    def create(self, start_time: str, end_time: str):
        """
        Creates an audit log report for the specified time period and saves it as a CSV file. The report
        includes audit information for every call made to the cloud service API during the specified time period.
        Creating a new audit log report will overwrite a previously-generated report.

        Args:
            start_time (str):
                The timestamp, in epoch, of the admin's last login.
            end_time (str):
                The timestamp, in epoch, of the admin's last logout.

        Returns:
            :obj:`str`: The status code for the operation.

        Examples:
            >>> zia.audit_logs.create(start_time='1627221600000',
            ...    end_time='1627271676622')

        """
        payload = {
            "startTime": start_time,
            "endTime": end_time,
        }
        return self._post("auditlogEntryReport", json=payload, box=False).status_code

    def cancel(self):
        """
        Cancels the request to create an audit log report.

        Returns:
            :obj:`str`: The operation response code.

        Examples:
            >>> zia.audit_logs.cancel()

        """
        return self._delete("auditlogEntryReport", box=False).status_code

    def get_report(self):
        """
        Returns the most recently created audit log report.

        Returns:
            :obj:`str`: String representation of CSV file.

        Examples:
            Write report to CSV file:

            >>> with open("audit_log.csv", "w+") as fh:
            ...    fh.write(zia.audit_logs.get_report())

        """
        return self._get("auditlogEntryReport/download", box=False).text
