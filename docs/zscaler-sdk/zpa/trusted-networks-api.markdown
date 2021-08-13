---
layout: default 
title: Trusted Networks API
parent: ZPA
permalink: /zscaler-sdk/zpa/trusted-networks-api
---
1. TOC
{:toc}

---
# Zscaler ZPA Trusted Networks API

## Overview
Trusted Networks are used in ZPA to identify a network that belongs to your organisation. At the time of publication there
are no public API methods to create, modify or delete a Trusted Network in ZPA. You'll need to create the Trusted 
Network in the UI before you can access that data via the API using pyZscaler.

## References
- [pyZscaler - Library Reference for Trusted Networks](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/trusted_networks.html){:target="_blank"}
- [Zscaler - ZPA Trusted Networks API Reference](https://help.zscaler.com/zpa/api-reference#/trusted-network-controller){:target="_blank"}
- [Zscaler - ZPA Trusted Networks Documentation](https://help.zscaler.com/z-app/about-trusted-networks){:target="_blank"}

## Class Methods
The pyZscaler Trusted Networks Class can be accessed via `zpa.trusted_networks`.

The following methods are supported by pyZscaler for ZPA Trusted Networks:

- [`get_network()`](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/trusted_networks.html#pyzscaler.zpa.trusted_networks.TrustedNetworksAPI.get_network){:target="_blank"}
- [`list_networks()`](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/trusted_networks.html#pyzscaler.zpa.trusted_networks.TrustedNetworksAPI.list_networks){:target="_blank"}

## Getting information on a ZPA Trusted Network
This section details how you get information on a Trusted Network in ZPA using pyZscaler.

### Class Methods used
{: .no_toc }

- `get_network()`

### Prerequisites
{: .no_toc }
You'll need the `id` of the Trusted Network that you want to get information on.

### Example
{: .no_toc }
Print information on a Trusted Network with an `id` of xyz.

```python
from pyzscaler.zpa import ZPA

with ZPA() as zpa:
    
    # Print information on Trusted Network with id 
    pprint(zpa.trusted_networks.get_network(''))
```

## Listing all ZPA Trusted Networks
This section details how you can list all Trusted Networks in ZPA using pyZscaler.

### Class Methods used
{: .no_toc }

- `list_networks()`

### Example
{: .no_toc }
Iterate through all Trusted Networks and print each Trusted Network.

```python
from pyzscaler.zpa import ZPA

with ZPA() as zpa:
    
    # Iterate trusted networks and print each one
    for network in zpa.trusted_networks.list_networks():
        pprint(network)
```

