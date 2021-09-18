import time

from box import BoxList
from restfly import APIIterator


# Converts Python Snake Case to Zscaler's lower camelCase
def snake_to_camel(name):
    # Edge-cases where camelCase is breaking
    if name == "routable_ip":
        return "routableIP"
    elif name == "is_name_l10n_tag":
        return "isNameL10nTag"
    elif name == "name_l10n_tag":
        return "nameL10nTag"
    else:
        name = name[0].lower() + name.title()[1:].replace("_", "")
    return name


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
    key = ""
    for i in range(0, len(str(n)), 1):
        key += seed[int(str(n)[i])]
    for j in range(0, len(str(r)), 1):
        key += seed[int(str(r)[j]) + 2]

    return {"timestamp": now, "key": key}


class Iterator(APIIterator):
    """
    Iterator class.
    """
    page_size = 100

    def __init__(self, api, path='', **kw):
        """Initialize Iterator class."""
        super().__init__(api, **kw)

        self.path = path

    def _get_page(self) -> None:
        """
        Iterator function to get the page.
        """
        self.page = self._api.get(self.path,
                                  params={"page": self.num_pages + 1, "pageSize": self.page_size},
                                  box=BoxList)
