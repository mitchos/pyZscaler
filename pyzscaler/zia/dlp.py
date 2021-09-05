from box import BoxList
from restfly.endpoint import APIEndpoint

from pyzscaler.utils import snake_to_camel


class DLPAPI(APIEndpoint):
    def add_dict(self, name, match_type, **kwargs):
        """
        Add a new Patterns and Phrases DLP Dictionary to ZIA.

        Args:
            name (str): The name of the DLP Dictionary.
            match_type (str): The DLP custom phrase/pattern match type. Accepted values are ``all`` or ``any``.
            **kwargs: Optional keyword args.

        Keyword Args:
            description (str): Additional information about the DLP Dictionary.
            phrases (list):
                A list of DLP phrases, with each phrase provided by a tuple following the convention
                (`action`, `pattern`). Accepted actions are ``all`` or ``unique``. E.g.

                .. code-block:: python

                    ('all', 'TOP SECRET')
                    ('unique', 'COMMERCIAL-IN-CONFIDENCE')

            patterns (list):
                A list of DLP patterns, with each pattern provided by a tuple following the convention
                (`action`, `pattern`). Accepted actions are ``all`` or ``unique``. E.g.

                .. code-block:: python

                    ('all', '\d{2} \d{3} \d{3} \d{3}')
                    ('unique', '[A-Z]{6}[A-Z0-9]{2,5}')

        Returns:
            :obj:`dict`: The newly created DLP Dictionary resource record.

        Examples:
            Match text found that contains an IPv4 address using patterns:

            >>> zia.dlp.add_dict(name='IPv4 Addresses',
            ...                description='Matches IPv4 address pattern.',
            ...                match_type='all',
            ...                patterns=[
            ...                    ('all', '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(/(\d|[1-2]\d|3[0-2]))?')
            ...                ]))

            Match text found that contains government document caveats using phrases.

            >>> zia.dlp.add_dict(name='Gov Document Caveats',
            ...                description='Matches government classification caveats.',
            ...                match_type='any',
            ...                phrases=[
            ...                    ('all', 'TOP SECRET'),
            ...                    ('all', 'SECRET'),
            ...                    ('all', 'CONFIDENTIAL')
            ...                ]))

            Match text found that meets the criteria for a Secret Project's document markings using phrases and
            patterns:

            >>> zia.dlp.add_dict(name='Secret Project Documents',
            ...                description='Matches documents created for the Secret Project.',
            ...                match_type='any',
            ...                phrases=[
            ...                    ('all', 'Project Umbrella'),
            ...                    ('all', 'UMBRELLA')
            ...                ],
            ...                patterns=[
            ...                    ('unique', '\d{1,2}-\d{1,2}-[A-Z]{5}')
            ...                ]))

        """

        payload = {
            "name": name,
            "dictionaryType": "PATTERNS_AND_PHRASES",
        }

        # Simplify Zscaler's required values for our users.
        if match_type == "all":
            payload[
                "customPhraseMatchType"
            ] = "MATCH_ALL_CUSTOM_PHRASE_PATTERN_DICTIONARY"
        elif match_type == "any":
            payload[
                "customPhraseMatchType"
            ] = "MATCH_ANY_CUSTOM_PHRASE_PATTERN_DICTIONARY"
        else:
            raise ValueError

        if kwargs.get("patterns"):
            for pattern in kwargs.pop("patterns"):
                payload.setdefault("patterns", []).append(
                    {
                        "action": f"PATTERN_COUNT_TYPE_{pattern[0].upper()}",
                        "pattern": pattern[1],
                    }
                )

        if kwargs.get("phrases"):
            for phrase in kwargs.pop("phrases"):
                payload.setdefault("phrases", []).append(
                    {
                        "action": f"PHRASE_COUNT_TYPE_{phrase[0].upper()}",
                        "phrase": phrase[1],
                    }
                )

        # Update payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        return self._post("dlpDictionaries", json=payload)

    def update_dict(self, dict_id, **kwargs):
        """
        Updates the specified DLP Dictionary.

        Args:
            dict_id (str): The unique id of the DLP Dictionary.
            **kwargs: Optional keyword args.

        Keyword Args:
            description (str): Additional information about the DLP Dictionary.
            match_type (str): The DLP custom phrase/pattern match type. Accepted values are ``all`` or ``any``.
            name (str): The name of the DLP Dictionary.
            phrases (list):
                A list of DLP phrases, with each phrase provided by a tuple following the convention
                (`action`, `pattern`). Accepted actions are ``all`` or ``unique``. E.g.

                .. code-block:: python

                    ('all', 'TOP SECRET')
                    ('unique', 'COMMERCIAL-IN-CONFIDENCE')

            patterns (list):
                A list of DLP pattersn, with each pattern provided by a tuple following the convention
                (`action`, `pattern`). Accepted actions are ``all`` or ``unique``. E.g.

                .. code-block:: python

                    ('all', '\d{2} \d{3} \d{3} \d{3}')
                    ('unique', '[A-Z]{6}[A-Z0-9]{2,5}')

        Returns:
            :obj:`dict`: The updated DLP Dictionary resource record.

        Examples:
            Update the name of a DLP Dictionary:

            >>> zia.dlp.update_dict('3',
            ...                name='IPv4 and IPv6 Addresses')

            Update the description and phrases for a DLP Dictionary.

            >>> zia.dlp.update_dict('4',
            ...        description='Updated government caveats.'
            ...        phrases=[
            ...                    ('all', 'TOP SECRET'),
            ...                    ('all', 'SECRET'),
            ...                    ('all', 'PROTECTED')
            ...                ])

        """

        # Set payload to value of existing record
        payload = {snake_to_camel(k): v for k, v in self.get_dict(dict_id).items()}

        if kwargs.get("match_type"):
            match_type = kwargs.pop("match_type")
            if match_type == "all":
                payload[
                    "customPhraseMatchType"
                ] = "MATCH_ALL_CUSTOM_PHRASE_PATTERN_DICTIONARY"
            elif match_type == "any":
                payload[
                    "customPhraseMatchType"
                ] = "MATCH_ANY_CUSTOM_PHRASE_PATTERN_DICTIONARY"
            else:
                raise ValueError

        # If patterns or phrases provided, overwrite existing values
        if kwargs.get("patterns"):
            payload["patterns"] = []
            for pattern in kwargs.pop("patterns"):
                payload.setdefault("patterns", []).append(
                    {
                        "action": f"PATTERN_COUNT_TYPE_{pattern[0].upper()}",
                        "pattern": pattern[1],
                    }
                )

        if kwargs.get("phrases"):
            payload["phrases"] = []
            for phrase in kwargs.pop("phrases"):
                payload["phrases"].append(
                    {
                        "action": f"PHRASE_COUNT_TYPE_{phrase[0].upper()}",
                        "phrase": phrase[1],
                    }
                )

        # Update payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        return self._put(f"dlpDictionaries/{dict_id}", json=payload)

    def list_dicts(self, query: str = None):
        """
        Returns a list of all custom and predefined ZIA DLP Dictionaries.

        Args:
            query (str): A search string used to match against a DLP dictionary's name or description attributes.

        Returns:
            :obj:`list`: A list containing ZIA DLP Dictionaries.

        Examples:
            Print all dictionaries

            >>> for dictionary in zia.dlp.list_dicts():
            ...    pprint(dictionary)

            Print dictionaries that match the name or description 'GDPR'

            >>> pprint(zia.dlp.list_dicts('GDPR'))

        """
        payload = {"search": query}
        return self._get("dlpDictionaries", params=payload, box=BoxList)

    def get_dict(self, dict_id: str):
        """
        Returns the DLP Dictionary that matches the specified DLP Dictionary id.

        Args:
            dict_id (str): The unique id for the DLP Dictionary.

        Returns:
            :obj:`dict`: The ZIA DLP Dictionary resource record.

        Examples:
            >>> pprint(zia.dlp.get_dict('3'))

        """

        return self._get(f"dlpDictionaries/{dict_id}")

    def delete_dict(self, dict_id: str):
        """
        Deletes the DLP Dictionary that matches the specified DLP Dictionary id.

        Args:
            dict_id (str): The unique id for the DLP Dictionary.

        Returns:
            :obj:`str`: The status code for the operation.

        Examples:
            >>> zia.dlp.delete_dict('8')

        """
        return self._delete(f"dlpDictionaries/{dict_id}", box=False).status_code

    def validate_dict(self, pattern):
        """
        Validates the provided pattern for usage in a DLP Dictionary.

        Note: The ZIA API documentation doesn't provide information on how to structure a request for this API endpoint.
         This endpoint is returning a valid response but validation isn't failing for obvious wrong patterns. Use at
         own risk.

        Args:
            pattern (str): DLP Pattern for evaluation.

        Returns:
            :obj:`dict`: Information on the provided pattern.

        """
        payload = {"data": pattern}

        return self._post("dlpDictionaries/validateDlpPattern", data=payload)
