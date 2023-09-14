from typing import Dict, List, Optional, Union

from box import Box
from restfly import APISession
from restfly.endpoint import APIEndpoint


class MicrotenantsAPI(APIEndpoint):
    def __init__(self, api: APISession):
        super().__init__(api)

        self.url_base = api.url_base

    def get_current_microtenant(self) -> Box:
        """
        Returns the name and ID of the configured Microtenant for the customer account this API key is associated with.

        Returns:
            :obj:`Box`: The name and ID of the configured Microtenant.

        Examples:

            Print the name and ID of the configured Microtenant::

                print(zpa.microtenants.list_microtenants())

        """
        return self._get("microtenants/summary")

    def find_microtenants(
        self,
        filters: Optional[List[Dict[str, Union[str, List[str]]]]] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort_name: Optional[str] = None,
        sort_order: Optional[str] = None,
    ):
        """
        Search for microtenants based on various filters.

        Args:
            filters (List[Dict], optional):
            A list of dictionaries, each representing a filter. Each dictionary should have the following keys:

                - 'filterName': The name of the filter.
                - 'operator': The operator to use (e.g., "equals", "not_equals").
                - 'values': A list of strings that you want to filter by.
                - 'commaSepValues':
                    A string of comma-separated values. Use only if you want to provide multiple filter values as a
                    string.
            page (int, optional): The page number to return.
            page_size (int, optional): The number of items to return per page.
            sort_name (str, optional): The name of the attribute to sort by.
            sort_order (str, optional): The sort order. Use "asc" for ascending and "desc" for descending.

        Returns:
            :obj:`Box`: The list of microtenants that match the filter criteria.

        Examples:
            Example with only filters::

                zpa.microtenants.find_microtenants(
                    filters=[
                        {
                            "filterName": "name",
                            "operator": "equals",
                            "values": ["value1"],
                        }
                    ]
                )
            Example with filters and pagination::

                zpa.microtenants.find_microtenants(
                    filters=[
                        {
                            "filterName": "name",
                            "operator": "equals",
                            "values": ["value1"],
                        }
                    ],
                    page=1,
                    page_size=10
                )

            Example with filters, pagination, and sorting::

                zpa.microtenants.find_microtenants(
                    filters=[
                        {
                            "filterName": "name",
                            "operator": "equals",
                            "values": ["value1"],
                        }
                    ],
                    page=1,
                    page_size=10,
                    sort_name="name",
                    sort_order="asc"
                )

        """
        filter_payload = {
            "filterBy": filters if filters is not None else [],
            "pageBy": {
                "page": str(page) if page is not None else None,
                "pageSize": str(page_size) if page_size is not None else None,
            },
            "sortBy": {"sortName": sort_name, "sortOrder": sort_order},
        }

        # Remove None values
        filter_payload = {k: v for k, v in filter_payload.items() if v is not None}
        filter_payload["pageBy"] = {k: v for k, v in filter_payload.get("pageBy", {}).items() if v is not None}

        return self._post("microtenants/search", json=filter_payload)

    def get_session(self) -> Box:
        """
        Returns the details of the current Microtenant session.

        Returns:
            :obj:`Box`: The details of the current Microtenant session.

        Examples:
            Print the details of the current Microtenant session::

                print(zpa.microtenants.get_session())

        """
        return self._get(f"{self.url_base}/mgmtconfig/v1/admin/me")
