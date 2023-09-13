import os

from box import Box
from restfly import APISession

from pyzscaler import __version__

from .admin import ZCONAdminAPI
from .config import ZCONConfigAPI
from .connectors import ZCONConnectorsAPI
from .locations import ZCONLocationsAPI
from .session import ZCONSessionAPI


class ZCON(APISession):
    """
    A Controller to access Endpoints in the Zscaler Cloud and Branch Connector API.

    The ZCON object stores the session token and simplifies access to CRUD options within the ZCON Portal.

    """

    _vendor = "Zscaler"
    _product = "Zscaler Cloud and Branch Connector"
    _backoff = 3
    _build = __version__
    _box = True
    _box_attrs = {"camel_killer_box": True}
    _env_base = "ZCON"
    _url = "https://connector.zscaler.net/api/v1"
    _env_cloud = "zscaler"

    def __init__(self, **kw):
        self._api_key = kw.get("api_key", os.getenv(f"{self._env_base}_API_KEY"))
        self._username = kw.get("username", os.getenv(f"{self._env_base}_USERNAME"))
        self._password = kw.get("password", os.getenv(f"{self._env_base}_PASSWORD"))
        self.env_cloud = kw.get("cloud", os.getenv(f"{self._env_base}_CLOUD"))
        self._url = (
            kw.get("override_url", os.getenv(f"{self._env_base}_OVERRIDE_URL"))
            or f"https://connector.{self.env_cloud}.net/api/v1"
        )
        self.conv_box = True
        super(ZCON, self).__init__(**kw)

    def _build_session(self, **kwargs) -> Box:
        """
        Build the APISession object.

        This method is called automatically when instantiating the ZCON object.

        Returns:
            Box: The Box object representing the ZCON API.

        """
        super(ZCON, self)._build_session(**kwargs)
        return self.session.create(api_key=self._api_key, username=self._username, password=self._password)

    def _deauthenticate(self):
        """
        End the authentication session.

        Returns:
            Box: The Box object representing the ZCON API.

        """
        return self.session.delete()

    @property
    def admin(self) -> ZCONAdminAPI:
        """
        The interface object for the :ref:`ZCON Admin interface <zcon-admin>`.

        Returns:
            ZCONAdminAPI: The AdminAPI object.

        """
        return ZCONAdminAPI(self)

    @property
    def connectors(self) -> ZCONConnectorsAPI:
        """
        The interface object for the :ref:`ZCON Connectors interface <zcon-connectors>`.

        Returns:
            ZCONConnectorsAPI: The ConnectorsAPI object.

        """
        return ZCONConnectorsAPI(self)

    @property
    def config(self) -> ZCONConfigAPI:
        """
        The interface object for the :ref:`ZCON Config interface <zcon-config>`.

        Returns:
            ZCONConfigAPI: The ConfigAPI object.

        """
        return ZCONConfigAPI(self)

    @property
    def locations(self) -> ZCONLocationsAPI:
        """
        The interface object for the :ref:`ZCON Locations interface <zcon-locations>`.

        Returns:
            ZCONLocationsAPI: The LocationsAPI object.

        """
        return ZCONLocationsAPI(self)

    @property
    def session(self) -> ZCONSessionAPI:
        """
        The interface object for the :ref:`ZCON Authentication interface <zcon-session>`.

        Returns:
            ZCONSessionAPI: The SessionAPI object.

        """
        return ZCONSessionAPI(self)
