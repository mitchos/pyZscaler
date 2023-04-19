from restfly.endpoint import APIEndpoint

from pyzscaler.utils import zdx_params


class DevicesAPI(APIEndpoint):
    @zdx_params
    def list_devices(self, **kwargs):
        """
        Returns a list of all devices in ZDX.

        Keyword Args:
            since (int): The number of hours to look back for devices.
            location_id (str): The unique ID for the location.
            department_id (str): The unique ID for the department.
            geo_id (str): The unique ID for the geolocation.

        Returns:
            :obj:`BoxList`: The list of devices in ZDX.

        Examples:
            List all devices in ZDX for the past 2 hours
            >>> for device in zdx.devices.list_devices():

            List all devices in ZDX for the past 24 hours
            >>> for device in zdx.devices.list_devices(since=24):

        """
        return self._get("devices", params=kwargs)

    @zdx_params
    def get_device(self, device_id: str, **kwargs):
        """
        Returns a single device in ZDX.

        Args:
            device_id (str): The unique ID for the device.

        Keyword Args:
            since (int): The number of hours to look back for devices.

        Returns:
            :obj:`Box`: The ZDX device resource record.

        Examples:
            Get information for the device with an ID of 123456789.
            >>> device = zdx.devices.get_device('123456789')

            Get information for the device with an ID of 123456789 for the last 24 hours.
            >>> device = zdx.devices.get_device('123456789', since=24)

        """
        return self._get(f"devices/{device_id}", params=kwargs)

    @zdx_params
    def get_device_apps(self, device_id: str, **kwargs):
        """
        Returns a list of all active applications for a device.

        Args:
            device_id (str): The unique ID for the device.

        Keyword Args:
            since (int): The number of hours to look back for devices.

        Returns:
            :obj:`BoxList`: The list of active applications for the device.

        Examples:
            Print a list of active applications for a device.

            >>> for app in zdx.devices.get_device_apps('123456789'):
            ...     print(app)

            Print a list of active applications for a device for the last 24 hours.

            >>> for app in zdx.devices.get_device_apps('123456789', since=24):
            ...     print(app)

        """
        return self._get(f"devices/{device_id}/apps", params=kwargs)

    def get_device_app(self, device_id: str, app_id: str):
        """
        Returns a single application for a device.

        Args:
            device_id (str): The unique ID for the device.
            app_id (str): The unique ID for the application.

        Returns:
            :obj:`Box`: The application resource record.

        Examples:
            Print a single application for a device.

            >>> app = zdx.devices.get_device_app('123456789', '987654321')
            ... print(app)

        """
        return self._get(f"devices/{device_id}/apps/{app_id}")

    def get_web_probes(self, device_id: str, app_id: str):
        """
        Returns a list of all active web probes for a specific application being used by a device.

        Args:
            device_id (str): The unique ID for the device.
            app_id (str): The unique ID for the application.

        Returns:
            :obj:`BoxList`: The list of web probes for the application.

        Examples:
            Print a list of web probes for an application.

            >>> for probe in zdx.devices.get_device_app_webprobes('123456789', '987654321'):
            ...     print(probe)

        """
        return self._get(f"devices/{device_id}/apps/{app_id}/web-probes")

    @zdx_params
    def get_web_probe(self, device_id: str, app_id: str, probe_id: str, **kwargs):
        """
        Returns a single web probe for a specific application being used by a device.

        Args:
            device_id (str): The unique ID for the device.
            app_id (str): The unique ID for the application.
            probe_id (str): The unique ID for the web probe.

        Keyword Args:
            since (int): The number of hours to look back for devices.

        Returns:
            :obj:`Box`: The web probe resource record.

        Examples:
            Print a single web probe for an application.

            >>> probe = zdx.devices.get_web_probe('123456789', '987654321', '123987456')
            ... print(probe)

        """
        return self._get(f"devices/{device_id}/apps/{app_id}/web-probes/{probe_id}", params=kwargs)

    @zdx_params
    def list_cloudpath_probes(self, device_id: str, app_id: str, **kwargs):
        """
        Returns a list of all active cloudpath probes for a specific application being used by a device.

        Args:
            device_id (str): The unique ID for the device.
            app_id (str): The unique ID for the application.

        Keyword Args:
            since (int): The number of hours to look back for devices.

        Returns:
            :obj:`BoxList`: The list of cloudpath probes for the application.

        Examples:
            Print a list of cloudpath probes for an application.

            >>> for probe in zdx.devices.list_cloudpath_probes('123456789', '987654321'):
            ...     print(probe)

        """
        return self._get(f"devices/{device_id}/apps/{app_id}/cloudpath-probes", params=kwargs)

    @zdx_params
    def get_cloudpath_probe(self, device_id: str, app_id: str, probe_id: str, **kwargs):
        """
        Returns a single cloudpath probe for a specific application being used by a device.

        Args:
            device_id (str): The unique ID for the device.
            app_id (str): The unique ID for the application.
            probe_id (str): The unique ID for the cloudpath probe.

        Keyword Args:
            since (int): The number of hours to look back for devices.

        Returns:
            :obj:`Box`: The cloudpath probe resource record.

        Examples:
            Print a single cloudpath probe for an application.

            >>> probe = zdx.devices.get_cloudpath_probe('123456789', '987654321', '123987456')
            ... print(probe)

        """
        return self._get(f"devices/{device_id}/apps/{app_id}/cloudpath-probes/{probe_id}", params=kwargs)

    @zdx_params
    def get_cloudpath(self, device_id: str, app_id: str, probe_id: str, **kwargs):
        """
        Returns a single cloudpath for a specific application being used by a device.

        Args:
            device_id (str): The unique ID for the device.
            app_id (str): The unique ID for the application.
            probe_id (str): The unique ID for the cloudpath probe.

        Keyword Args:
            since (int): The number of hours to look back for devices.

        Returns:
            :obj:`Box`: The cloudpath resource record.

        Examples:
            Print a single cloudpath for an application.

            >>> cloudpath = zdx.devices.get_cloudpath('123456789', '987654321', '123987456')
            ... print(cloudpath)

        """
        return self._get(f"devices/{device_id}/apps/{app_id}/cloudpath-probes/{probe_id}/cloudpath", params=kwargs)

    @zdx_params
    def get_call_quality_metrics(self, device_id: str, app_id: str, **kwargs):
        """
        Returns a single call quality metrics for a specific application being used by a device.

        Args:
            device_id (str): The unique ID for the device.
            app_id (str): The unique ID for the application.

        Keyword Args:
            since (int): The number of hours to look back for devices.

        Returns:
            :obj:`Box`: The call quality metrics resource record.

        Examples:
            Print call quality metrics for an application.

            >>> metrics = zdx.devices.get_call_quality_metrics('123456789', '987654321')
            ... print(metrics)

        """
        return self._get(f"devices/{device_id}/apps/{app_id}/call-quality-metrics", params=kwargs)

    @zdx_params
    def get_health_metrics(self, device_id: str, **kwargs):
        """
        Returns health metrics trend for a specific device.

        Args:
            device_id (str): The unique ID for the device.

        Keyword Args:
            since (int): The number of hours to look back for devices.

        Returns:
            :obj:`Box`: The health metrics resource record.

        Examples:
            Print health metrics for an application.

            >>> metrics = zdx.devices.get_health_metrics('123456789')
            ... print(metrics)

        """
        return self._get(f"devices/{device_id}/health-metrics", params=kwargs)

    def get_events(self, device_id: str):
        """
        Returns a list of all events for a specific device.

        Args:
            device_id (str): The unique ID for the device.

        Returns:
            :obj:`BoxList`: The list of events for the device.

        Examples:
            Print a list of events for a device.

            >>> for event in zdx.devices.get_events('123456789'):
            ...     print(event)

        """
        return self._get(f"devices/{device_id}/events")

    def list_deeptraces(self, device_id: str):
        """
        Returns a list of all deep traces for a specific device.

        Args:
            device_id (str): The unique ID for the device.

        Returns:
            :obj:`BoxList`: The list of deep traces for the device.

        Examples:
            Print a list of deep traces for a device.

            >>> for trace in zdx.devices.list_deep_traces('123456789'):
            ...     print(trace)

        """
        return self._get(f"devices/{device_id}/deeptraces")

    def start_deeptrace(self, device_id: str, app_id: str, session_name: str, **kwargs):
        """
        Starts a deep trace for a specific device and application.

        Args:
            device_id (str): The unique ID for the device.
            app_id (str): The unique ID for the application.
            session_name (str): The name of the deeptrace session.

        Keyword Args:
            web_probe_id (str): The unique ID for the Web probe.
            cloudpath_probe_id (str): The unique ID for the Cloudpath probe.
            session_length_minutes (int): The duration of the deeptrace session in minutes. Defaults to 5.
            probe_device (bool): Whether to probe the device.

        Returns:
            :obj:`Box`: The deeptrace resource record.

        Examples:
            Start a deeptrace for a device.

            >>> trace = zdx.devices.start_deeptrace(device_id='123456789', app_id='1', session_name='My Deeptrace')
            ... print(trace)

        """
        payload = {
            "session_name": session_name,
            "app_id": app_id,
        } | kwargs

        return self._post(f"devices/{device_id}/deeptraces", json=payload)

    def get_deeptrace(self, device_id: str, trace_id: str):
        """
        Returns information on a single deeptrace for a specific device.

        Args:
            device_id (str): The unique ID for the device.
            trace_id (str): The unique ID for the deeptrace.

        Returns:
            :obj:`Box`: The deeptrace resource record.

        Examples:
            Print a single deeptrace for a device.

            >>> trace = zdx.devices.get_deeptrace('123456789', '987654321')
            ... print(trace)

        """
        return self._get(f"devices/{device_id}/deeptraces/{trace_id}")

    def delete_deeptrace(self, device_id: str, trace_id: str):
        """
        Deletes a single deeptrace session and associated data for a specific device.

        Args:
            device_id (str): The unique ID for the device.
            trace_id (str): The unique ID for the deeptrace.

        Returns:
            :obj:`str`: The trace ID that was deleted.

        Examples:
            Delete a single deeptrace for a device.

            >>> trace = zdx.devices.delete_deeptrace('123456789', '987654321')
            ... print(trace)

        """
        return self._delete(f"devices/{device_id}/deeptraces/{trace_id}")

    def get_deeptrace_webprobe_metrics(self, device_id: str, trace_id: str):
        """
        Returns web probe metrics for a specific deeptrace.

        Args:
            device_id (str): The unique ID for the device.
            trace_id (str): The unique ID for the deeptrace.

        Returns:
            :obj:`Box`: The deeptrace web probe metrics.

        Examples:
            Print web probe metrics for a deeptrace.

            >>> metrics = zdx.devices.get_deeptrace_webprobe_metrics('123456789', '987654321')
            ... print(metrics)

        """
        return self._get(f"devices/{device_id}/deeptraces/{trace_id}/webprobe-metrics")

    def get_deeptrace_cloudpath_metrics(self, device_id: str, trace_id: str):
        """
        Returns cloudpath metrics for a specific deeptrace.

        Args:
            device_id (str): The unique ID for the device.
            trace_id (str): The unique ID for the deeptrace.

        Returns:
            :obj:`Box`: The deeptrace cloudpath metrics.

        Examples:
            Print cloudpath metrics for a deeptrace.

            >>> metrics = zdx.devices.get_deeptrace_cloudpath_metrics('123456789', '987654321')
            ... print(metrics)

        """
        return self._get(f"devices/{device_id}/deeptraces/{trace_id}/cloudpath-metrics")

    def get_deeptrace_cloudpath(self, device_id: str, trace_id: str):
        """
        Returns cloudpath for a specific deeptrace.

        Args:
            device_id (str): The unique ID for the device.
            trace_id (str): The unique ID for the deeptrace.

        Returns:
            :obj:`Box`: The deeptrace cloudpath.

        Examples:
            Print cloudpath for a deeptrace.

            >>> metrics = zdx.devices.get_deeptrace_cloudpath('123456789', '987654321')
            ... print(metrics)

        """
        return self._get(f"devices/{device_id}/deeptraces/{trace_id}/cloudpath")

    def get_deeptrace_health_metrics(self, device_id: str, trace_id: str):
        """
        Returns health metrics for a specific deeptrace.

        Args:
            device_id (str): The unique ID for the device.
            trace_id (str): The unique ID for the deeptrace.

        Returns:
            :obj:`Box`: The deeptrace health metrics.

        Examples:
            Print health metrics for a deeptrace.

            >>> metrics = zdx.devices.get_deeptrace_health_metrics('123456789', '987654321')
            ... print(metrics)

        """
        return self._get(f"devices/{device_id}/deeptraces/{trace_id}/health-metrics")

    def get_deeptrace_events(self, device_id: str, trace_id: str):
        """
        Returns events for a specific deeptrace.

        Args:
            device_id (str): The unique ID for the device.
            trace_id (str): The unique ID for the deeptrace.

        Returns:
            :obj:`Box`: The deeptrace events.

        Examples:
            Print events for a deeptrace.

            >>> events = zdx.devices.get_deeptrace_events('123456789', '987654321')
            ... print(events)

        """
        return self._get(f"devices/{device_id}/deeptraces/{trace_id}/events")

    def get_deeptrace_top_processes(self, device_id: str, trace_id: str):
        """
        Returns top processes for a specific deeptrace.

        Args:
            device_id (str): The unique ID for the device.
            trace_id (str): The unique ID for the deeptrace.

        Returns:
            :obj:`Box`: The deeptrace top processes.

        Examples:
            Print top processes for a deeptrace.

            >>> top_processes = zdx.devices.get_deeptrace_top_processes('123456789', '987654321')
            ... print(top_processes)

        """
        return self._get(f"devices/{device_id}/deeptraces/{trace_id}/top-processes")
