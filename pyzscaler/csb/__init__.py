import os

from box import Box
from restfly.session import APISession

from pyzscaler import __version__

from .sandbox import CloudSandboxAPI


class CSB(APISession):
    """
    A Controller to access the cloud Sanbox API. CSB has a seperate API for submitting files for analysis.
    Analysis reports are retrieved via the ZIA API

    The CSB object stores the session token and simplifies access to CRUD options within the CSB Portal.

    Attributes:
        cloud (str): The Zscaler cloud for your tenancy, accepted values are:

            * ``zscaler``
            * ``zscalerone``
            * ``zscalertwo``
            * ``zscalerthree``
            * ``zscloud``
            * ``zscalerbeta``
        sandbox_token (str): The CSB API key generated from the ZIA console.
        override_sandbox_url (str):
            If supplied, this attribute can be used to override the production URL that is derived
            from supplying the `cloud` attribute. Use this attribute if you have a non-standard tenant URL
            (e.g. internal test instance etc). When using this attribute, there is no need to supply the `cloud`
            attribute. The override URL will be prepended to the API endpoint suffixes. The protocol must be included
            i.e. http:// or https://.

    """

    _vendor = "Zscaler"
    _product = "Zscaler Cloud Sandbox"
    _backoff = 3
    _build = __version__
    _box = True
    _box_attrs = {"camel_killer_box": True}
    _env_base = "ZIA"
    _env_cloud = "zscaler"
    _url = "https://csbapi.zscaler.net/zscsb/submit"

    def __init__(self, **kw):
        self._env_cloud = kw.get("cloud", os.getenv(f"{self._env_base}_CLOUD"))
        self.sandbox_token = kw.get("sandbox_token", os.getenv("SANDBOX_TOKEN"))
        self._url = (
            kw.get("override_sandbox_url", os.getenv(f"{self._env_base}_OVERRIDE_SANDBOX_URL"))
            or f"https://csbapi.{self._env_cloud}.net/zscsb/submit"
        )
        super(CSB, self).__init__(**kw)

    def _build_session(self, **kwargs) -> Box:
        super(CSB, self)._build_session(**kwargs)
        self._session.params = {
            "api_token": self.sandbox_token,
        }

    @property
    def sandbox(self):
        """The interface object for the :ref:`CSB Authenticated Session interface <csb-session>`."""
        return CloudSandboxAPI(self)
