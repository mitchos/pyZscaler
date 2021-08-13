---
layout: default 
title: Machine Groups API
parent: ZPA
permalink: /zscaler-sdk/zpa/machine-groups-api
---
1. TOC
{:toc}

---
# Zscaler ZPA Machine Groups API

## Overview
Machine Groups are used in ZPA to identify individual devices that will connect to ZPA via tunnel before the user has
logged-in to Windows.  

At the time of publication there are no public API methods to create, modify or delete a Machine Group in ZPA. You'll
need to create Machine Groups in the UI before you can access that data via the API using pyZscaler.

## References
- [pyZscaler - Library Reference for Machine Groups](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/machine_groups.html){:target="_blank"}
- [Zscaler - ZPA Machine Groups API Reference](https://help.zscaler.com/zpa/api-reference#/machine-group-controller){:target="_blank"}
- [Zscaler - ZPA Machine Groups Documentation](https://help.zscaler.com/zpa/about-machine-groups){:target="_blank"}

## Class Methods
The pyZscaler Machine Groups Class can be accessed via `zpa.machine_groups`.

The following methods are supported by pyZscaler for ZPA Machine Groups:

- [`get_machine_group()`](){:target="_blank"}
- [`list_machine_groups()`](){:target="_blank"}

## Getting information on a ZPA Machine Group
This section details how you get information on a Machine Group in ZPA using pyZscaler.

### Class Methods used
{: .no_toc }

- `get_machine_group()`

### Prerequisites
{: .no_toc }
You'll need the `id` of the Machine Group that you want to get information on.

### Example
{: .no_toc }
Print information on a Machine Group with an `id` of _916196382959075882_.

```python
from pyzscaler.zpa import ZPA

with ZPA() as zpa:
    
    # Print information on an Machine Group with id 916196382959075882
    pprint(zpa.machine_groups.get_machine_groups('916196382959075882'))
```

## Listing all ZPA Machine Groups
This section details how you can list all Machine Groups in ZPA using pyZscaler.

### Class Methods used
{: .no_toc }

- `list_machine_groups()`

### Example
{: .no_toc }
Iterate through all Machine Groups and print each Machine Group.

```python
from pyzscaler.zpa import ZPA

with ZPA() as zpa:
    
    # Iterate Machine Groups and print each one
    for machine_group in zpa.machine_groups.list_machine_groupss():
        pprint(machine_group)
```

