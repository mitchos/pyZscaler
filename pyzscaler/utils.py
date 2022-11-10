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
    }
    return edge_cases.get(name, name[0].lower() + name.title()[1:].replace("_", ""))


def chunker(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


# Recursive function to convert all keys and nested keys from snake case
# to camel case.
def convert_keys(data):
    if isinstance(data, (list, BoxList)):
        return [convert_keys(inner_dict) for inner_dict in data]
    elif isinstance(data, (dict, Box)):
        new_dict = {}
        for k in data.keys():
            v = data[k]
            new_key = snake_to_camel(k)
            new_dict[new_key] = convert_keys(v) if isinstance(v, (dict, list)) else v
        return new_dict
    else:
        return data


def keys_exists(element: dict, *keys):
    """
    Check if *keys (nested) exists in `element` (dict).
    """
    if not isinstance(element, dict):
        raise AttributeError("keys_exists() expects dict as first argument.")
    if len(keys) == 0:
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
    for j in range(len(str(r))):
        key += seed[int(str(r)[j]) + 2]

    return {"timestamp": now, "key": key}


def pick_version_profile(kwargs: list, payload: list):
    # Used in ZPA endpoints.
    # This function is used to convert the name of the version profile to
    # the version profile id. This means our users don't need to look up the
    # version profile id mapping themselves.

    version_profile = kwargs.pop("version_profile", None)
    if version_profile:
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
