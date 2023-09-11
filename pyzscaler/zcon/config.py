from box import Box
from restfly import APIEndpoint


class ConfigAPI(APIEndpoint):
    def activate(self, force: bool = False) -> Box:
        """
        Activate the configuration.

        Returns:
            :obj:`int`: The status code of the operation.

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

        """
        return self._get("ecAdminActivateStatus")
