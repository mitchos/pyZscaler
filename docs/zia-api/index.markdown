---
layout: default 
title: ZIA 
permalink: /zia-api/ 
nav_order: 2 
has_children: true

---

# Getting Started with ZIA

For ZIA, you will need to provide params when initialising the class or set the environment variables.

## Initialising the ZIA instance and returning a list of users

All examples in this documentation will assume that you are initialising the ZIA Class the same way as shown below.
Ensure that you make adjustments in your code if you are using a different naming convention.

We'll use the Python ``with`` context handler so that the ``ZIA._deauthenticate`` method is called to delete the session
when we're done. If you don't do this then your audit logs will show the API user logging in but not logging out. No
issues or limits around this have been found during testing of pyZscaler but it's general best-practice not to leave
authentication sessions dangling.

```python
from pyzscaler.zia import ZIA
from pprint import pprint

with ZIA(api_key='API_KEY', cloud='CLOUD', username='USERNAME', password='PASSWORD') as zia:
    for user in zia.users.list():
        pprint(user)
```

## ZIA Parameters

The table below shows the parameters that the ZIA Class requires.

| Param        | ENV        | Description |
|:-------------|:------------------|:------|
| cloud           | `ZIA_CLOUD` | The cloud that your ZIA tenant is provisioned on.  |
| api_key | `ZIA_API_KEY`   | The API key generated from your ZIA console.  |
| username           | `ZIA_USERNAME`      | The username of your administrator user that will be used for API calls.   |
| password           | `ZIA_PASSWORD` | The password for the administrator user.  |

### How to generate the API Key

Follow the [ZIA documentation](https://help.zscaler.com/zia/api-getting-started#RetrieveAPIKey) to generate an API Key.

### How to determine the ZIA Cloud

You can find the name of the cloud in the URL that admins use to log into the Zscaler service. E.g. if an organisation
logs into admin.zscaler.net, then that organisation's cloud name is zscaler.net. You don't need to supply the .net
suffix with pyZscaler, so the `CLOUD` arg would simply be `zscaler`.

For convenience, the table below contains the mapping of each Zscaler cloud to pyZscaler `CLOUD` param.

| URL | CLOUD param |
|:----|:------|
| admin.zscaler.net | zscaler |
| admin.zscalerone.net | zscalerone |
| admin.zscalertwo.net | zscalertwo |
| admin.zscalerthree.net | zscalerthree |
| admin.zscloud.net | zscloud |
| admin.zscalerbeta.net | zscalerbeta |
| admin.zscalergov.net | zscalergov |



