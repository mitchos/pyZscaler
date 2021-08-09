---
layout: default 
title: Segment Groups
parent: ZPA 
nav_order: 3
---
1. TOC
{:toc}

---
# Overview

Segment Groups are used to configure policies for one or more Application Segments. Application Segments
can only belong to a single Segment Group.

## References
- pyZscaler - Library Reference for Segment Groups
- Zscaler - ZPA Segment Groups API Reference
- Zscaler - ZPA Segment Groups Documentation

## Class Methods
The following methods are supported by pyZscaler for ZPA Segment Groups:

- [`add_group()`](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/segment_groups.html#pyzscaler.zpa.segment_groups.SegmentGroupsAPI.add_group)
- [`delete_group()`](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/segment_groups.html#pyzscaler.zpa.segment_groups.SegmentGroupsAPI.delete_group)
- [`get_group()`](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/segment_groups.html#pyzscaler.zpa.segment_groups.SegmentGroupsAPI.get_group)
- [`list_groups()`](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/segment_groups.html#pyzscaler.zpa.segment_groups.SegmentGroupsAPI.list_groups)
- [`update_group()`](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/segment_groups.html#pyzscaler.zpa.segment_groups.SegmentGroupsAPI.update_group)

## Adding a ZPA Segment Group
This section details how you can add a Segment Group in ZPA using pyZscaler.

### Overview
{: .no_toc }
Unless you know what parameters you want set, you may want to start with an 'empty' Segment Group. You can always
customise the Segment Group later using the `update_group()` method.

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


## Deleting a ZPA Segment Group
This section details how you can delete a Segment Group in ZPA using pyZscaler.

### Prerequisites
{: .no_toc }
You'll need the `id` of the Segment Group that you want to delete.

### Example
{: .no_toc }
```python
from pyzscaler.zpa import ZPA

with ZPA() as zpa:
    
    # Delete the segment group with id of 45096653
    zpa.segment_groups.delete_group('45096653')
```

## Getting information on a ZPA Segment Group
This section details how you can get information on a single Segment Group in ZPA using pyZscaler.

### Example
{: .no_toc }
```python
from pprint import pprint
from pyzscaler.zpa import ZPA

with ZPA() as zpa:
    
    pprint(zpa.segment_groups.get_group('45096653'))
```

## Listing all ZPA Segment Groups

### Example
{: .no_toc }
```python
from pprint import pprint
from pyzscaler.zpa import ZPA

with ZPA() as zpa:
    
    for group in zpa.segment_groups.list_groups():
        pprint(group)
```

## Updating a ZPA Segment Group

### Example
{: .no_toc }
```python
from pyzscaler.zpa import ZPA

with ZPA() as zpa:
    
    zpa.segment_groups.update_group('45096653',
                                    name='Development Apps',
                                    enabled=True)
```