[![pyZscaler](https://raw.githubusercontent.com/mitchos/pyZscaler/gh-pages/docs/assets/images/logo.svg)](https://github.com/mitchos/pyZscaler)
# pyZscaler - An unofficial SDK for the Zscaler API

[![Build Status](https://github.com/mitchos/pyZscaler/actions/workflows/build.yml/badge.svg)](https://github.com/mitchos/pyZscaler/actions/workflows/build.yml)
[![Documentation Status](https://readthedocs.org/projects/pyzscaler/badge/?version=latest)](https://pyzscaler.readthedocs.io/?badge=latest)
[![License](https://img.shields.io/github/license/mitchos/pyZscaler.svg)](https://github.com/mitchos/pyZscaler)
[![Code Quality](https://app.codacy.com/project/badge/Grade/d339fa5d957140f496fdb5c40abc4666)](https://www.codacy.com/gh/mitchos/pyZscaler/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=mitchos/pyZscaler&amp;utm_campaign=Badge_Grade)
[![PyPI Version](https://img.shields.io/pypi/v/pyzscaler.svg)](https://pypi.org/project/pyZscaler)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/pyzscaler.svg)](https://pypi.python.org/pypi/pyzscaler/)
[![GitHub Release](https://img.shields.io/github/release/mitchos/pyZscaler.svg)](https://github.com/mitchos/pyZscaler/releases/)

pyZscaler is an SDK that provides a uniform and easy-to-use interface for each of the Zscaler product APIs.

This SDK is not affiliated with, nor supported by Zscaler in any way.

## Quick links
* [pyZscaler API Documentation](https://pyzscaler.readthedocs.io)
* [pyZscaler User Documentation and Examples (WIP)](https://pyzscaler.packet.tech)

## Overview
Each Zscaler product has separate developer documentation and authentication methods. This SDK simplifies
software development using the Zscaler API.

This SDK leverages the [RESTfly framework](https://restfly.readthedocs.io/en/latest/index.html) developed
by Steve McGrath.

## Features
- Simplified authentication with Zscaler APIs.
- Uniform interaction with all Zscaler APIs.
- Uses [python-box](https://github.com/cdgriffith/Box/wiki) to add dot notation access to json data structures.
- Zscaler API output automatically converted from CamelCase to Snake Case.
- Various quality of life enhancements for object CRUD methods.

## Products
- Zscaler Private Access (ZPA)
- Zscaler Internet Access (ZIA)
- Zscaler Digital Experience (ZDX)
- Zscaler Mobile Admin Portal for Zscaler Client Connector (ZCC)
- Zscaler Connector Portal (ZCON)


## Installation

The most recent version can be installed from pypi as per below.

    $ pip install pyzscaler

## Usage

Before you can interact with any of the Zscaler APIs, you may need to generate API keys or retrieve tenancy information
for each product that you are interfacing with. Once you have the requirements and you have installed pyZscaler,
you're ready to go.


### Quick ZIA Example - Explicitly Activate Changes
**Note:** Changes will not be activated until you explicitly call the `activate()` method or the admin session is closed.
It's a best-practice to log out your API session so that logging is sane and you don't have unnecessary sessions open.
```python
from pyzscaler import ZIA

zia = ZIA(api_key='API_KEY', cloud='CLOUD', username='USERNAME', password='PASSWORD')
for user in zia.users.list_users():
    print(user)
    
zia.config.activate() # Explicitly activate changes (if applicable). 
zia.session.delete()  # Log out of the ZIA API and automatically commit any other changes
```

### Quick ZIA Example - Using the Python Context Manager

**Note**: Using the Python Context Manager will automatically log the admin user out and commit/activate any changes 
made when execution is complete.

```python
from pyzscaler import ZIA
with ZIA(api_key='API_KEY', cloud='CLOUD', username='USERNAME', password='PASSWORD') as zia:
    for user in zia.users.list_users():
        print(user)

```


### Quick ZPA Example

```python
from pyzscaler import ZPA
from pprint import pprint

zpa = ZPA(client_id='CLIENT_ID', client_secret='CLIENT_SECRET', customer_id='CUSTOMER_ID')
for app_segment in zpa.app_segments.list_segments():
    pprint(app_segment)
```

### Quick ZCC Example

```python
from pyzscaler import ZCC
from pprint import pprint

zcc = ZCC(client_id='CLIENT_ID', client_secret='CLIENT_SECRET', company_id='COMPANY_ID')
for device in zcc.devices.list_devices():
    pprint(device)
```
### Quick ZDX Example

```python
from pyzscaler import ZDX

zdx = ZDX(client_id='CLIENT_ID', client_secret='CLIENT_SECRET', cloud='CLOUD')
for device in zdx.devices.list_devices():
    print(device)
```
### Quick ZCON Example
The Zscaler Connector Portal uses the same authentication methods as ZIA and this will allow us to use the Python Context
Manager just like we did with ZIA. Of course, you can still use the explicit method if you prefer.

```python
from pyzscaler import ZCON

with ZCON(api_key='API_KEY', cloud='CLOUD', username='USERNAME', password='PASSWORD') as zcon:
    for group in zcon.groups.list_groups():
        print(group)
```



## Documentation
### API Documentation
pyZscaler's API is fully 100% documented and is hosted at [ReadTheDocs](https://pyzscaler.readthedocs.io). 

This documentation should be used when working with pyZscaler rather than referring to Zscaler's API reference. 
pyZscaler makes some quality of life improvements to simplify and clarify arguments passed to Zscaler's API.

### User Documentation
A start has been made on [user documentation](https://pyzscaler.packet.tech) with examples and explanations on how to implement with pyZcaler.

## Is It Tested?
Yes! pyZscaler has a complete test suite that fully covers all methods within all modules.

## Contributing

Contributions to pyZscaler are absolutely welcome.

Please see the [Contribution Guidelines](https://github.com/mitchos/pyZscaler/blob/main/CONTRIBUTING.md) for more information.

[Poetry](https://python-poetry.org/docs/) is currently being used for builds and management. You'll want to have
poetry installed and available in your environment.

## Issues
Please feel free to open an issue using [Github Issues](https://github.com/mitchos/pyZscaler/issues) if you run into any problems using pyZscaler.

## License
MIT License

Copyright (c) 2021 Mitch Kelly

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.