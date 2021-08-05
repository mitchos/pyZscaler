---
layout: default 
title: ZPA 
permalink: /zpa-api/ 
nav_order: 2 
has_children: true

---

# Getting Started with ZPA

For ZPA, you will need to provide params when initialising the class or set the environment variables.

## Initialising the ZPA instance and returning a list of Application Segments

All examples in this documentation will assume that you are initialising the ZPA Class the same way as shown below.
Ensure that you make adjustments in your code if you are using a different naming convention.

```python
from pyzscaler.zpa import ZPA
from pprint import pprint

zpa = ZPA(client_id='CLIENT_ID', client_secret='CLIENT_SECRET', customer_id='CUSTOMER_ID')

for app_segment in zpa.app_segments.list():
    pprint(app_segment)
```

## ZPA Parameters

The table below shows the parameters that the ZPA Class requires.

| Param        | ENV        | Description |
|:-------------|:------------------|:------|
| client_id           | `ZIA_CLIENT_ID` | The client ID that is associated with the client secret.  |
| client_secret | `ZIA_CLIENT_SECRET`   | The client secret that was generated for the client ID.  |
| customer_id           | `ZPA_CUSTOMER_ID`      | The customer ID for the ZPA tenancy.  |


### How to generate the API Key

See the [ZPA docs](https://help.zscaler.com/zpa/about-api-keys) for how to generate the `client_id`, `client_secret` and find the `customer_id`.




