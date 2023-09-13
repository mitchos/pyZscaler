from box import Box
from restfly import APIEndpoint


class ZCONConfigAPI(APIEndpoint):
    def activate(self, force: bool = False) -> Box:
        """
        Activate the configuration.

        Args:
            force (bool): If set to True, forces the activation. Default is False.

        Returns:
            :obj:`Box`: The status code of the operation.

        Examples:
            Activate the configuration without forcing::

                zcon.config.activate()

            Forcefully activate the configuration::

                zcon.config.activate(force=True)

        """
        if force:
            return self._post("ecAdminActivateStatus/forcedActivate")
        else:
            return self._post("ecAdminActivateStatus/activate")

    def get_status(self):
        """
        Get the status of the configuration.

        Returns:
            :obj:`Box`: The status of the configuration.

        Examples:
            Get the status of the configuration::

                print(zcon.config.get_status())

        """
        return self._get("ecAdminActivateStatus")
