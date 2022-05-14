from box import Box, BoxList
from restfly.endpoint import APIEndpoint

from pyzscaler.utils import Iterator, convert_keys, snake_to_camel


class RuleLabelsAPI(APIEndpoint):
    def list_labels(self, **kwargs) -> BoxList:
        """
        Returns the list of ZIA Rule Labels.

        Keyword Args:
            **max_items (int, optional):
                The maximum number of items to request before stopping iteration.
            **max_pages (int, optional):
                The maximum number of pages to request before stopping iteration.
            **page_size (int, optional):
                Specifies the page size. The default size is 100, but the maximum size is 1000.

        Returns:
            :obj:`BoxList`: The list of Rule Labels configured in ZIA.

        Examples:
            List Rule Labels using default settings:

            >>> for label in zia.labels.list_labels():
            ...   print(label)

            List labels, limiting to a maximum of 10 items:

            >>> for label in zia.labels.list_labels(max_items=10):
            ...    print(label)

            List labels, returning 200 items per page for a maximum of 2 pages:

            >>> for label in zia.labels.list_labels(page_size=200, max_pages=2):
            ...    print(label)

        """
        return BoxList(Iterator(self._api, "ruleLabels", **kwargs))

    def get_label(self, label_id: str) -> Box:
        """
        Returns the label details for a given Rule Label.

        Args:
            label_id (str): The unique identifier for the Rule Label.

        Returns:
            :obj:`Box`: The Rule Label resource record.

        Examples:
            >>> label = zia.labels.get_label('99999')

        """
        return self._get(f"ruleLabels/{label_id}")

    def add_label(self, name: str, **kwargs) -> Box:
        """
        Creates a new ZIA Rule Label.

        Args:
            name (str):
                The name of the Rule Label.

        Keyword Args:
            description (str):
                Additional information about the Rule Label.

        Returns:
            :obj:`Box`: The newly added Rule Label resource record.

        Examples:
            Add a label with default parameters:

            >>> label = zia.labels.add_label("My New Label")

            Add a label with description:

            >>> label = zia.labels.add_label("My Second Label":
            ...    description="My second label description")

        """
        payload = {"name": name}

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        return self._post("ruleLabels", json=payload)

    def update_label(self, label_id: str, **kwargs):
        """
        Updates information for the specified ZIA Rule Label.

        Args:
            label_id (str): The unique id for the Rule Label that will be updated.

        Keyword Args:
            name (str): The name of the Rule Label.
            description (str): Additional information for the Rule Label.

        Returns:
            :obj:`Box`: The updated Rule Label resource record.

        Examples:
            Update the name of a Rule Label:

            >>> label = zia.labels.update_label(99999,
            ...    name="Updated Label Name")

            Update the name and description of a Rule Label:

            >>> label = zia.labels.update_label(99999,
            ...    name="Updated Label Name",
            ...    description="Updated Label Description")

        """
        # Get the label data from ZIA
        payload = convert_keys(self.get_label(label_id))

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        return self._put(f"ruleLabels/{label_id}", json=payload)

    def delete_label(self, label_id):
        """
        Deletes the specified Rule Label.

        Args:
            label_id (str): The unique identifier of the Rule Label that will be deleted.

        Returns:
            :obj:`int`: The response code for the request.

        Examples
            >>> user = zia.labels.delete_label('99999')

        """

        return self._delete(f"ruleLabels/{label_id}", box=False).status_code
