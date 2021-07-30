from restfly.endpoint import APIEndpoint


class ActivationAPI(APIEndpoint):
    def status(self):
        """
        Returns the activation status for a configuration change.

        Returns:
            :obj:`str`
                Configuration status.

        Examples:
            >>> config_status = zia.config.status()

        """
        return self._get("status").status

    def activate(self):
        """
        Activates configuration changes.

        Returns:
            :obj:`str`
                Configuration status.

        Examples:
            >>> config_activate = zia.config.activate()

        """
        return self._post("status/activate").status
