import time


def snake_to_camel(name):
    # Edge-cases where camelCase is breaking
    if name == "routable_ip":
        return "routableIP"
    elif name == "is_name_l10n_tag":
        return "isNameL10nTag"
    else:
        name = name[0].lower() + name.title()[1:].replace("_", "")
    return name


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
