---
layout: default 
title: Segment Groups API
parent: ZPA
permalink: /zscaler-sdk/zpa/segment-groups-api
---

1. TOC 
{:toc}

---

# Zscaler ZPA Segment Groups API 

## Overview

Segment Groups are used to configure policies for one or more Application Segments. Application Segments can only belong
to a single Segment Group.

Creating a Segment Group is a prerequisite for adding an Application Segment.

## References

- [pyZscaler - Library Reference for Segment Groups](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/segment_groups.html){:target="_blank"}
- [Zscaler - ZPA Segment Groups API Reference](https://help.zscaler.com/zpa/api-reference#/segment-group-controller){:target="_blank"}
- [Zscaler - ZPA Segment Groups Documentation](https://help.zscaler.com/zpa/about-segment-groups){:target="_blank"}

## Class Methods
The pyZscaler Segment Groups Class can be accessed via `zpa.segment_groups`.

The following methods are supported by pyZscaler for ZPA Segment Groups:

- [`add_group()`](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/segment_groups.html#pyzscaler.zpa.segment_groups.SegmentGroupsAPI.add_group){:target="_blank"}
- [`delete_group()`](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/segment_groups.html#pyzscaler.zpa.segment_groups.SegmentGroupsAPI.delete_group){:target="_blank"}
- [`get_group()`](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/segment_groups.html#pyzscaler.zpa.segment_groups.SegmentGroupsAPI.get_group){:target="_blank"}
- [`list_groups()`](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/segment_groups.html#pyzscaler.zpa.segment_groups.SegmentGroupsAPI.list_groups){:target="_blank"}
- [`update_group()`](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/segment_groups.html#pyzscaler.zpa.segment_groups.SegmentGroupsAPI.update_group){:target="_blank"}

## Adding a ZPA Segment Group
This section details how you can add a Segment Group via API in ZPA using pyZscaler.

### Overview
{: .no_toc } 
If you don't know which applications you want to associate with the Segment Group (or they haven't been
created yet), you may want to start with a basic config that only has a name. You can always customise the Segment Group
later using the `update_group()` method.

### Class Methods used
{: .no_toc }

- `add_group()`

### Prerequisites
{: .no_toc } 
The minimum params required to create a Segment Group in ZPA with the API are:

- `name`

The Segment Group will be in the disabled state unless you pass `enabled=True` upon creation.

### Example
{: .no_toc } 
We can add a Segment Group with the absolute minimum required parameters as per below:

```python
from pyzscaler.zpa import ZPA

with ZPA() as zpa:
    # Add a segment group called 'Management Apps' in the disabled state
    zpa.segment_groups.add_group(name='Management Apps')

    # Add a segment group called 'Web Apps' in the enabled state
    zpa.segment_groups.add_group(name="Web Apps", enabled=True)
```

### Detailed Example
{: .no_toc }
In this example we're going to add a Segment Group via API in ZPA with the following configuration:

- Name is _Remote Access_
- Segment Group is _enabled_
- Description is _Remote Acccess Applications_
- Application IDs to associate are _926196382959075422_, _926196382959075423_ and _926196382959075424_.

```python
from pyzscaler.zpa import ZPA

with ZPA() as zpa:
    # Add a segment group called 'Remote Access' and associate some applications
    zpa.segment_groups.add_group(name='Remote Access',
                                 enabled=True,
                                 description='Remote Access Applications',
                                 application_ids=[
                                     '926196382959075422',
                                     '926196382959075423',
                                     '926196382959075424'])

```

## Deleting a ZPA Segment Group
This section details how you can delete a Segment Group via API in ZPA using pyZscaler.

### Class Methods used
{: .no_toc }

- `delete_group()`

### Prerequisites
{: .no_toc } 
You'll need the `id` of the Segment Group that you want to delete.

### Example
{: .no_toc }
Delete a Segment Group with the `id` _45096653_.

```python
from pyzscaler.zpa import ZPA

with ZPA() as zpa:
    # Delete the segment group with id of 45096653
    zpa.segment_groups.delete_group('45096653')
```

## Getting information on a ZPA Segment Group
This section details how you can get information on a single Segment Group via API in ZPA using pyZscaler.

### Class Methods used
{: .no_toc }

- `get_group()`

### Prerequisites
{: .no_toc }
You'll need the `id` of the Segment Group that you want information on.

### Example
{: .no_toc }
Get information for a Segment Group with an `id` of _45096653_.

```python
from pprint import pprint
from pyzscaler.zpa import ZPA

with ZPA() as zpa:
    pprint(zpa.segment_groups.get_group('45096653'))
```

## Listing all ZPA Segment Groups
This section details how you can list all Segment Groups via API in ZPA using pyZscaler.

### Class Methods used
{: .no_toc }

- `list_groups()`

### Example
{: .no_toc }
Iterate through Segment Groups list and print each configured Segment Group.
{: .no_toc }

```python
from pprint import pprint
from pyzscaler.zpa import ZPA

with ZPA() as zpa:
    for group in zpa.segment_groups.list_groups():
        pprint(group)
```

## Updating a ZPA Segment Group
This section details how you can update a Segment Group via API in ZPA using pyZscaler.

### Class Methods used
{: .no_toc }

- `update_group()`

### Prerequisites
{: .no_toc }
You'll need the `id` of the Segment Group that you want to update. 

### Example
{: .no_toc }
Update the name of a Segment Group to _Development Apps_ and enable it.


```python
from pyzscaler.zpa import ZPA

with ZPA() as zpa:
    zpa.segment_groups.update_group('45096653',
                                    name='Development Apps',
                                    enabled=True)
```