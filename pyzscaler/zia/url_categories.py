from box import Box, BoxList
from restfly.endpoint import APIEndpoint

from pyzscaler.utils import convert_keys, snake_to_camel


class URLCategoriesAPI(APIEndpoint):
    def lookup(self, urls: list) -> BoxList:
        """
        Lookup the category for the provided URLs.

        Args:
            urls (list):
                The list of URLs to perform a category lookup on.

        Returns:
            :obj:`BoxList`: A list of URL category reports.

        Examples:
            >>> zia.url_categories.lookup(['example.com', 'test.com'])

        """
        payload = urls

        return self._post("urlLookup", json=payload)

    def list_categories(self, custom_only: bool = False) -> BoxList:
        """
        Returns information on URL categories.

        Args:
            custom_only (bool):
                Returns only custom categories if True.

        Returns:
            :obj:`BoxList`: A list of information for all or custom URL categories.

        Examples:
            List all URL categories:

            >>> zia.url_categories.list_categories()

            List only custom URL categories:

            >>> zia.url_categories.list_categories(custom_only=True)

        """

        return self._get(f"urlCategories?customOnly={custom_only}")

    def get_quota(self) -> Box:
        """
        Returns information on URL category quota usage.

        Returns:
            :obj:`Box`: The URL quota statistics.

        Examples:
            >>> zia.url_categories.get_quota()

        """

        return self._get("urlCategories/urlQuota")

    def get_category(self, category_id: str) -> Box:
        """
        Returns URL category information for the provided category.

        Args:
            category_id (str):
                The unique identifier for the category (e.g. 'MUSIC')

        Returns:
            :obj:`Box`: The resource record for the category.

        Examples:
            >>> zia.url_categories.get_category('ALCOHOL_TOBACCO')

        """
        return self._get(f"urlCategories/{category_id}")

    def add_url_category(self, name: str, super_category: str, urls: list, **kwargs) -> Box:
        """
        Adds a new custom URL category.

        Args:
            name (str):
                Name of the URL category.
            super_category (str):
                The name of the parent category.
            urls (list):
                Custom URLs to add to a URL category.
            **kwargs:
                Optional keyword args.

        Keyword Args:
            db_categorized_urls (list):
                URLs entered will be covered by policies that reference the parent category, in addition to this one.
            description (str):
                Description of the category.
            custom_category (bool):
                Set to true for custom URL category. Up to 48 custom URL categories can be added per organisation.

        Returns:
            :obj:`Box`: The newly configured custom URL category resource record.

        Examples:
            Add a new category for beers that don't taste good:

            >>> zia.url_categories.add_url_category(name='Beer',
            ...    super_category='ALCOHOL_TOBACCO',
            ...    urls=['xxxx.com.au', 'carltondraught.com.au'],
            ...    description="Beers that don't taste good")

        """

        payload = {
            "type": "URL_CATEGORY",
            "superCategory": super_category,
            "configuredName": name,
            "urls": urls,
        }

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        return self._post("urlCategories", json=payload)

    def add_tld_category(self, name: str, tlds: list, **kwargs) -> Box:
        """
        Adds a new custom TLD category.

        Args:
            name (str):
                The name of the TLD category.
            tlds (list):
                A list of TLDs in the format '.tld'.
            **kwargs:
                Optional keyword args.

        Keyword Args:
            description (str):
                Description of the category.

        Returns:
            :obj:`Box`: The newly configured custom TLD category resource record.

        Examples:
            Create a category for all 'developer' sites:

            >>> zia.url_categories.add_tld_category(name='Developer Sites',
            ...    urls=['.dev'],
            ...    description="Sites that are likely run by developers.")

        """

        payload = {
            "type": "TLD_CATEGORY",
            "superCategory": "USER_DEFINED",  # TLDs can only be added in USER_DEFINED category
            "configuredName": name,
            "urls": tlds,  # ZIA API reuses the 'urls' key for tlds
        }

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        return self._post("urlCategories", json=payload)

    def update_url_category(self, category_id: str, **kwargs) -> Box:
        """
        Updates a URL category.

        Args:
            category_id (str):
                The unique identifier of the URL category.
            **kwargs:
                Optional keyword args.

        Keyword Args:
            name (str):
                The name of the URL category.
            urls (list):
                Custom URLs to add to a URL category.
            db_categorized_urls (list):
                URLs entered will be covered by policies that reference the parent category, in addition to this one.
            description (str):
                Description of the category.

        Returns:
            :obj:`Box`: The updated URL category resource record.

        Examples:
            Update the name of a category:

            >>> zia.url_categories.update_url_category('CUSTOM_01',
            ...    name="Wines that don't taste good.")

            Update the urls of a category:

            >>> zia.url_categories.update_url_category('CUSTOM_01',
            ...    urls=['www.yellowtailwine.com'])

        """

        payload = convert_keys(self.get_category(category_id))

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        return self._put(f"urlCategories/{category_id}", json=payload)

    def add_urls_to_category(self, category_id: str, urls: list) -> Box:
        """
        Adds URLS to a URL category.

        Args:
            category_id (str):
                The unique identifier of the URL category.
            urls (list):
                Custom URLs to add to a URL category.

        Returns:
            :obj:`Box`: The updated URL category resource record.

        Examples:
            >>> zia.url_categories.add_urls_to_category('CUSTOM_01',
            ...    urls=['example.com'])

        """

        payload = convert_keys(self.get_category(category_id))
        payload["urls"] = urls

        return self._put(f"urlCategories/{category_id}?action=ADD_TO_LIST", json=payload)

    def delete_urls_from_category(self, category_id: str, urls: list) -> Box:
        """
        Adds URLS to a URL category.

        Args:
            category_id (str):
                The unique identifier of the URL category.
            urls (list):
                Custom URLs to delete from a URL category.

        Returns:
            :obj:`Box`: The updated URL category resource record.

        Examples:
            >>> zia.url_categories.delete_urls_from_category('CUSTOM_01',
            ...    urls=['example.com'])

        """

        payload = convert_keys(self.get_category(category_id))
        payload["urls"] = urls

        return self._put(f"urlCategories/{category_id}?action=REMOVE_FROM_LIST", json=payload)

    def delete_category(self, category_id: str) -> int:
        """
        Deletes the specified URL category.

        Args:
            category_id (str):
                The unique identifier for the category.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> zia.url_categories.delete_category('CUSTOM_01')

        """

        return self._delete(f"urlCategories/{category_id}", box=False).status_code
