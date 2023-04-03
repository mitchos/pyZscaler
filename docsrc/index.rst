.. meta::
   :description lang=en:
        pyZscaler is an SDK that provides a simple and uniform interface for each of the Zscaler product APIs.
.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Contents

   zs/zia/index
   zs/zpa/index
   zs/zcc/index
   zs/zdx/index

pyZscaler SDK - Library Reference
=====================================================================
pyZscaler is an SDK that provides a uniform and easy-to-use interface for each of the Zscaler product APIs.

Quick Links
--------------
- `pyZscaler User Documentation and Examples <https://mitchos.github.io/pyZscaler>`_
- `pyZscaler SDK on GitHub <https://github.com/mitchos/pyZscaler>`_

.. attention:: This SDK is not affiliated with, nor supported by Zscaler in any way.


Overview
==========
This site is the library reference for the pyZscaler SDK and describes every class and method in detail. If you are
looking for user documentation with explanations and examples then you might be looking for the
`pyZscaler User Documentation <https://mitchos.github.io/pyZscaler>`_

Features
----------
- Simplified authentication with Zscaler APIs.
- Uniform interaction with all Zscaler APIs.
- Uses `python-box <https://github.com/cdgriffith/Box/wiki>`_ to add dot notation access to json data structures.
- Zscaler API output automatically converted from CamelCase to Snake Case.
- Various quality of life enhancements for object update methods.

Products
---------
- :doc:`Zscaler Private Access (ZPA) <zs/zpa/index>`
- :doc:`Zscaler Internet Access (ZIA) <zs/zia/index>`
- :doc:`Zscaler Mobile Admin Portal <zs/zcc/index>`
- :doc:`Zscaler Digital Experience (ZDX) <zs/zdx/index>`

Installation
==============

The most recent version can be installed from pypi as per below.

.. code-block:: console

    $ pip install pyzscaler

Usage
========
Before you can interact with any of the Zscaler APIs, you may need to generate API keys or retrieve tenancy information
for each product that you are interfacing with. Once you have the requirements and you have installed pyZscaler,
you're ready to go.

Getting started
--------------------------

Quick ZIA Example
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from pyzscaler import ZIA
    from pprint import pprint

    zia = ZIA(api_key='API_KEY', cloud='CLOUD', username='USERNAME', password='PASSWORD')
    for user in zia.users.list_users():
        pprint(user)

Quick ZPA Example
^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from pyzscaler import ZPA
    from pprint import pprint

    zpa = ZPA(client_id='CLIENT_ID', client_secret='CLIENT_SECRET', customer_id='CUSTOMER_ID')
    for app_segment in zpa.app_segments.list_segments():
        pprint(app_segment)


Quick ZCC Example
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from pyzscaler import ZCC
    from pprint import pprint

    zcc = ZCC(client_id='CLIENT_ID', client_secret='CLIENT_SECRET', company_id='COMPANY_ID)
    for device in zcc.devices.list_devices():
        pprint(device)

Quick ZDX Example
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from pyzscaler import ZDX
    from pprint import pprint

    zcc = ZDX(client_id='CLIENT_ID', client_secret='CLIENT_SECRET')
    for device in zdx.devices.list_devices():
        pprint(device)


.. automodule:: pyzscaler
   :members:

Contributing
==============
Contributions to pyZscaler are absolutely welcome. At the moment, we could use more tests and documentation/examples.
Please see the `Contribution Guidelines <https://github.com/mitchos/pyZscaler/blob/main/CONTRIBUTING.md>`_ for more information.

`Poetry <https://python-poetry.org/docs/>`_ is currently being used for builds and management. You'll want to have
poetry installed and available in your environment.

Issues
=========
Please feel free to open an issue using `Github Issues <https://github.com/mitchos/pyZscaler/issues>`_ if you run into any problems using pyZscaler.

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