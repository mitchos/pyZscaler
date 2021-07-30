from restfly.endpoint import APIEndpoint
from pyzscaler.utils import snake_to_camel
from box import BoxList


class URLCategoriesAPI(APIEndpoint):
    def lookup(self, urls: list):
        """
        Lookup the category for the provided URLs.

        Args:
            urls (list):
                The list of URLs to perform a category lookup on.

        Returns:
            :obj:`list`: A list of URL category reports.

        Examples:
            >>> zia.url_categories.lookup(['example.com', 'test.com'])

        """
        payload = urls

        return self._post("urlLookup", json=payload, box=BoxList)

    def list_categories(self, custom_only: bool = False):
        """
        Returns information on URL categories.

        Args:
            custom_only (bool):
                Returns only custom categories if True.

        Returns:
            :obj:`list`: A list of information for all or custom URL categories.

        Examples:
            List all URL categories:

            >>> zia.url_categories.list_categories()

            List only custom URL categories:

            >>> zia.url_categories.list_categories(custom_only=True)

        """

        return self._get(f"urlCategories?customOnly={custom_only}", box=BoxList)

    def get_quota(self):
        """
        Returns information on URL category quota usage.

        Returns:
            :obj:`dict`: The URL quota statistics.

        Examples:
            >>> zia.url_categories.get_quota()

        """

        return self._get("urlCategories/urlQuota")

    def get_category(self, category_id: str):
        """
        Returns URL category information for the provided category.

        Args:
            category_id (str):
                The unique identifier for the category (e.g. 'MUSIC')

        Returns:
            :obj:`dict`: The resource record for the category.

        Examples:
            >>> zia.url_categories.get_category('ALCOHOL_TOBACCO')

        """
        return self._get(f"urlCategories/{category_id}")

    def add_url_category(self, name: str, super_category: str, urls: list, **kwargs):
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

        Returns:
            :obj:`dict`: The newly configured custom URL category resource record.

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

    def add_tld_category(self, name: str, tlds: list, **kwargs):
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
            :obj:`dict`: The newly configured custom TLD category resource record.

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

    def update_url_category(self, category_id: str, **kwargs):
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
            :obj:`dict`: The updated URL category resource record.

        Examples:
            Update the name of a category:

            >>> zia.url_categories.update_url_category('CUSTOM_01',
            ...    name="Wines that don't taste good.")

            Update the urls of a category:

            >>> zia.url_categories.update_url_category('CUSTOM_01',
            ...    urls=['www.yellowtailwine.com'])

        """

        # Cache existing record for defaulting mandatory fields that may not require updating.
        category_record = self.get_category(category_id)

        payload = {
            # configuredName required
            "configuredName": kwargs.pop("name", category_record.configured_name)
        }

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        return self._put(f"urlCategories/{category_id}", json=payload)

    def add_urls_to_category(self, category_id: str, urls: list):
        """
        Adds URLS to a URL category.

        Args:
            category_id (str):
                The unique identifier of the URL category.
            urls (list):
                Custom URLs to add to a URL category.

        Returns:
            :obj:`dict`: The updated URL category resource record.

        Examples:
            >>> zia.url_categories.add_urls_to_category('CUSTOM_01',
            ...    urls=['example.com'])

        """

        # Cache existing record for defaulting mandatory fields that may not require updating.
        category_record = self.get_category(category_id)

        payload = {
            "configuredName": category_record.configured_name,  # configuredName required.
            "urls": urls,
        }

        return self._put(
            f"urlCategories/{category_id}?action=ADD_TO_LIST", json=payload
        )

    def delete_urls_from_category(self, category_id: str, urls: list):
        """
        Adds URLS to a URL category.

        Args:
            category_id (str):
                The unique identifier of the URL category.
            urls (list):
                Custom URLs to delete from a URL category.

        Returns:
            :obj:`dict`: The updated URL category resource record.

        Examples:
            >>> zia.url_categories.delete_urls_from_category('CUSTOM_01',
            ...    urls=['example.com'])

        """

        # Cache existing record for defaulting mandatory fields that may not require updating.
        category_record = self.get_category(category_id)

        payload = {
            "configuredName": category_record.configured_name,  # configuredName required.
            "urls": urls,
        }

        return self._put(
            f"urlCategories/{category_id}?action=REMOVE_FROM_LIST", json=payload
        )

    def delete_category(self, category_id: str):
        """
        Deletes the specified URL category.

        Args:
            category_id (str):
                The unique identifier for the category.

        Returns:
            :obj:`str`: The status code for the operation.

        Examples:
            >>> zia.url_categories.delete_category('CUSTOM_01')

        """

        return self._delete(f"urlCategories/{category_id}", box=False).status_code
