---
layout: default 
title: Application Segments API
parent: ZPA
permalink: /zscaler-sdk/zpa/app-segments-api
---
1. TOC
{:toc}

---

# Zscaler ZPA App Segments API 

## Overview
Application Segments are used to configure groups of Applications in ZPA.

## References
- [pyZscaler - Library Reference for Application Segments](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/app_segments.html){:target="_blank"}
- [Zscaler - ZPA Application Segment API Reference](https://help.zscaler.com/zpa/api-reference#/application-controller){:target="_blank"}
- [Zscaler - ZPA Application Segment Documentation](https://help.zscaler.com/zpa/configuring-application-segments){:target="_blank"}

## Class Methods
The pyZscaler Application Segments module can be accessed via `zpa.app_segments`.

The following methods are supported by pyZscaler for ZPA Application Segments.

- [add_segment()](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/app_segments.html#pyzscaler.zpa.app_segments.AppSegmentsAPI){:target="_blank"}
- [delete_segment()](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/app_segments.html#pyzscaler.zpa.app_segments.AppSegmentsAPI.delete_segment){:target="_blank"}
- [get_segment()](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/app_segments.html#pyzscaler.zpa.app_segments.AppSegmentsAPI.details){:target="_blank"}
- [list_segments()](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/app_segments.html#pyzscaler.zpa.app_segments.AppSegmentsAPI.list_segments){:target="_blank"}
- [update_segment()](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/app_segments.html#pyzscaler.zpa.app_segments.AppSegmentsAPI.update_segment){:target="_blank"}

## Adding a ZPA Application Segment
This section details how you can add an Application Segment in ZPA using pyZscaler.

### Class Methods used
{: .no_toc }
- `add_segment()`

### Prerequisites
{: .no_toc }
You must create the following objects in ZPA before you can add an Application Segment:

- [Segment Group](segment_groups)
- [Server Group](server_groups)

The ZPA API requires the following params to be provided when adding an Application Segment:
- `name`
- `segment_group_id`
- `server_groups`
- `tcp_ports` or `udp_ports`

### Basic Example
{: .no_toc }
We can add a location with the absolute minimum required parameters as per below:

```python
from pyzscaler.zpa import ZPA
from pprint import pprint

zpa = ZPA()

app_segment = zpa.app_segments.add_segment(
    name="Web Frontends",
    domain_names=["webfe.example.com"],
    segment_group_id="916196382959075332",
    server_group_ids=["916196382959075335"],
    tcp_ports=["443", "443"],
)

pprint(app_segment)  # Print the app segment
pprint(app_segment.id)  # Print the app segment ID
```
The `add_segment()` method will return the created Application Segment as a dict and you can access
the keys using dot notation thanks to `box`. In the example above, we can print the entire Application Segment record that's returned or a single key, e.g. `id`.

### Example: Adding a ZPA Application Segment with additional params
{: .no_toc }
We'll use a similar example to our basic one above, but this time we'll use a few more parameters to further
define our Application Segment. It should be fairly obvious what this does, but in summary:

- Create an application segment that covers port `22` (SSH) for access to a development jumpbox accessible
    via `jumpbox.dev.example.com`. There is already a segment group created and a server group for this
    app. We'll enable the application segment, ensure CNAME is being pushed to ZCC and set health reporting to `CONTINUOUS`.

```python
from pyzscaler.zpa import ZPA

zpa = ZPA()

app_segment = zpa.app_segments.add_segment(
    name="Development Jumpbox",
    description="SSH Access to Development Jumpbox",
    domain_names=["jumpbox.dev.example.com"],
    segment_group_id='916197382959075421',
    server_group_ids=["916192562959075224"],
    tcp_ports=["22", "22"],
    enabled=True,
    is_cname_enabled=True,
    health_reporting='CONTINUOUS'
)

```


## Deleting a ZPA Application Segment
This section details how you can delete an Application Segment in ZPA using pyZscaler.

### Class Methods used
{: .no_toc }
- `delete_segment()`

### Overview
{: .no_toc }
Deleting an Application Segment using the ZPA API requires the Application Segment ID. This ID
needs to be provided to the pyZscaler `delete_segment()` method.

The ZPA API provides the HTTP status code as a response and this is returned from the `delete_segment()` method as
a `str`. 

### Prerequisites
{: .no_toc }
You'll need the `id` of the Application Segment you're going to delete.

### Example
{: .no_toc }
We'll delete an Application Segment and add a quick check for the successful deletion code `429` just in case something
goes wrong!

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
This section details how you can get a list of Application Segments in ZPA using pyZscaler.

### Class Methods used
{: .no_toc }
- `list_segments()`

### Overview
{: .no_toc }
There's plenty that you can do with a list of Application Segments. The returned list from this
method will provide all Application Segments with each being its own `dict`. If you familiarise
yourself with the data structure for an Application Segment then you can easily access key
values using `box` notation.

### Example
{: .no_toc }
See the comments in the code block for a description of the different examples.

```python
from pyzscaler.zpa import ZPA
from pprint import pprint

zpa = ZPA()

# We can assign the returned app segment list to a variable
app_segments = zpa.app_segments.list_segments()

# We can iterate over the app segment list and do something
for app_segment in app_segments:

    # Only print the IDs
    print(app_segment.id)

    # Print the name and ports
    print('Name: ', app_segment.name)
    if 'tcp_port_ranges' in app_segment:
        print('TCP Ports: ')
        for port in app_segment.tcp_port_ranges:
            print(port)
    if 'udp_port_ranges' in app_segment:
        print('UDP Ports: ')
        for port in app_segment.udp_port_ranges:
            print(port)
```

## Getting information on a ZPA Application Segment
This section details how you can get information for a single Application Segment in ZPA using pyZscaler.

### Class Methods used
{: .no_toc }
- `get_segment()`

### Overview
{: .no_toc }
The `get_segment()` method is most useful when you want to retrieve some Application Segment properties
to use in another API call. Remember that you can access dict keys using box notation
e.g. `app_segment.id`.

### Prerequisites
{: .no_toc }
You'll need the `id` of the Application Segment to use this method.

### Example
{: .no_toc }
```python
from pyzscaler.zpa import ZPA
from pprint import pprint

zpa = ZPA()

# We can assign the returned app segment list to a variable
app_segment = zpa.app_segments.get_segment('9161963824890752113')

# Print the name of the app segment
print(app_segment.name)

```

## Updating a ZPA Application Segment
This section details how you can update an Application Segment in ZPA using pyZscaler.

### Class Methods used
{: .no_toc }
- `update_segment()`

### Overview
{: .no_toc }
The ZPA API requires you to provide certain parameters in an update API call, even if you aren't modifying them.
pyZscaler simplifies the update process by allowing you to provide only the parameters you want to change. All
other properties for the object will remain unchanged.

### Prerequisites
{: .no_toc }
You'll need the `id` of the Application Segment that you want to update.

### Example
{: .no_toc }
See the comments in the code block for a description of the different examples.


```python
from pyzscaler.zpa import ZPA
from pprint import pprint

zpa = ZPA()

# Update the name of an app segment
zpa.app_segments.update_segment('9161963824890752113',
                                name='Datacenter RDP')

# Disable an app segment
zpa.app_segments.update_segment('9161963824890752113',
                                enabled=False)

# Enable multiple app segments
app_segments = ['9161963824890752114', '9161963824890752115', '9161963824890752116']

for segment_id in app_segments:
    zpa.app_segments.update_segment(segment_id,
                                    enabled=True)

```


