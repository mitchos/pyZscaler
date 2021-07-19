---
layout: default title: ZIA permalink: /zia/ nav_order: 2 has_children: true

---

# Getting Started with ZIA

For ZIA, you will need to provide params when instantiating the class or set the environment variables.

## Instantiating the ZIA Class and returning a list of users

```python
from pyzscaler import ZIA

zia = ZIA(api_key='API_KEY', cloud='CLOUD', username='USERNAME', password='PASSWORD')
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



