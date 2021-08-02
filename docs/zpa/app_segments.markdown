---
layout: default 
title: Application Segments 
parent: ZPA 
nav_order: 3
---

# Overview

Application Segments are used to configure groups of Applications in ZPA.

The following methods are supported by pyZscaler for ZPA Application Segments:

- add_segment()
- delete_segment()
- details()
- list_segments()
- update_segment()

## Adding a ZPA Application Segment
### Prerequisites
You must create the following objects in ZPA before you can add an Application Segment:

- Segment Group
- Server Group

```python
from pyzscaler.zpa import ZPA
from pprint import pprint

zpa = ZPA()

app_segment = zpa.app_segments.add_segment(
    name="Web Frontends",
    domain_names=["webfe.example.com"],
    segment_group="232356567677776",
    server_groups=["232356567677776"],
    tcp_ports=["443"],
)

pprint(app_segment)  # Print the app segment
pprint(app_segment.id)  # Print the app segment ID
```
The `add_segment()` method will return the created Application Segment as a dict and you can access
the keys using dot notation thanks to `box`. In the example above, we can print the entire Application Segment record that's returned or a single key, e.g. `id`.

## Deleting a ZPA Application Segment
Deleting an Application Segment using the ZPA API requires the Application Segment ID. This ID
needs to be provided to the pyZscaler `delete_segment()` method.

The ZPA API provides the HTTP status code as a response and this is returned from the `delete_segment()` method as
a `str`.

```python
from pyzscaler.zpa import ZPA

zpa = ZPA()

zpa.app_segments.delete_segment('232356567677776')
print(zpa.app_segments.delete_segment('232356567677776'))  # Print the status code

# Assign the status code to a variable and then do something with it
status = zpa.app_segments.delete_segment('232356567677776')
if status != '429':
    print('Something went wrong.')
```

## Getting a list of all ZPA Application Segments


```python
from pyzscaler.zpa import ZPA
from pprint import pprint

zpa = ZPA()

# Assign all app segments to a list variable
app_segments = zpa.app_segments.list_segments()

# Iterate over the app segment list and do something
for app_segment in zpa.app_segments.list_segments():
    pprint(app_segment)

```



