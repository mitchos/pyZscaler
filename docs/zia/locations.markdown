---
layout: default 
title: Locations 
parent: ZIA 
nav_order: 3
---

# Overview

Locations are used to identify the networks where traffic is coming from in your organisation.

The following methods are supported by pyZscaler for locations:

- add_location()
- delete_location()
- get_location()
- list_locations()
- list_locations_lite()
- list_sub_locations()
- update_location()

## Adding a new location

We need to add a location before we can use locations in our policies. There are a few options that we can use when
creating a location in ZIA, they are:

- Adding a location with an IP address
- Adding a location with whitelisted proxy ports
- Adding a location with VPN credentials

### Adding a location with an IP address

If you're using the ZIA web UI then you can't add an IP address to a location unless it already exists as a static IP.
The API will allow you to add an IP address to a location, but be aware that you'll need to add it to the static IP
list, i.e. the API won't automatically add it there for you.

We can add a location with the absolute minimum required parameters as per below:

```python
from pyzscaler.zia import ZIA

with ZIA(api_key='API_KEY', cloud='CLOUD', username='USERNAME', password='PASSWORD') as zia:
    zia.locations.add_location(name="Sydney Office",
                               ip_addresses=["203.0.113.10"])
```

In reality we would want to define some more parameters to ensure the location information is complete and usable. For
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

## Getting information on an existing location



