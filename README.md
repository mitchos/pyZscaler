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
- Cloud Security Posture Management (CSPM) - (work in progress)


## Installation

The most recent version can be installed from pypi as per below.

    $ pip install pyzscaler

## Usage

Before you can interact with any of the Zscaler APIs, you may need to generate API keys or retrieve tenancy information
for each product that you are interfacing with. Once you have the requirements and you have installed pyZscaler,
you're ready to go.


### Quick ZIA Example

```python
from pyzscaler.zia import ZIA
from pprint import pprint

zia = ZIA(api_key='API_KEY', cloud='CLOUD', username='USERNAME', password='PASSWORD')
for user in zia.users.list_users():
    pprint(user)
```

### Quick ZPA Example

```python
from pyzscaler.zpa import ZPA
from pprint import pprint

zpa = ZPA(client_id='CLIENT_ID', client_secret='CLIENT_SECRET', customer_id='CUSTOMER_ID')
for app_segment in zpa.app_segments.list():
    pprint(app_segment)
```

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