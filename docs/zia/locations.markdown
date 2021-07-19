---
layout: default title: locations parent: ZIA nav_order: 3
---

# locations

The following methods allow for interaction with the ZIA Location Management API endpoints.

Access methods via `ZIA.locations`

## list_locations()

Returns a list of configured locations.

### Example

```python
import pyZscaler.ZIA
import pprint

zia = ZIA()

for location in zia.locations.list_locations():
    pprint(location)

```


