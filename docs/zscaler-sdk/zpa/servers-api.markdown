---
layout: default 
title: Servers API
parent: ZPA
permalink: /zscaler-sdk/zpa/servers-api
---
1. TOC
{:toc}

---
# Zscaler ZPA Servers API

## Overview

Server objects in ZPA are used to define the virtual or physical servers that host an application.

When you define a Server using the ZPA API, you'll also want to assign it to a [Server Group](server-groups-api) so that you
can assign it to an [Application Segment](app-segments-api).

## References
- [pyZscaler - Library Reference for Servers](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/servers.html){:target="_blank"}
- [Zscaler - ZPA Servers API Reference](https://help.zscaler.com/zpa/api-reference#/app-server-controller){:target="_blank"}
- [Zscaler - ZPA Servers Documentation](https://help.zscaler.com/zpa/about-servers){:target="_blank"}

## Class Methods
The pyZscaler Servers Class can be accessed via `zpa.servers`.

The following methods are supported by pyZscaler for ZPA Servers:

- [`add_server()`](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/servers.html#pyzscaler.zpa.servers.AppServersAPI.add_server){:target="_blank"}
- [`delete_server()`](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/servers.html#pyzscaler.zpa.servers.AppServersAPI.delete_server){:target="_blank"}
- [`get_server()`](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/servers.html#pyzscaler.zpa.servers.AppServersAPI.get_server){:target="_blank"}
- [`list_servers()`](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/servers.html#pyzscaler.zpa.servers.AppServersAPI.list_servers){:target="_blank"}
- [`update_server()`](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/servers.html#pyzscaler.zpa.servers.AppServersAPI.update_server){:target="_blank"}

## Adding a ZPA Server
This section details how you can add a Server in ZPA using pyZscaler.

### Class Methods used
{: .no_toc }

- `add_server()`

### Prerequisites
{: .no_toc }
The following parameters are required to add a new server:

- `name`
- `address`

### Example
{: .no_toc }
Adding a server with a `name` of _mgmt.server.dc.example.com_ and `address` of _192.0.2.10_. We won't be setting
`enabled` to _True_ in this case; the server will be left in the disabled state.

```python
from pyzscaler.zpa import ZPA

with ZPA() as zpa:
    
    # Add a server called mgmt.server.dc.example.com
    zpa.servers.add_server('mgmt.server.dc-p.example.com',
                           address='192.0.2.10')
```

### Detailed Example
{: .no_toc }

Add a server with the following configuration:

- Server name is _webfe.server.dc-p.example.com_
- IP address is _192.0.2.11_
- Description is _Web Frontend Server in Primary DC_
- Assign Server to Server Group with ID of _916196382959075481_
- Enable the server

```python
from pyzscaler.zpa import ZPA

with ZPA() as zpa:
    
    # Add a server called mgmt.server.dc.example.com
    zpa.servers.add_server('webfe.server.dc-p.example.com',
                           address='192.0.2.11',
                           description='Web Frontend Server in Primary DC',
                           app_server_group_ids=['916196382959075481'],
                           enabled=True)
```

## Deleting a ZPA Server
This section details how you can delete a Server in ZPA using pyZscaler.

### Class Methods used
{: .no_toc }

- `delete_server()`

### Prerequisites
{: .no_toc }
You'll need the `id` of the server you want to delete.

### Example
{: .no_toc }
Delete a ZPA Server with an `id` of _716195282989075421_.

```python
from pyzscaler.zpa import ZPA

with ZPA() as zpa:
    
    zpa.servers.delete_server('716195282989075421')
```

## Getting information on a ZPA Server
This section details how you can get information on a Server in ZPA using pyZscaler.

### Class Methods used
{: .no_toc }

- `get_server()`

### Prerequisites
{: .no_toc }

### Example
{: .no_toc }
Print information for a ZPA Server with an `id` of `716195282989075422`.

```python
from pprint import pprint
from pyzscaler.zpa import ZPA

with ZPA() as zpa:
    
    # Print all information for the server
    pprint(zpa.servers.get_server('716195282989075422'))

    ## Print the server groups that this server belongs to
    server = zpa.servers.get_server('716195282989075422')
    try:
        for group_id in server['app_server_group_ids']:
            print(group_id)
    except KeyError:
        print('No Server Groups.')

```

## Listing all ZPA Servers
This section details how you can list all Servers in ZPA using pyZscaler.

### Class Methods used
{: .no_toc }

- `list_servers()`

### Example
{: .no_toc }
Iterate through the list of ZPA Servers and print information for each Server.

```python
from pprint import pprint
from pyzscaler.zpa import ZPA

with ZPA() as zpa:
    
    # Iterate server list and print each server record
    for server in zpa.servers.list_servers():
        pprint(server)
```

## Updating a ZPA Server
This section details how you can update a Server Group in ZPA using pyZscaler.

### Class Methods used
{: .no_toc }

- `update_server()`

### Prerequisites
{: .no_toc }
You'll need the `id` for the Server that you want to update.

### Example
{: .no_toc }

- Update a Server of `id` of _716195282989075425_ 
- Change the `name` to _DC Jumpbox_ 
- Add Server to an `app_server_group_id` of _916196382959075481_.

```python
from pprint import pprint
from pyzscaler.zpa import ZPA

with ZPA() as zpa:
    
    # Update server with id of 716195282989075425
    zpa.servers.update_server('716195282989075425',
                              name='DC Jumpbox',
                              app_server_group_ids=['916196382959075481'])
```
