import os

from box import Box
from restfly.session import APISession

from pyzscaler import __version__
from pyzscaler.zdx.admin import AdminAPI
from pyzscaler.zdx.apps import AppsAPI
from pyzscaler.zdx.devices import DevicesAPI
from pyzscaler.zdx.session import SessionAPI
from pyzscaler.zdx.users import UsersAPI


class ZDX(APISession):
    """
    A Controller to access Endpoints in the Zscaler Digital Experience (ZDX) API.

    The ZDX object stores the session token and simplifies access to CRUD options within the ZDX Portal.

    Attributes:
        client_id (str): The ZDX Client ID generated from the ZDX Portal.
        client_secret (str): The ZDX Client Secret generated from the ZDX Portal.
        cloud (str): The Zscaler cloud for your tenancy, accepted values are below. Defaults to ``zdxcloud``.

            * ``zdxcloud``
            * ``zdxbeta``

        override_url (str):
            If supplied, this attribute can be used to override the production URL that is derived
            from supplying the `cloud` attribute. Use this attribute if you have a non-standard tenant URL
            (e.g. internal test instance etc). When using this attribute, there is no need to supply the `cloud`
            attribute. The override URL will be prepended to the API endpoint suffixes. The protocol must be included
            i.e. http:// or https://.

    """

    _vendor = "Zscaler"
    _product = "pyZscaler"
    _backoff = 3
    _build = __version__
    _box = True
    _box_attrs = {"camel_killer_box": True}
    _env_base = "ZDX"
    _env_cloud = "zdxcloud"
    _url = "https://api.zdxcloud.net/v1"

    def __init__(self, **kw):
        self._client_id = kw.get("client_id", os.getenv(f"{self._env_base}_CLIENT_ID"))
        self._client_secret = kw.get("client_secret", os.getenv(f"{self._env_base}_CLIENT_SECRET"))
        self._cloud = kw.get("cloud", os.getenv(f"{self._env_base}_CLOUD", self._env_cloud))
        self._url = kw.get("override_url", os.getenv(f"{self._env_base}_OVERRIDE_URL")) or f"https://api.{self._cloud}.net/v1"
        self.conv_box = True
        super(ZDX, self).__init__(**kw)

    def _build_session(self, **kwargs) -> Box:
        """Creates a ZCC API session."""
        super(ZDX, self)._build_session(**kwargs)
        self._auth_token = self.session.create_token(client_id=self._client_id, client_secret=self._client_secret).token
        return self._session.headers.update({"Authorization": f"Bearer {self._auth_token}"})

    @property
    def session(self):
        """The interface object for the :ref:`ZDX Session interface <zdx-session>`."""
        return SessionAPI(self)

    @property
    def admin(self):
        """The interface object for the :ref:`ZDX Admin interface <zdx-admin>`."""
        return AdminAPI(self)

    @property
    def apps(self):
        """The interface object for the :ref:`ZDX Apps interface <zdx-apps>`."""
        return AppsAPI(self)

    @property
    def devices(self):
        """The interface object for the :ref:`ZDX Devices interface <zdx-devices>`."""
        return DevicesAPI(self)

    @property
    def users(self):
        """The interface object for the :ref:`ZDX Users interface <zdx-users>`."""
        return UsersAPI(self)
