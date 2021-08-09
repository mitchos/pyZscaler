import os

from restfly.session import APISession

from pyzscaler.version import version
from .audit_logs import AuditLogsAPI
from .config import ActivationAPI
from .firewall import FirewallPolicyAPI
from .locations import LocationsAPI
from .sandbox import CloudSandboxAPI
from .security import SecurityPolicyAPI
from .session import AuthenticatedSessionAPI
from .ssl import SSLInspectionAPI
from .traffic import TrafficForwardingAPI
from .url_categories import URLCategoriesAPI
from .url_filters import URLFilteringAPI
from .users import UserManagementAPI
from .vips import DataCenterVIPSAPI


class ZIA(APISession):
    """
    A Controller to access Endpoints in the Zscaler Internet Access (ZIA) API.

    The ZIA object stores the session token and simplifies access to CRUD options within the ZIA platform.

    Attributes:
        api_key (str): The ZIA API key generated from the ZIA console.
        username (str): The ZIA administrator username.
        password (str): The ZIA administrator password.

    """

    _vendor = "Zscaler"
    _product = "Zscaler Internet Access"
    _backoff = 3
    _build = version
    _box = True
    _box_attrs = {"camel_killer_box": True}
    _env_base = "ZIA"
    _env_cloud = "zscaler"
    _url = "https://zsapi.zscaler.net/api/v1"

    def __init__(self, **kw):
        self._api_key = kw.get("api_key", os.getenv(f"{self._env_base}_API_KEY"))
        self._username = kw.get("username", os.getenv(f"{self._env_base}_USERNAME"))
        self._password = kw.get("password", os.getenv(f"{self._env_base}_PASSWORD"))
        self._env_cloud = kw.get("cloud", os.getenv(f"{self._env_base}_CLOUD"))
        self._url = f"https://zsapi.{self._env_cloud}.net/api/v1"
        super(ZIA, self).__init__(**kw)

    def _build_session(self, **kwargs) -> None:
        """Creates a ZIA API session."""
        super(ZIA, self)._build_session(**kwargs)
        return self.session.create(
            api_key=self._api_key, username=self._username, password=self._password
        )

    def _deauthenticate(self):
        """Ends the authentication session."""
        return self.session.delete()

    @property
    def session(self):
        """The interface object for the :ref:`ZIA Authenticated Session interface <zia-session>`."""
        return AuthenticatedSessionAPI(self)

    @property
    def audit_logs(self):
        """
        The interface object for the :ref:`ZIA Admin Audit Logs interface <zia-audit_logs>`.

        """
        return AuditLogsAPI(self)

    @property
    def config(self):
        """
        The interface object for the :ref:`ZIA Activation interface <zia-config>`.

        """
        return ActivationAPI(self)

    @property
    def firewall(self):
        """
        The interface object for the :ref:`ZIA Firewall Policies interface <zia-firewall>`.

        """
        return FirewallPolicyAPI(self)

    @property
    def locations(self):
        """
        The interface object for the :ref:`ZIA Locations interface <zia-locations>`.

        """
        return LocationsAPI(self)

    @property
    def sandbox(self):
        """
        The interface object for the :ref:`ZIA Cloud Sandbox interface <zia-sandbox>`.

        """
        return CloudSandboxAPI(self)

    @property
    def security(self):
        """
        The interface object for the :ref:`ZIA Security Policy Settings interface <zia-security>`.

        """
        return SecurityPolicyAPI(self)

    @property
    def ssl(self):
        """
        The interface object for the :ref:`ZIA SSL Inspection interface <zia-ssl>`.

        """
        return SSLInspectionAPI(self)

    @property
    def traffic(self):
        """
        The interface object for the :ref:`ZIA Traffic Forwarding interface <zia-traffic>`.

        """
        return TrafficForwardingAPI(self)

    @property
    def url_categories(self):
        """
        The interface object for the :ref:`ZIA URL Categories interface <zia-url_categories>`.

        """
        return URLCategoriesAPI(self)

    @property
    def url_filters(self):
        """
        The interface object for the :ref:`ZIA URL Filtering interface <zia-url_filters>`.

        """
        return URLFilteringAPI(self)

    @property
    def users(self):
        """
        The interface object for the :ref:`ZIA User Management interface <zia-users>`.

        """
        return UserManagementAPI(self)

    @property
    def vips(self):
        """
        The interface object for the :ref:`ZIA Data Center VIPs interface <zia-vips>`.

        """
        return DataCenterVIPSAPI(self)
