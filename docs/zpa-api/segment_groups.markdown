---
layout: default 
title: Segment Groups
parent: ZPA 
nav_order: 3
---

# Overview

Segment Groups are used to configure policies for one or more Application Segments. Application Segments
can only belong to a single Segment Group.

## Class Methods
The following methods are supported by pyZscaler for ZPA Segment Groups:

- [`add_group()`](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/segment_groups.html#pyzscaler.zpa.segment_groups.SegmentGroupsAPI.add_group)
- [`delete_group()`](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/segment_groups.html#pyzscaler.zpa.segment_groups.SegmentGroupsAPI.delete_group)
- [`get_group()`](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/segment_groups.html#pyzscaler.zpa.segment_groups.SegmentGroupsAPI.get_group)
- [`list_groups()`](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/segment_groups.html#pyzscaler.zpa.segment_groups.SegmentGroupsAPI.list_groups)
- [`update_group()`](https://pyzscaler.readthedocs.io/en/latest/zs/zpa/segment_groups.html#pyzscaler.zpa.segment_groups.SegmentGroupsAPI.update_group)

## Adding a ZPA Segment Group
The minimum params required to create a Segment Group in ZPA with the API are:

 - `name`

The Segment Group will be in the disabled state unless you pass `enabled=True` upon creation.

### Example

```python
from pyzscaler.zpa import ZPA

with ZPA() as zpa:
    
    # Add a segment group called 'Management Apps' in the disabled state
    zpa.segment_groups.add_group(name='Management Apps')
    
    # Add a segment group called 'Web Apps' in the enabled state
    zpa.segment_groups.add_group(name="Web Apps", enabled=True)
```

## Deleting a ZPA Segment Group

### Example

```python
from pyzscaler.zpa import ZPA

with ZPA() as zpa:
    
    # Delete the segment group with id of 45096653
    zpa.segment_groups.delete_group('45096653')
```

## Getting information for a ZPA Segment Group

### Example
```python
from pprint import pprint
from pyzscaler.zpa import ZPA

with ZPA() as zpa:
    
    pprint(zpa.segment_groups.get_group('45096653'))
```

## Listing all ZPA Segment Groups

### Example

```python
from pprint import pprint
from pyzscaler.zpa import ZPA

with ZPA() as zpa:
    
    for group in zpa.segment_groups.list_groups():
        pprint(group)
```

## Updating a ZPA Segment Group

### Example

```python
from pyzscaler.zpa import ZPA

with ZPA() as zpa:
    
    zpa.segment_groups.update_group('45096653',
                                    name='Development Apps',
                                    enabled=True)
```