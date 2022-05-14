ZCC
==========
This package covers the ZCC interface.

Retrieving the ZCC Company ID.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ZCC Company ID can be obtained by following these instructions:
    1. Navigate to the Zscaler Mobile Admin Portal in a web browser.
    2. Open the Browser console (typically ``F12``) and click on **Network**.
    3. From the top navigation, click on **Enrolled Devices**.
    4. Look for the API call ``mobileadmin.zscaler.net/webservice/api/web/usersByCompany`` in the 'Networks' tab
       of the Browser Console. Click on this entry.
    5. Click on either **Preview** or **Response** to see the data that was returned by the Mobile Admin Portal.
    6. The Company ID is represented as an ``int`` and can be found under the ``companyId`` key in the object returned
       for each user.

.. toctree::
    :maxdepth: 1
    :glob:
    :hidden:

    *

.. automodule:: pyzscaler.zcc
    :members:
