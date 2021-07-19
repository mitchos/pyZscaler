---
layout: default title: ZIA Class parent: ZIA nav_order: 2
---

# ZIA Class

_class_ **ZIA(_\*\*kw_)**
{: .text-purple-100 } {: .bg-grey-lt-000 } A Controller to access Endpoints in the Zscaler Internet Access (ZIA) API.

The ZIA object stores the session token and simplifies access to CRUD options within the ZIA platform.

## ZIA Class Params

| Param        | Type        | Description |
|:-------------|:------------------|:------|
| api_key | str | The ZIA API key generated from the ZIA console.|
| username | str | The ZIA administrator username. |
| password | str | The ZIA administrator password. |
| cloud | str | The cloud that your ZIA tenant is provisioned on. |

# Example

Using environment variables:

```python
import pyZscaler.ZIA

zia = ZIA()
```

Using params:

```python
import pyZscaler.ZIA

zia = ZIA(api_key='', cloud='', username='', password='')
```