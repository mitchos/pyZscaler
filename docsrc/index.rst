.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Contents

   zs/zpa/index

pyZscaler is an unofficial SDK for interacting with Zscaler APIs
=====================================================================
pyZscaler aims to provide a uniform and easy-to-use interface for each of the Zscaler product APIs.


.. attention:: This SDK is not affiliated with, nor supported by Zscaler in any way.

   :strong:`Caveats`

   - Not all features may be implemented.
   - Implemented features may be buggy or incorrect.
   - Bugs will be fixed in my own time.

Overview
==========
With each Zscaler product having its own developer documentation and authentication methods, this SDK should simplify
your ability to develop software that uses the Zscaler API.

This SDK leverages the very awesome `RESTfly framework <https://restfly.readthedocs.io/en/latest/index.html>`_ developed by Steve McGrath, which simplifies the development of
building libraries to interact with RESTful APIs. A big thank you to Steve.

Features
----------
- Simplified authentication with Zscaler APIs.
- Uniform interaction with all Zscaler APIs.
- Uses `python-box <https://github.com/cdgriffith/Box/wiki>`_ to add dot notation access to json data structures.
- Zscaler API output automatically converted from CamelCase to Snake Case.

Products
---------
- :doc:`Zscaler Private Access (ZPA) <zs/zpa/index>`
- Zscaler Internet Access (ZIA) - (work in progress)
- Cloud Security Posture Management (CSPM) - (work in progress)

Installation
==============

The most recent version can be installed from pypi as per below.

.. code-block:: console

    $ pip install pyzscaler

Usage
========
Before you can interact with any of the Zscaler APIs, you will need to generate API keys for each product that you are
writing code for. Once you have generated the API keys and installed pyZscaler, you're ready to go.

Getting started with ZPA
--------------------------
For ZPA, you will need the ``CLIENT_ID``, ``CLIENT_SECRET`` and ``CUSTOMER_ID``.

- `How to generate the CLIENT_ID, CLIENT_SECRET and find the CUSTOMER_ID <https://help.zscaler.com/zpa/about-api-keys>`_

.. code-block:: python

    from pyzscaler import ZPA
    zpa = ZPA('CLIENT_ID', 'CLIENT_SECRET', 'CUSTOMER_ID')
    for app_segment in zpa.app_segments.list():
        pprint(app_segment)

.. automodule:: zscaler
   :members:

License
=========
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