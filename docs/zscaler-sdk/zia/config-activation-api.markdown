---
layout: default 
title:  Config Activation API
parent: ZIA
permalink: /zscaler-sdk/zia/config-activation-api
---
1. TOC
{:toc}

---

# Zscaler ZIA Config Activation API 

## Overview

Configuration changes in ZIA go into a staging state until activated. 

## Class Methods
{: .no_toc }
The following methods are supported by pyZscaler for config activation:

- [`activate()`](https://pyzscaler.readthedocs.io/en/latest/zs/zia/config.html#pyzscaler.zia.config.ActivationAPI){:target="_blank"}
- [`status()`](https://pyzscaler.readthedocs.io/en/latest/zs/zia/config.html#pyzscaler.zia.config.ActivationAPI.status){:target="_blank"}

## Activating configuration
This section shows how to activate configuration changes using pyZscaler.

### Prerequisites
{: .no_toc }
There must be configuration changes that are staged and ready to be activated. 

### Example
{: .no_toc }
```python
from pyzscaler.zia import ZIA

with ZIA(api_key='API_KEY', cloud='CLOUD', username='USERNAME', password='PASSWORD') as zia:
    # Activate the config
    zia.config.activate()
    
    # Activate the config and print the status
    status = zia.config.activate()
    print(status)

```

## Checking the configuration activation status
This section shows how to check the current configuration activation status.

The status can be in one of three states:
- `ACTIVE`
- `PENDING`
- `INPROGRESS`

### Example
{: .no_toc }
```python
from pyzscaler.zia import ZIA

with ZIA(api_key='API_KEY', cloud='CLOUD', username='USERNAME', password='PASSWORD') as zia:
    
    # Print the configuration activation status
    status = zia.config.status()
    print(status)
```