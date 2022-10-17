import pytest
import responses
from responses import matchers


@pytest.fixture(name="blacklist_urls")
def fixture_urls():
    return {"blacklistUrls": ["test.com", "example.com"]}


@pytest.fixture(name="whitelist_urls")
def fixture_whitelist_urls():
    return {"whitelistUrls": ["demo.com", "site.com"]}


@responses.activate
def test_get_blacklist(zia, blacklist_urls):
    responses.add(responses.GET, url="https://zsapi.zscaler.net/api/v1/security/advanced", json=blacklist_urls, status=200)
    resp = zia.security.get_blacklist()

    assert isinstance(resp, list)
    assert resp[0] == "test.com"


@responses.activate
def test_get_whitelist(zia, whitelist_urls):
    responses.add(responses.GET, url="https://zsapi.zscaler.net/api/v1/security", json=whitelist_urls, status=200)
    resp = zia.security.get_whitelist()

    assert isinstance(resp, list)
    assert resp[0] == "demo.com"


@responses.activate
def test_get_whitelist_empty(zia, whitelist_urls):
    responses.add(responses.GET, url="https://zsapi.zscaler.net/api/v1/security", json={}, status=200)
    resp = zia.security.get_whitelist()

    assert isinstance(resp, list)
    assert resp == []


@responses.activate
def test_erase_whitelist(zia):
    responses.add(
        responses.PUT,
        url="https://zsapi.zscaler.net/api/v1/security",
        status=200,
        match=[matchers.json_params_matcher({"whitelistUrls": []})],
    )

    resp = zia.security.erase_whitelist()
    assert resp == 200


@responses.activate
def test_replace_whitelist(zia, whitelist_urls):
    responses.add(
        responses.PUT,
        url="https://zsapi.zscaler.net/api/v1/security",
        json=whitelist_urls,
        status=200,
        match=[matchers.json_params_matcher(whitelist_urls)],
    )
    resp = zia.security.replace_whitelist(["demo.com", "site.com"])

    assert isinstance(resp, list)
    assert resp[0] == "demo.com"


@responses.activate
def test_add_urls_to_whitelist(zia, whitelist_urls):
    responses.add(responses.GET, url="https://zsapi.zscaler.net/api/v1/security", json=whitelist_urls, status=200)

    whitelist_urls["whitelistUrls"].append("mysite.com")

    responses.add(
        responses.PUT,
        url="https://zsapi.zscaler.net/api/v1/security",
        json=whitelist_urls,
        status=200,
        match=[matchers.json_params_matcher(whitelist_urls)],
    )
    resp = zia.security.add_urls_to_whitelist(["mysite.com"])

    assert isinstance(resp, list)
    assert resp[2] == "mysite.com"


@responses.activate
def test_delete_urls_from_whitelist(zia, whitelist_urls):
    responses.add(responses.GET, url="https://zsapi.zscaler.net/api/v1/security", json=whitelist_urls, status=200)

    whitelist_urls["whitelistUrls"].pop(0)

    responses.add(
        responses.PUT,
        url="https://zsapi.zscaler.net/api/v1/security",
        json=whitelist_urls,
        status=200,
        match=[matchers.json_params_matcher(whitelist_urls)],
    )

    resp = zia.security.delete_urls_from_whitelist(["demo.com"])

    assert isinstance(resp, list)
    assert len(resp) == 1


@responses.activate
def test_add_urls_to_blacklist(zia, blacklist_urls):

    blacklist_urls["blacklistUrls"].append("mysite.com")

    responses.add(
        responses.POST,
        url="https://zsapi.zscaler.net/api/v1/security/advanced/blacklistUrls?action=ADD_TO_LIST",
        status=204,
        match=[matchers.json_params_matcher({"blacklistUrls": ["mysite.com"]})],
    )
    responses.add(responses.GET, url="https://zsapi.zscaler.net/api/v1/security/advanced", json=blacklist_urls, status=200)
    resp = zia.security.add_urls_to_blacklist(["mysite.com"])

    assert isinstance(resp, list)
    assert resp == ["test.com", "example.com", "mysite.com"]


@responses.activate
def test_delete_urls_from_blacklist(zia, blacklist_urls):
    blacklist_urls["blacklistUrls"].pop(0)

    responses.add(
        responses.POST,
        url="https://zsapi.zscaler.net/api/v1/security/advanced/blacklistUrls?action=REMOVE_FROM_LIST",
        status=204,
        match=[matchers.json_params_matcher({"blacklistUrls": ["test.com"]})],
    )
    resp = zia.security.delete_urls_from_blacklist(["test.com"])

    assert isinstance(resp, int)
    assert resp == 204


@responses.activate
def test_erase_blacklist(zia):
    responses.add(
        responses.PUT,
        url="https://zsapi.zscaler.net/api/v1/security/advanced",
        status=200,
        match=[matchers.json_params_matcher({"blacklistUrls": []})],
    )

    resp = zia.security.erase_blacklist()
    assert resp == 200


@responses.activate
def test_replace_blacklist(zia):
    new_urls = {"blacklistUrls": ["abc.com", "def.com"]}

    responses.add(
        responses.PUT,
        url="https://zsapi.zscaler.net/api/v1/security/advanced",
        json=new_urls,
        status=204,
        match=[matchers.json_params_matcher(new_urls)],
    )
    resp = zia.security.replace_blacklist(["abc.com", "def.com"])

    assert isinstance(resp, list)
    assert resp[0] == "abc.com"
