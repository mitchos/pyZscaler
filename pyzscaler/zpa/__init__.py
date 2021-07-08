import os
from restfly.session import APISession
from pyzscaler.version import version

from .app_segments import AppSegmentsAPI
from .certificates import BACertificatesAPI
from .cloud_connector_groups import CloudConnectorGroupsAPI
from .connector_groups import ConnectorGroupsAPI
from .idp import IDPControllerAPI
from .machine_groups import MachineGroupsAPI
from .policies import PolicySetsAPI
from .posture_profiles import PostureProfilesAPI
from .saml_attributes import SAMLAttributesAPI
from .scim_attributes import SCIMAttributesAPI
from .scim_groups import SCIMGroupsAPI
from .segment_groups import SegmentGroupsAPI
from .servers import AppServersAPI
from .server_groups import ServerGroupsAPI
from .trusted_networks import TrustedNetworksAPI


class ZPA(APISession):
    """A Controller to access Endpoints in the Zscaler Private Access (ZPA) API.

    The ZPA object stores the session token and simplifies access to API interfaces within ZPA.

    Attributes:
        _client_id (str): The ZPA API client ID generated from the ZPA console.
        _client_secret (str): The ZPA API client secret generated from the ZPA console.
        _customer_id (str): The ZPA tenant ID found in the Administration > Company menu in the ZPA console.

    """
    _vendor = 'Zscaler'
    _product = 'Zscaler Private Access'
    _build = version
    _box = True
    _box_attrs = {
        'camel_killer_box': True
    }
    _env_base = 'ZPA'
    _url = 'https://config.private.zscaler.com'

    def __init__(self, **kw):
        self._client_id = kw.get('client_id',
                                 os.getenv(f'{self._env_base}_CLIENT_ID'))
        self._client_secret = kw.get('client_secret',
                                     os.getenv(f'{self._env_base}_CLIENT_SECRET'))
        self._customer_id = kw.get('customer_id',
                                   os.getenv(f'{self._env_base}_CUSTOMER_ID'))
        super(ZPA, self).__init__(**kw)

    def _build_session(self, **kwargs) -> None:
        super(ZPA, self)._build_session(**kwargs)

        payload = f"client_id={self._client_id}&client_secret={self._client_secret}"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        token = self.post('signin', headers=headers, data=payload).access_token
        self._session.headers.update({
            'Authorization': f'Bearer {token}'
        })
        self._url = f'https://config.private.zscaler.com/mgmtconfig/v1/admin/customers/{self._customer_id}'

    @property
    def servers(self):
        """
        The interface object for the :ref:`ZPA Application Servers interface <zpa-app_servers>`.

        """
        return AppServersAPI(self)

    @property
    def app_segments(self):
        """
        The interface object for the :ref:`ZPA Application Segments interface <zpa-app_segments>`.

        """
        return AppSegmentsAPI(self)

    @property
    def segment_groups(self):
        return SegmentGroupsAPI(self)

    @property
    def connector_groups(self):
        """
        The interface object for the :ref:`ZPA Connector Groups interface <zpa-connector_groups>`.

        """
        return ConnectorGroupsAPI(self)

    @property
    def idp(self):
        """
        The interface object for the :ref:`ZPA IDP interface <zpa-idp>`.

        """
        return IDPControllerAPI(self)

    @property
    def machine_groups(self):
        """
        The interface object for the :ref:`ZPA Machine Groups interface <zpa-machine_groups>`.

        """
        return MachineGroupsAPI(self)

    @property
    def cloud_connector_groups(self):
        """
        The interface object for the :ref:`ZPA Cloud Connector Groups interface <zpa-cloud_connector_groups>`.

        """
        return CloudConnectorGroupsAPI(self)

    @property
    def policies(self):
        """
        The interface object for the :ref:`ZPA Policy Sets interface <zpa-policies>`.

        """
        return PolicySetsAPI(self)

    @property
    def posture_profiles(self):
        """
        The interface object for the :ref:`ZPA Posture Profiles interface <zpa-posture_profiles>`.

        """
        return PostureProfilesAPI(self)

    @property
    def saml_attributes(self):
        """
        The interface object for the :ref:`ZPA SAML Attributes interface <zpa-saml_attributes>`.

        """
        return SAMLAttributesAPI(self)

    @property
    def scim_attributes(self):
        """
        The interface object for the :ref:`ZPA SCIM Attributes interface <zpa-scim_attributes>`.

        """
        return SCIMAttributesAPI(self)

    @property
    def trusted_networks(self):
        """
        The interface object for the :ref:`ZPA Trusted Networks interface <zpa-trusted_networks>`.

        """
        return TrustedNetworksAPI(self)

    @property
    def scim_groups(self):
        """
        The interface object for the :ref:`ZPA SCIM Groups interface <zpa-scim_groups>`.

        """
        self._url = f'https://config.private.zscaler.com/userconfig/v1/customers/{self._customer_id}'
        return SCIMGroupsAPI(self)

    @property
    def server_groups(self):
        """
        The interface object for the :ref:`ZPA Server Groups interface <zpa-server_groups>`.

        """
        return ServerGroupsAPI(self)

    @property
    def certificates(self):
        """
        The interface object for the :ref:`ZPA Browser Access Certificates interface <zpa-certificates>`.

        """
        return BACertificatesAPI(self)
