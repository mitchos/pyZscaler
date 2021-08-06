---

layout: home 
nav_order: 1
---

# Home

<img alt="pyZscaler Logo" src="https://mitchos.github.io/pyZscaler/assets/images/logo.svg" width="600" height="180">

pyZscaler provides a uniform and simple python interface for each of the Zscaler product APIs. 
{: .fs-6 } 
{: .fw-300 }

[Get Started Now](#getting-started){: .btn .btn-purple }
[View pyZscaler on GitHub](http://github.com/mitchos/pyZscaler/){: .btn }{:target="_blank"}


---

**Attention:** This SDK is not affiliated with, nor supported by Zscaler in any way.

## Quick Links
- [pyZscaler Library Documentation on ReadTheDocs](https://pyzscaler.readthedocs.io)

## Overview

With each Zscaler product having its own developer documentation and authentication methods, this SDK simplifies your
ability to develop software that uses the Zscaler API.

This SDK uses the [RESTfly framework](https://restfly.readthedocs.io/en/latest/index.html) developed by Steve McGrath.

The Zscaler APIs expect and return JSON structures with key names in CamelCase. This violates PEP-8 and results in code
that's hard to read. pyZscaler will seamlessly convert to PEP-8 compliant Snake Case so that your code can remain
readable and beautiful. Refer to the pyZscaler API documentation at ReadTheDocs to ensure that you are passing correctly
named parameters to the class methods.

## About This Site

This site aims to provide a reference for developing code that uses this SDK. Code examples are provided to be verbose
and explanatory; there may be better and more concise ways to implement the example in production. e.g. positional args
in class method calls are shown using the arg name for clarity.

RFC5735 TEST-NET addresses are used in examples. Be aware that if you use these in your testing then the geo-location
features will not work as these IP addresses don't resolve to a registered location.

### Features

- Simplified authentication with Zscaler APIs.
- Uniform interaction with all Zscaler APIs.
- Uses [python-box](https://github.com/cdgriffith/Box/wiki) to add dot notation access to json data structures.
- Zscaler API output automatically converted from CamelCase to Snake Case.

### Products

- Zscaler Private Access (ZPA)
- Zscaler Internet Access (ZIA)

## Installation

The most recent version can be installed from pypi as per below.

    $ pip install pyzscaler

## Getting Started

After you've installed pyZscaler, check out the guide for each library below:

- [ZIA](zia-api/index) (work in progress)
- [ZPA](zpa-api/index) (work in progress)

While these guides are still a work in progress, visit the
[pyZscaler API documentation](https://pyzscaler.readthedocs.io/en/latest/index.html) for limited examples and full
documentation of each library.

## License

MIT License

Copyright (c) 2021 Mitch Kelly

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
