from restfly.endpoint import APIEndpoint


class SecurityPolicyAPI(APIEndpoint):
    def get_whitelist(self):
        """
        Returns a list of whitelisted URLs.

        Returns:
            :obj:`list`: A list of whitelisted URLs

        Examples:
            >>> for url in zia.security.get_whitelist():
            ...    pprint(url)

        """
        response = self._get("security")

        # ZIA removes the whitelistUrls key from the JSON response when it's empty.
        if "whitelist_urls" in self._get("security"):
            return response.whitelist_urls
        else:
            return []  # Return empty list so other methods in this class don't break

    def get_blacklist(self):
        """
        Returns a list of blacklisted URLs.

        Returns:
            :obj:`list`: A list of blacklisted URLs

        Examples:
            >>> for url in zia.security.get_blacklist():
            ...    pprint(url)

        """

        return self._get("security/advanced").blacklistUrls

    def erase_whitelist(self):
        """
        Erases all URLs in the whitelist.

        Returns:
            :obj:`str`: The status code for the operation.

        Examples:
            >>> zia.security.erase_whitelist()

        """
        payload = {"whitelistUrls": []}

        return self._put("security", json=payload, box=False).status_code

    def replace_whitelist(self, url_list: list):
        """
        Replaces the existing whitelist with the URLs provided.

        Args:
            url_list (:obj:`list` of :obj:`str`):
                The list of URLs for the new whitelist.

        Returns:
            :obj:`list` of :obj:`str`: The complete and updated whitelist.

        Examples:
            >>> zia.security.replace_whitelist(['example.com'])

        """

        payload = {"whitelistUrls": url_list}

        return self._put("security", json=payload).whitelist_urls

    def add_urls_to_whitelist(self, url_list: list):
        """
        Adds the provided URLs to the whitelist.

        Args:
            url_list (:obj:`list` of :obj:`str`):
                The list of URLs to be added.

        Returns:
            :obj:`list` of :obj:`str`: The complete and updated whitelist.

        Examples:
            >>> zia.security.add_urls_to_whitelist(['example.com', 'web.example.com'])

        """

        # Get the current whitelist
        whitelist = self.get_whitelist()

        # Add existing URLs to whitelist
        whitelist.extend(url for url in url_list if url not in whitelist)

        payload = {"whitelistUrls": whitelist}

        return self._put("security", json=payload).whitelist_urls

    def delete_urls_from_whitelist(self, url_list: list):
        """
        Deletes the provided URLs from the whitelist.

        Args:
            url_list (:obj:`list` of :obj:`str`):
                The list of URLs to be deleted.

        Returns:
            :obj:`list` of :obj:`str`: The complete and updated whitelist.

        Examples:
            >>> zia.security.delete_urls_from_whitelist(['example.com', 'web.example.com'])

        """
        # Get the current whitelist
        whitelist = self.get_whitelist()

        # If URLs provided, create new whitelist without them
        whitelist = [url for url in whitelist if url not in url_list]

        payload = {"whitelistUrls": whitelist}

        return self._put("security", json=payload).whitelist_urls

    def add_urls_to_blacklist(self, url_list: list):
        """
        Adds the provided URLs to the blacklist.

        Args:
            url_list (:obj:`list` of :obj:`str`):
                The list of URLs to be added.

        Returns:
            :obj:`list` of :obj:`str`: The complete and updated blacklist.

        Examples:
            >>> zia.security.add_urls_to_blacklist(['example.com', 'web.example.com'])

        """

        payload = {"blacklistUrls": url_list}

        return self._post(
            "security/advanced/blacklistUrls?action=ADD_TO_LIST",
            json=payload,
            box=False,
        ).status_code

    def replace_blacklist(self, url_list: list):
        """
        Replaces the existing blacklist with the URLs provided.

        Args:
            url_list (:obj:`list` of :obj:`str`):
                The list of URLs for the new blacklist.

        Returns:
            :obj:`list` of :obj:`str`: The complete and updated blacklist.

        Examples:
            >>> zia.security.replace_blacklist(['example.com'])

        """

        payload = {"blacklistUrls": url_list}

        return self._put("security/advanced", json=payload).blacklist_urls

    def erase_blacklist(self):
        """
        Erases all URLs in the blacklist.

        Returns:
            :obj:`str`: The status code for the operation.

        Examples:
            >>> zia.security.erase_blacklist()

        """

        payload = {"blacklistUrls": []}

        return self._put("security/advanced", json=payload, box=False).status_code

    def delete_urls_from_blacklist(self, url_list: list):
        """
        Deletes the provided URLs from the blacklist.

        Args:
            url_list (:obj:`list` of :obj:`str`):
                The list of URLs to be deleted.

        Returns:
            :obj:`list` of :obj:`str`: The complete and updated blacklist.

        Examples:
            >>> zia.security.delete_urls_from_blacklist(['example.com', 'web.example.com'])

        """

        payload = {"blacklistUrls": url_list}

        return self._post(
            "security/advanced/blacklistUrls?action=REMOVE_FROM_LIST",
            json=payload,
            box=False,
        ).blacklist_urls
