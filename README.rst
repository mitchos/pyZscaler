pyZscaler - An unofficial SDK for the Zscaler API
=====================================================================
pyZscaler is an SDK that provides a uniform and easy-to-use interface for each of the Zscaler product APIs.


.. attention:: This SDK is not affiliated with, nor supported by Zscaler in any way.

   :strong:`Caveats`

   - Not all features may be implemented.
   - Implemented features may be buggy or incorrect.
   - Bugs will be fixed in my own time.

Overview
==========
With each Zscaler product having its own developer documentation and authentication methods, this SDK should simplify
your ability to develop software that uses the Zscaler API.

The goal of Pyzscaler is to eventually cover all public API endpoints published by Zscaler across all of their products.

This SDK leverages the very awesome `RESTfly framework <https://restfly.readthedocs.io/en/latest/index.html>`_ developed
by Steve McGrath, which simplifies the development of building libraries to interact with RESTful APIs.

Features
----------
- Simplified authentication with Zscaler APIs.
- Uniform interaction with all Zscaler APIs.
- Uses `python-box <https://github.com/cdgriffith/Box/wiki>`_ to add dot notation access to json data structures.
- Zscaler API output automatically converted from CamelCase to Snake Case.
- Various quality of life enhancements for object update methods.

Products
---------
- Zscaler Private Access (ZPA)
- Zscaler Internet Access (ZIA)
- Cloud Security Posture Management (CSPM) - (work in progress)

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

Getting started with ZIA
--------------------------
For ZIA, you will need to provide params when instantiating the class or set the environment variables as per the
table below:

.. list-table:: ZIA Requirements
   :header-rows: 1

   * - Param
     - ENV
     - Description
   * - cloud
     - ``ZIA_CLOUD``
     - The cloud that your ZIA tenant is provisioned on.
   * - api_key
     - ``ZIA_API_KEY``
     - The API key generated from your ZIA console.
   * - username
     - ``ZIA_USERNAME``
     - The username of your administrator user that will be used for API calls.
   * - password
     - ``ZIA_PASSWORD``
     - The password for the administrator user.

See the `ZIA docs <https://help.zscaler.com/zia/api-getting-started#RetrieveAPIKey>`_ for how to generate the `api_key`.

How to determine the ZIA CLOUD
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can find the name of the cloud in the URL that admins use to log into the Zscaler service. E.g.
if an organisation logs into admin.zscaler.net, then that organization's cloud name is zscaler.net. You don't
need to supply the .net suffix with pyZscaler, so the ``CLOUD`` arg would simply be ``zscaler``.

.. list-table:: ZIA Cloud List
   :header-rows: 1

   * - URL
     - CLOUD
   * - admin.zscaler.net
     - zscaler
   * - admin.zscalerone.net
     - zscalerone
   * - admin.zscalertwo.net
     - zscalertwo
   * - admin.zscalerthree.net
     - zscalerthree
   * - admin.zscloud.net
     - zscloud
   * - admin.zscalerbeta.net
     - zscalerbeta
   * - admin.zscalergov.net
     - zscalergov

Quick ZIA Example
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from pyzscaler.zia import ZIA
    from pprint import pprint

    zia = ZIA(api_key='API_KEY', cloud='CLOUD', username='USERNAME', password='PASSWORD')
    for user in zia.users.list():
        pprint(user)

Getting started with ZPA
--------------------------
For ZPA, you will need to provide params when instantiating the class or set the environment variables as per the
table below:

.. list-table:: ZPA Requirements
   :header-rows: 1

   * - Param
     - ENV
     - Description
   * - client_id
     - ``ZPA_CLIENT_ID``
     - The client ID that is associated with the client secret.
   * - client_secret
     - ``ZPA_CLIENT_SECRET``
     - The client secret that was generated for the client ID.
   * - customer_id
     - ``ZPA_CUSTOMER_ID``
     - The customer ID for the ZPA tenancy.

See the `ZPA docs <https://help.zscaler.com/zpa/about-api-keys>`_ for how to generate the `client_id`, `client_secret` and find the `customer_id`.

Quick ZPA Example
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from pyzscaler.zpa import ZPA
    from pprint import pprint

    zpa = ZPA(client_id='CLIENT_ID', client_secret='CLIENT_SECRET', customer_id='CUSTOMER_ID')
    for app_segment in zpa.app_segments.list():
        pprint(app_segment)

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