import functools
import re
import time

from box import Box, BoxList
from restfly import APIIterator


def snake_to_camel(name: str):
    """Converts Python Snake Case to Zscaler's lower camelCase."""
    if "_" not in name:
        return name
    # Edge-cases where camelCase is breaking
    edge_cases = {
        "routable_ip": "routableIP",
        "is_name_l10n_tag": "isNameL10nTag",
        "name_l10n_tag": "nameL10nTag",
        "surrogate_ip": "surrogateIP",
        "surrogate_ip_enforced_for_known_browsers": "surrogateIPEnforcedForKnownBrowsers",
        "ec_vms": "ecVMs",
        "ipv6_enabled": "ipV6Enabled",
        "valid_ssl_certificate": "validSSLCertificate",
    }
    return edge_cases.get(name, name[0].lower() + name.title()[1:].replace("_", ""))


def camel_to_snake(name: str):
    """Converts Zscaler's lower camelCase to Python Snake Case."""
    edge_cases = {
        "routableIP": "routable_ip",
        "isNameL10nTag": "is_name_l10n_tag",
        "nameL10nTag": "name_l10n_tag",
        "surrogateIP": "surrogate_ip",
        "surrogateIPEnforcedForKnownBrowsers": "surrogate_ip_enforced_for_known_browsers",
        "ecVMs": "ec_vms",
        "ipV6Enabled": "ipv6_enabled",
        "validSSLCertificate": "valid_ssl_certificate",
    }
    # Check if name is an edge case
    if name in edge_cases:
        return edge_cases[name]

    name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", name)
    return name.lower()


def chunker(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def convert_keys(data, direction="to_camel"):
    converter = camel_to_snake if direction == "to_snake" else snake_to_camel

    if isinstance(data, (list, BoxList)):
        return [convert_keys(inner_dict, direction=direction) for inner_dict in data]
    elif isinstance(data, (dict, Box)):
        new_dict = {}
        for k in data.keys():
            v = data[k]
            new_key = converter(k)
            new_dict[new_key] = convert_keys(v, direction=direction) if isinstance(v, (dict, list)) else v
        return new_dict
    else:
        return data


def keys_exists(element: dict, *keys):
    """
    Check if *keys (nested) exists in `element` (dict).
    """
    if not isinstance(element, dict):
        raise AttributeError("keys_exists() expects dict as first argument.")
    if not keys:
        raise AttributeError("keys_exists() expects at least two arguments, one given.")

    _element = element
    for key in keys:
        try:
            _element = _element[key]
        except KeyError:
            return False
    return True


# Takes a tuple if id_groups, kwargs and the payload dict; reformat for API call
def add_id_groups(id_groups: list, kwargs: dict, payload: dict):
    for entry in id_groups:
        if kwargs.get(entry[0]):
            payload[entry[1]] = [{"id": param_id} for param_id in kwargs.pop(entry[0])]
    return


def obfuscate_api_key(seed: list):
    now = int(time.time() * 1000)
    n = str(now)[-6:]
    r = str(int(n) >> 1).zfill(6)
    key = "".join(seed[int(str(n)[i])] for i in range(len(str(n))))
    for j in range(len(r)):
        key += seed[int(r[j]) + 2]

    return {"timestamp": now, "key": key}


def pick_version_profile(kwargs: list, payload: list):
    if version_profile := kwargs.pop("version_profile", None):
        payload["overrideVersionProfile"] = True
        if version_profile == "default":
            payload["versionProfileId"] = 0
        elif version_profile == "previous_default":
            payload["versionProfileId"] = 1
        elif version_profile == "new_release":
            payload["versionProfileId"] = 2


class Iterator(APIIterator):
    """Iterator class."""

    page_size = 100

    def __init__(self, api, path: str = "", **kw):
        """Initialize Iterator class."""
        super().__init__(api, **kw)

        self.path = path
        self.max_items = kw.pop("max_items", 0)
        self.max_pages = kw.pop("max_pages", 0)
        self.payload = {}
        if kw:
            self.payload = {snake_to_camel(key): value for key, value in kw.items()}

    def _get_page(self) -> None:
        """Iterator function to get the page."""
        resp = self._api.get(
            self.path,
            params={**self.payload, "page": self.num_pages + 1},
        )
        try:
            # If we are using ZPA then the API will return records under the
            # 'list' key.
            self.page = resp.get("list") or []
        except AttributeError:
            # If the list key doesn't exist then we're likely using ZIA so just
            # return the full response.
            self.page = resp
        finally:
            # If we use the default retry-after logic in Restfly then we are
            # going to keep seeing 429 messages in stdout. ZIA and ZPA have a
            # standard 1 sec rate limit on the API endpoints with pagination so
            # we are going to include it here.
            time.sleep(1)


class ZDXIterator(APIIterator):
    """
    Iterator class for ZDX endpoints.

    """

    def __init__(self, api, endpoint, limit=None, **kwargs):
        super().__init__(api, **kwargs)
        self.endpoint = endpoint
        self.limit = limit
        self.next_offset = None
        self.total = 0

        # Load the first page
        self._get_page()

    def __next__(self):
        try:
            item = super().__next__()
        except StopIteration:
            if self.next_offset is None:
                # There is no next page, so we're done iterating
                raise
            # There is another page, so get it and continue iterating
            self._get_page()
            item = super().__next__()
        return item

    def _get_page(self):
        params = {"limit": self.limit, "offset": self.next_offset} if self.next_offset else {}

        # Request the next page
        response = self._api.get(self.endpoint, params=params)

        # Extract the next offset and the data items from the response
        self.next_offset = response.get("next_offset")
        self.page = response["users"]

        # Update the total number of records
        self.total += len(self.page)

        # Reset page_count for the new page
        self.page_count = 0


# Maps ZCC numeric os_type and registration_type arguments to a human-readable string
zcc_param_map = {
    "os": {
        "ios": 1,
        "android": 2,
        "windows": 3,
        "macos": 4,
        "linux": 5,
    },
    "reg_type": {
        "all": 0,
        "registered": 1,
        "removal_pending": 3,
        "unregistered": 4,
        "removed": 5,
        "quarantined": 6,
    },
}


def calculate_epoch(hours: int):
    current_time = int(time.time())
    past_time = int(current_time - (hours * 3600))
    return current_time, past_time


def zdx_params(func):
    """
    Decorator to add custom parameter functionality for ZDX API calls.

    Args:
        func: The function to decorate.

    Returns:
        The decorated function.

    """

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        since = kwargs.pop("since", None)
        search = kwargs.pop("search", None)
        location_id = kwargs.pop("location_id", None)
        department_id = kwargs.pop("department_id", None)
        geo_id = kwargs.pop("geo_id", None)

        if since:
            current_time, past_time = calculate_epoch(since)
            kwargs["to"] = current_time
            kwargs["from"] = past_time

        kwargs["q"] = search or kwargs.get("q")
        kwargs["loc"] = location_id or kwargs.get("loc")
        kwargs["dept"] = department_id or kwargs.get("dept")
        kwargs["geo"] = geo_id or kwargs.get("geo")

        return func(self, *args, **kwargs)

    return wrapper
