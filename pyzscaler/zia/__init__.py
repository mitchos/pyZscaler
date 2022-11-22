import os

from box import Box
from restfly.session import APISession

from pyzscaler import __version__

from .admin_and_role_management import AdminAndRoleManagementAPI
from .audit_logs import AuditLogsAPI
from .config import ActivationAPI
from .dlp import DLPAPI
from .firewall import FirewallPolicyAPI
from .labels import RuleLabelsAPI
from .locations import LocationsAPI
from .sandbox import CloudSandboxAPI
from .security import SecurityPolicyAPI
from .session import AuthenticatedSessionAPI
from .ssl_inspection import SSLInspectionAPI
from .traffic import TrafficForwardingAPI
from .url_categories import URLCategoriesAPI
from .url_filters import URLFilteringAPI
from .users import UserManagementAPI
from .vips import DataCenterVIPSAPI
from .web_dlp import WebDLP


class ZIA(APISession):
    """
    A Controller to access Endpoints in the Zscaler Internet Access (ZIA) API.

    The ZIA object stores the session token and simplifies access to CRUD options within the ZIA platform.

    Attributes:
        api_key (str): The ZIA API key generated from the ZIA console.
        username (str): The ZIA administrator username.
        password (str): The ZIA administrator password.
        cloud (str): The Zscaler cloud for your tenancy, accepted values are:

            * ``zscaler``
            * ``zscalerone``
            * ``zscalertwo``
            * ``zscalerthree``
            * ``zscloud``
            * ``zscalerbeta``
        override_url (str):
            If supplied, this attribute can be used to override the production URL that is derived
            from supplying the `cloud` attribute. Use this attribute if you have a non-standard tenant URL
            (e.g. internal test instance etc). When using this attribute, there is no need to supply the `cloud`
            attribute. The override URL will be prepended to the API endpoint suffixes. The protocol must be included
            i.e. http:// or https://.

    """

    _vendor = "Zscaler"
    _product = "Zscaler Internet Access"
    _backoff = 3
    _build = __version__
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
        self._url = (
            kw.get("override_url", os.getenv(f"{self._env_base}_OVERRIDE_URL"))
            or f"https://zsapi.{self._env_cloud}.net/api/v1"
        )
        self.conv_box = True
        self.sandbox_token = kw.get("sandbox_token", os.getenv(f"{self._env_base}_SANDBOX_TOKEN"))
        super(ZIA, self).__init__(**kw)

    def _build_session(self, **kwargs) -> Box:
        """Creates a ZIA API session."""
        super(ZIA, self)._build_session(**kwargs)
        return self.session.create(
            api_key=self._api_key,
            username=self._username,
            password=self._password,
        )

    def _deauthenticate(self):
        """Ends the authentication session."""
        return self.session.delete()

    @property
    def session(self):
        """The interface object for the :ref:`ZIA Authenticated Session interface <zia-session>`."""
        return AuthenticatedSessionAPI(self)

    @property
    def admin_and_role_management(self):
        """
        The interface object for the :ref:`ZIA Admin and Role Management interface <zia-admin_and_role_management>`.

        """
        return AdminAndRoleManagementAPI(self)

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
    def dlp(self):
        """
        The interface object for the :ref:`ZIA DLP Dictionaries interface <zia-dlp>`.


        """
        return DLPAPI(self)

    @property
    def firewall(self):
        """
        The interface object for the :ref:`ZIA Firewall Policies interface <zia-firewall>`.

        """
        return FirewallPolicyAPI(self)

    @property
    def labels(self):
        """
        The interface object for the :ref:`ZIA Rule Labels interface <zia-labels>`.

        """
        return RuleLabelsAPI(self)

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
        The interface object for the :ref:`ZIA SSL Inspection interface <zia-ssl_inspection>`.

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

    @property
    def web_dlp(self):
        """
        The interface object for the :ref: `ZIA Data-Loss-Prevention Web DLP Rules`.

        """
        return WebDLP(self)
