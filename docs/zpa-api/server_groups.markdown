---
layout: default 
title: Server Groups
parent: ZPA 
nav_order: 3
---
1. TOC
{:toc}

---
# Overview

Server Groups are used within ZPA to define a group of servers that host one or more applications. Application Segments
are assigned to Server Groups.

## References
- [pyZscaler - Library Reference for Server Groups](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/server_groups.html){:target="_blank"}
- [Zscaler - ZPA Server Groups API Reference](https://help.zscaler.com/zpa/api-reference#/server-group-controller){:target="_blank"}
- [Zscaler - ZPA Server Groups Documentation](https://help.zscaler.com/zpa/about-server-groups){:target="_blank"}

## Class Methods
The pyZscaler Server Groups module can be accessed via `zpa.server_groups`.

The following methods are supported by pyZscaler for ZPA Server Groups:

- [`add_group()`](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/server_groups.html#pyzscaler.zpa.server_groups.ServerGroupsAPI.add_group){:target="_blank"}
- [`delete_group()`](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/server_groups.html#pyzscaler.zpa.server_groups.ServerGroupsAPI.delete_group){:target="_blank"}
- [`get_group()`](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/server_groups.html#pyzscaler.zpa.server_groups.ServerGroupsAPI.get_group){:target="_blank"}
- [`list_groups()`](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/server_groups.html#pyzscaler.zpa.server_groups.ServerGroupsAPI.list_groups){:target="_blank"}
- [`update_group()`](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/server_groups.html#pyzscaler.zpa.server_groups.ServerGroupsAPI.update_group){:target="_blank"}

## Adding a ZPA Server Group
This section details how you can add a Server Group in ZPA using pyZscaler.

### Class Methods used
{: .no_toc }

- `add_group()`

### Prerequisites
{: .no_toc }
You must have one or more `app_connector_group_ids` that you want to attach to the Server Group.

### Example
{: .no_toc }
Add a ZPA Server Group with a `name` of _DC1 - Management Zone_ and associate an App Connector with an `id` of _2345324_.


```python
from pyzscaler.zpa import ZPA

with ZPA() as zpa:
    
    # Add a server group called 'DC1 - Management Zone'
    zpa.server_groups.add_group('DC1 - Management Zone',
                                app_connector_ids=['2345324'])
```

### Detailed Example
{: .no_toc }
Add a ZPA Server group with the following configuration:
- Name is _Corporate HQ App Servers_
- App Connector IDs are _234721_ and _234722_
- Application IDs are _926196382959075422_ and _926196382959075423_
- Server IDs are _916196382959075424_ and _916196382959075425_
- Description is _Servers in Corporate HQ Office_
- IP Anchoring is enabled.

```python
from pyzscaler.zpa import ZPA

with ZPA() as zpa:
    zpa.server_groups.add_group('Corporate HQ App Servers',
                                app_connector_ids=['234721', '234722'],
                                application_ids=['926196382959075422', '926196382959075423'],
                                server_ids=['916196382959075424', '916196382959075425'],
                                description='Servers in Corporate HQ Office',
                                ip_anchored=True)
```

## Deleting a ZPA Server Group
This section details how you can delete a Server Group in ZPA using pyZscaler.

### Class Methods used
{: .no_toc }

- `delete_group()`

### Prerequisites
{: .no_toc }
You'll need the `id` of the Server Group you want to delete.

### Example
{: .no_toc }
Delete a Server Group with an `id` of _916196382959075361_.

```python
from pyzscaler.zpa import ZPA

with ZPA() as zpa:
    zpa.server_groups.delete_group('916196382959075361')

```

## Getting information on a ZPA Server Group
This section details how you can get information on a Server Group in ZPA using pyZscaler.

### Class Methods used
{: .no_toc }

- `get_group()`

### Prerequisites
{: .no_toc }
You'll need the `id` of the Server Group that you want to get information on.

### Example
{: .no_toc }
Get information on the Server Group with an `id` of _916196382959075362_.

```python
from pprint import pprint
from pyzscaler.zpa import ZPA

with ZPA() as zpa:
    # Print all information for the server group
    pprint(zpa.server_groups.get_group('916196382959075361'))
    
    # Print the server IDs for the server group
    for server in zpa.server_groups.get_group('916196382959075361').server_ids:
        print(server)

```

## Listing all ZPA Server Groups
This section details how you can list all Server Groups in ZPA using pyZscaler.

### Class Methods used
{: .no_toc }

- `list_groups()`

### Example
{: .no_toc }
Iterate through the list of all Server Groups and print each Server Group.

```python
from pprint import pprint
from pyzscaler.zpa import ZPA

with ZPA() as zpa:
    for group in zpa.server_groups.list_groups():
        pprint(group)

```

## Updating a ZPA Server Group
This section details how you can update a Server Group in ZPA using pyZscaler.

### Class Methods used
{: .no_toc }

- `update_group()`

### Prerequisites
{: .no_toc }
You'll need the `id` of the Server Group that you want to update.

### Example
{: .no_toc }
Update the name and description of a Server Group, enabling Dynamic Discovery.

```python
from pyzscaler.zpa import ZPA

with ZPA() as zpa:
    zpa.server_groups.update_group('916196382959075361',
                                   name='DC_Management_NICs',
                                   description='Management NICs for servers in DC',
                                   dynamic_discovery=True)
```
