---
layout: default 
title: IdP API
parent: ZPA
permalink: /zscaler-sdk/zpa/idp-api
---
1. TOC
{:toc}

---
# Zscaler ZPA IdP API

## Overview
IdPs are used in ZPA to authenticate and authorise users.  

At the time of publication there are no public API methods to create, modify or delete an IdP in ZPA. You'll
need to create IdPs in the UI before you can access that data via the API using pyZscaler.

## References
- [pyZscaler - Library Reference for IdPs](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/idp.html){:target="_blank"}
- [Zscaler - ZPA IdPs API Reference](https://help.zscaler.com/zpa/api-reference#/idp-controller){:target="_blank"}
- [Zscaler - ZPA IdPs Documentation](https://help.zscaler.com/zpa/about-idp-configuration){:target="_blank"}

## Class Methods
The pyZscaler IdPs Class can be accessed via `zpa.idp`.

The following methods are supported by pyZscaler for ZPA IdPs:

- [`get_idp()`](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/idp.html#pyzscaler.zpa.idp.IDPControllerAPI.get_idp){:target="_blank"}
- [`list_idps()`](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/idp.html#pyzscaler.zpa.idp.IDPControllerAPI.list_idps){:target="_blank"}

## Getting information on a ZPA IdP
This section details how you get information on an IdP in ZPA using pyZscaler.

### Class Methods used
{: .no_toc }

- `get_idp()`

### Prerequisites
{: .no_toc }
You'll need the `id` of the IdP that you want to get information on.

### Example
{: .no_toc }
Print information on an IdP with an `id` of xyz.

```python
from pyzscaler.zpa import ZPA

with ZPA() as zpa:
    
    # Print information on an IdP with id 
    pprint(zpa.idp.get_idp(''))
```

## Listing all ZPA IdPs
This section details how you can list all IdPs in ZPA using pyZscaler.

### Class Methods used
{: .no_toc }

- `list_idps()`

### Example
{: .no_toc }
Iterate through all IdPs and print each IdP.

```python
from pyzscaler.zpa import ZPA

with ZPA() as zpa:
    
    # Iterate IdPs and print each one
    for idp in zpa.idp.list_idps():
        pprint(idp)
```

