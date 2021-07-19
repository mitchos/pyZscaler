---

# Feel free to add content and custom Front Matter to this file.

# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: home nav_order: 1
---

# Home

pyZscaler aims to provide a uniform and easy-to-use interface for each of the Zscaler product APIs. {: .fs-6 } {:
.fw-300 }

[Get Started Now](http://example.com/){: .btn .btn-purple } [View pyZscaler on GitHub](http://example.com/){: .btn }


---

Attention: This SDK is not affiliated with, nor supported by Zscaler in any way.

# Overview

With each Zscaler product having its own developer documentation and authentication methods, this SDK should simplify
your ability to develop software that uses the Zscaler API.

This SDK leverages the very awesome [RESTfly framework](https://restfly.readthedocs.io/en/latest/index.html) developed
by Steve McGrath, which simplifies the development of building libraries to interact with RESTful APIs. A big thank you
to Steve.

## Features

- Simplified authentication with Zscaler APIs.
- Uniform interaction with all Zscaler APIs.
- Uses [python-box](https://github.com/cdgriffith/Box/wiki) to add dot notation access to json data structures.
- Zscaler API output automatically converted from CamelCase to Snake Case.

## Products

- Zscaler Private Access (ZPA)
- Zscaler Internet Access (ZIA)
- Cloud Security Posture Management (CSPM) - (work in progress)

# Installation

The most recent version can be installed from pypi as per below.

    $ pip install pyzscaler

# License

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
