---
layout: default 
title: Locations 
parent: ZIA 
nav_order: 3
---
1. TOC
{:toc}

---

# Locations Overview

Locations are used to identify the networks where traffic is coming from in your organisation.

## Class Methods
The following methods are supported by pyZscaler for locations:

- [`add_location()`](https://pyzscaler.readthedocs.io/en/latest/zs/zia/locations.html#pyzscaler.zia.locations.LocationsAPI.add_location){:target="_blank"}
- [`delete_location()`](https://pyzscaler.readthedocs.io/en/latest/zs/zia/locations.html#pyzscaler.zia.locations.LocationsAPI.delete_location){:target="_blank"}
- [`get_location()`](https://pyzscaler.readthedocs.io/en/latest/zs/zia/locations.html#pyzscaler.zia.locations.LocationsAPI.get_location){:target="_blank"}
- [`list_locations()`](https://pyzscaler.readthedocs.io/en/latest/zs/zia/locations.html#pyzscaler.zia.locations.LocationsAPI.list_locations){:target="_blank"}
- [`list_locations_lite()`](https://pyzscaler.readthedocs.io/en/latest/zs/zia/locations.html#pyzscaler.zia.locations.LocationsAPI.list_locations_lite){:target="_blank"}
- [`list_sub_locations()`](https://pyzscaler.readthedocs.io/en/latest/zs/zia/locations.html#pyzscaler.zia.locations.LocationsAPI.list_sub_locations){:target="_blank"}
- [`update_location()`](https://pyzscaler.readthedocs.io/en/latest/zs/zia/locations.html#pyzscaler.zia.locations.LocationsAPI.update_location){:target="_blank"}

## Obtaining a Location `id`
Many of the methods in the `locations` class require the location `id`, this can be obtained
via the following methods:

- `list_locations()`
- `list_locations_lite()`
- `get_location()`

The location `id` is also returned as part of the created or updated location dict via the following methods:

- `add_location()`
- `update_location()`

## Adding a new location
We need to add a location before we can use locations in our policies. 

### Class Methods Used
{: .no_toc }
- `add_location()`

### Basic Example
{: .no_toc }
We can add a location with the absolute minimum required parameters as per below:

```python
from pyzscaler.zia import ZIA

with ZIA(api_key='API_KEY', cloud='CLOUD', username='USERNAME', password='PASSWORD') as zia:
    zia.locations.add_location(name="Sydney Office",
                               ip_addresses=["203.0.113.10"])
```

### Location Options
{: .no_toc }
There are a few options that we can use when creating a location in ZIA, they are:

- Adding a location with an IP address
- Adding a location with proxy ports
- Adding a location with VPN credentials

### Adding a location with an IP address
{: .no_toc }


#### Prerequisites
{: .no_toc }
If you're using the ZIA web UI then you can't add an IP address to a location unless it already exists as a static IP.
The API will allow you to add an IP address to a location, but be aware that you'll need to add it to the static IP
list, i.e. the API won't automatically add it there for you.

#### Example
{: .no_toc }
In reality, we would want to define some more parameters to ensure the location information is complete and usable. For
this example location, we'll add the following:

- Country
- Timezone
- Require authentication
- Enable the firewall
- Enable the AUP (acceptable use policy)
- Set the traffic profile to corporate
- Description of the location

```python
from pyzscaler.zia import ZIA

with ZIA(api_key='API_KEY', cloud='CLOUD', username='USERNAME', password='PASSWORD') as zia:
    sydney_office = zia.locations.add_location(name="Sydney Office",
                                               description='Sydney Corporate Office located at 123 Example St',
                                               ip_addresses=["203.0.113.10"],
                                               auth_required=True,
                                               aup_enabled=True,
                                               ofw_enabled=True,
                                               profile="CORPORATE",
                                               country="AUSTRALIA",
                                               tz="AUSTRALIA_SYDNEY")

    print(sydney_office)  # Prints the entire dict
    print(sydney_office.ip_addresses)  # Prints the list of IP addresses
    print(sydney_office.tz)  # Prints the timezone
```

We've assigned the returned resource record for Sydney office to the ``sydney_office`` variable. This is returned as
a ``dict`` and allows us to access those keys using dot notation thanks to `box`.

### Adding a Location with Proxy Ports
{: .no_toc }

#### Prerequisites
{: .no_toc }
Before you can add a location with Proxy Ports, your organisation must have a spare whitelisted Proxy Port available.

- Authentication must be enabled when using Proxy Ports
- There is a 1:1 relationship between Locations and Proxy Ports in ZIA. 

#### Example
{: .no_toc }
We'll use a similar construct to our Sydney office in the previous example but this time there are no Static IPs 
associated with this location. We'll use the whitelisted Proxy Port of 10579 to identify traffic from this 
location.

```python
from pyzscaler.zia import ZIA

with ZIA(api_key='API_KEY', cloud='CLOUD', username='USERNAME', password='PASSWORD') as zia:
    sydney_office = zia.locations.add_location(name="Melbourne Office",
                                               description='Melbourne Corporate Office located at 456 Fake St',
                                               auth_required=True,
                                               aup_enabled=True,
                                               ofw_enabled=True,
                                               ports=['10579'],
                                               profile="CORPORATE",
                                               country="AUSTRALIA",
                                               tz="AUSTRALIA_MELBOURNE")
```

### Adding a Location with VPN Credentials
{: .no_toc }
#### Prerequisites
{: .no_toc }
Before you can add a Location with VPN Credentials, you must create the VPN Credential that you're going to
use to identify traffic from this location.

#### Example
{: .no_toc }
Following our Australian branch office theme from previous examples, we'll create a new location for Brisbane.
This time we'll pass the ID of the VPN credentials that already exist via the `vpn_credentials` parameter.

```python
from pyzscaler.zia import ZIA

with ZIA(api_key='API_KEY', cloud='CLOUD', username='USERNAME', password='PASSWORD') as zia:
    sydney_office = zia.locations.add_location(name="Brisbane Office",
                                               description='Brisbane Corporate Office located at 789 Business St',
                                               auth_required=True,
                                               aup_enabled=True,
                                               ofw_enabled=True,
                                               vpn_credentials=['4562873'],
                                               profile="CORPORATE",
                                               country="AUSTRALIA",
                                               tz="AUSTRALIA_MELBOURNE")
```

## Deleting a Location
This section details how you can delete a location that's configured in ZIA using pyZscaler.

### Class Methods Used
{: .no_toc }
- `delete_location()`

### Prerequisites
{: .no_toc }
- Location `id` of the location you are deleting. 
  - [How to obtain the location `id`](#obtaining-a-location-id).

### Example
{: .no_toc }
Delete a location with the `id` of _97456691_.

```python
from pyzscaler.zia import ZIA

with ZIA(api_key='API_KEY', cloud='CLOUD', username='USERNAME', password='PASSWORD') as zia:
    zia.locations.delete_location('97456691')
    
    # Print the HTTP response status code
    print(zia.locations.delete_location('97456691')) 
```


## Getting Location Information
This section details how you can get information for a location that's configured in ZIA using pyZscaler.

### Class Methods Used
{: .no_toc }
- `get_location()`

### Prerequisites
{: .no_toc }
- Location `id` for the location you are looking up. 
  - [How to obtain the location `id`](#obtaining-a-location-id).

### Example
{: .no_toc }
Get information for a location with the `id` of _97456691_.

```python
from pprint import pprint
from pyzscaler.zia import ZIA

with ZIA(api_key='API_KEY', cloud='CLOUD', username='USERNAME', password='PASSWORD') as zia:
    office_location = zia.locations.get_location('97456691')
    
    # Print the returned office location dict
    pprint(office_location)
```

## Listing Locations
This section details how you can get a list of locations that are configured in ZIA using pyZscaler.

### Class methods used
{: .no_toc }

- `list_locations()`
- `list_locations_lite()`
- `list_sub_locations()`

### Listing all locations
{: .no_toc }

#### Example
{: .no_toc }

This example shows the following:

- Print information for all locations
- Print only the name of all locations
- Print only locations where the country is _Australia_

```python
from pprint import pprint
from pyzscaler.zia import ZIA

with ZIA(api_key='API_KEY', cloud='CLOUD', username='USERNAME', password='PASSWORD') as zia:
    
    # Print all information for all locations
    for location in zia.locations.list_locations():
        pprint(location)
    
    # Print only the name of all locations    
    for location in zia.locations.list_locations():
        pprint(location.name)
    
    # Print only locations located in Australia
    australian_locations = [x for x in zia.locations.list_locations() if 'country' in x and x.country == "AUSTRALIA"]
    for location in australian_locations:
        pprint(location)

```

### Listing only `id` and `name` for all locations
{: .no_toc }

This section details how you can list only the `id` and `name` for all locations in ZIA using pyZscaler.

#### Example
{: .no_toc }

Print the location `id` and `name` for all locations:

```python
from pprint import pprint
from pyzscaler.zia import ZIA

with ZIA(api_key='API_KEY', cloud='CLOUD', username='USERNAME', password='PASSWORD') as zia:
    
    # Print location id and name for all locations
    for location in zia.locations.list_locations_lite():
        pprint(location)
```

### Listing all sub-locations for a location
{: .no_toc }

This section details how you can list all sub-locations for a location in ZIA using pyZscaler.

#### Prerequisites
{: .no_toc }

- Parent location `id` that the sub-locations belong to. 
  - [How to obtain the location `id`](#obtaining-a-location-id).

#### Example
{: .no_toc }

List all sub-locations for location with `id` of _97456691_.

```python
from pprint import pprint
from pyzscaler.zia import ZIA

with ZIA(api_key='API_KEY', cloud='CLOUD', username='USERNAME', password='PASSWORD') as zia:
    
    # Print all information for all sub-locations
    for sub_location in zia.locations.list_sub_locations('97456691'):
        pprint(sub_location)
```


## Updating a Location
This section details how you can update a location that already exists in ZIA using pyZscaler.

### Class methods used
{: .no_toc }

- `update_location()`

### Prerequisites
{: .no_toc }

- Location `id` for the location you want to update.
  - [How to obtain the location `id`](#obtaining-a-location-id).

### Example
{: .no_toc }

This example shows the following:

- Update the name of the Canberra location with `id` of _97456691_.
- Update the name, IP addresses and disable the firewall of the Canberra location with `id` of _97456691_.

```python
from pyzscaler.zia import ZIA

with ZIA(api_key='API_KEY', cloud='CLOUD', username='USERNAME', password='PASSWORD') as zia:

    # Update the name only
    zia.locations.update_location('97456691',
                                  name='Canberra Office')
    
    # Update the name, IP addresses and disable the firewall
    zia.locations.update_location('97456691',
                                  name='Canberra Office',
                                  ip_addresses=['203.0.113.11', '203.0.113.12'],
                                  ofw_enabled=False)
```

