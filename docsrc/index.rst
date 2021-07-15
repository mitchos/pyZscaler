.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Contents

   zs/zia/index
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

`How to generate the API_KEY <https://help.zscaler.com/zia/api-getting-started#RetrieveAPIKey>`_

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


.. code-block:: python

    from pyzscaler import ZIA
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

- `How to generate the CLIENT_ID, CLIENT_SECRET and find the CUSTOMER_ID <https://help.zscaler.com/zpa/about-api-keys>`_


.. code-block:: python

    from pyzscaler import ZPA
    zpa = ZPA(client_id='CLIENT_ID', client_secret='CLIENT_SECRET', customer_id='CUSTOMER_ID')
    for app_segment in zpa.app_segments.list():
        pprint(app_segment)

.. automodule:: pyzscaler
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