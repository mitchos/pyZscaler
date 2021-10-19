import time

from box import BoxList
from restfly import APIIterator


def snake_to_camel(name):
    """Converts Python Snake Case to Zscaler's lower camelCase."""
    # Edge-cases where camelCase is breaking
    edge_cases = {
        "routable_ip": "routableIP",
        "is_name_l10n_tag": "isNameL10nTag",
        "name_l10n_tag": "nameL10nTag",
        "surrogate_ip": "surrogateIP",
        "surrogate_ip_enforced_for_known_browsers": "surrogateIPEnforcedForKnownBrowsers",
    }
    ret = edge_cases.get(name, name[0].lower() + name.title()[1:].replace("_", ""))
    return ret


# Takes a tuple if id_groups, kwargs and the payload dict; reformat for API call
def add_id_groups(id_groups, kwargs, payload):
    for entry in id_groups:
        if kwargs.get(entry[0]):
            payload[entry[1]] = [{"id": param_id} for param_id in kwargs.pop(entry[0])]
    return


def obfuscate_api_key(seed):
    now = int(time.time() * 1000)
    n = str(now)[-6:]
    r = str(int(n) >> 1).zfill(6)
    key = "".join(seed[int(str(n)[i])] for i in range(len(str(n))))
    for j in range(len(str(r))):
        key += seed[int(str(r)[j]) + 2]

    return {"timestamp": now, "key": key}


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
        self.page = self._api.get(
            self.path,
            params={**self.payload, "page": self.num_pages + 1},
            box=BoxList,
        )
