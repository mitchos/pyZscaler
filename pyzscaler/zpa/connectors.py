from restfly.endpoint import APIEndpoint

from pyzscaler.utils import Iterator


class ConnectorsAPI(APIEndpoint):
    def list_connectors(self, **kwargs):
        return Iterator(self._api, "connector", **kwargs)

    def get_connector(self, connector_id: str):
        return self._get(f"connector/{connector_id}")

    def update_connector(self):
        pass

    def delete_connector(self, connector_id: str):
        return self._delete(f"connector/{connector_id}")

    def bulk_delete_connector(self, connector_ids: list):
        return self._post("connector/bulkDelete")
