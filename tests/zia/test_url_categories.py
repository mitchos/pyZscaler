import pytest
import responses
from box import Box, BoxList
from responses import matchers


@pytest.fixture(name="url_categories")
def fixture_url_categories():
    return [
        {
            "id": "TEST_A",
            "urls": [],
            "dbCategorizedUrls": [],
            "customCategory": False,
            "editable": True,
            "description": "TEST_A_DESC",
            "type": "URL_CATEGORY",
            "val": 1,
            "customUrlsCount": 0,
            "urlsRetainingParentCategoryCount": 0,
        },
        {
            "id": "TEST_B",
            "urls": [],
            "dbCategorizedUrls": [],
            "customCategory": False,
            "editable": True,
            "description": "TEST_B_DESC",
            "type": "URL_CATEGORY",
            "val": 2,
            "customUrlsCount": 0,
            "urlsRetainingParentCategoryCount": 0,
        },
    ]


@pytest.fixture(name="custom_categories")
def fixture_custom_url_categories():
    return [
        {
            "configuredName": "Test URL",
            "customCategory": True,
            "customUrlsCount": 2,
            "dbCategorizedUrls": ["news.com", "cnn.com"],
            "description": "Test",
            "editable": True,
            "id": "CUSTOM_02",
            "keywords": [],
            "keywordsRetainingParentCategory": [],
            "superCategory": "TEST",
            "type": "URL_CATEGORY",
            "urls": ["test.example.com", "example.com"],
            "urlsRetainingParentCategoryCount": 0,
            "val": 129,
        },
        {
            "configuredName": "Test TLD",
            "customCategory": True,
            "customUrlsCount": 2,
            "dbCategorizedUrls": [],
            "description": "Test",
            "editable": True,
            "id": "CUSTOM_03",
            "keywords": [],
            "keywordsRetainingParentCategory": [],
            "superCategory": "USER_DEFINED",
            "type": "TLD_CATEGORY",
            "urls": [".ru", ".tk"],
            "urlsRetainingParentCategoryCount": 0,
            "val": 130,
        },
    ]


@pytest.fixture(name="url_lookups")
def fixture_url_lookups():
    # Generate a list of URLs for the given quantity
    def _method(num):
        return [f"www.{x}.com" for x in range(num)]

    return _method


@responses.activate
def test_url_category_lookup(zia):
    lookup_response = [
        {
            "url": "github.com",
            "url_classifications": ["PROFESSIONAL_SERVICES", "OTHER_INFORMATION_TECHNOLOGY"],
            "url_classifications_with_security_alert": [],
        }
    ]
    responses.add(
        method="POST",
        url="https://zsapi.zscaler.net/api/v1/urlLookup",
        json=lookup_response,
        status=200,
    )
    resp = zia.url_categories.lookup(["github.com"])
    assert isinstance(resp, BoxList)
    assert len(resp) == 1
    assert resp[0].url == "github.com"


@responses.activate
def test_url_category_lookup_chunked(zia, url_lookups):
    urls = url_lookups(250)

    responses.add(
        method="POST",
        url="https://zsapi.zscaler.net/api/v1/urlLookup",
        json=urls[:101],
        status=200,
    )

    responses.add(
        method="POST",
        url="https://zsapi.zscaler.net/api/v1/urlLookup",
        json=urls[101:201],
        status=200,
    )
    responses.add(
        method="POST",
        url="https://zsapi.zscaler.net/api/v1/urlLookup",
        json=urls[201:],
        status=200,
    )

    resp = zia.url_categories.lookup(urls)
    assert isinstance(resp, BoxList)
    assert len(resp) == 250


@responses.activate
def test_list_categories(zia, url_categories):
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/urlCategories?customOnly=False&includeOnlyUrlKeywordCounts=False",
        json=url_categories,
        status=200,
    )
    resp = zia.url_categories.list_categories()
    assert isinstance(resp, BoxList)
    assert len(resp) == 2
    assert resp[0].id == "TEST_A"


@responses.activate
def test_get_quota(zia):
    quota_response = {
        "uniqueUrlsProvisioned": 1,
        "remainingUrlsQuota": 24999,
    }
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/urlCategories/urlQuota",
        json=quota_response,
        status=200,
    )
    resp = zia.url_categories.get_quota()
    assert isinstance(resp, Box)
    assert resp.unique_urls_provisioned == 1


@responses.activate
def test_get_category(zia, url_categories):
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/urlCategories/TEST_A",
        json=url_categories[0],
        status=200,
    )
    resp = zia.url_categories.get_category("TEST_A")
    assert isinstance(resp, Box)
    assert resp.id == "TEST_A"


@responses.activate
def test_add_url_category(zia, custom_categories):
    responses.add(
        method="POST",
        url="https://zsapi.zscaler.net/api/v1/urlCategories",
        json=custom_categories[0],
        status=200,
    )
    resp = zia.url_categories.add_url_category(
        name="Test", super_category="TEST", urls=["example.com", "test.example.com"], description="Test"
    )
    assert isinstance(resp, Box)
    assert resp.configured_name == "Test URL"


@responses.activate
def test_add_tld_category(zia, custom_categories):
    responses.add(
        method="POST",
        url="https://zsapi.zscaler.net/api/v1/urlCategories",
        json=custom_categories[1],
        status=200,
    )
    resp = zia.url_categories.add_tld_category(name="Test", tlds=[".ru", ".tk"], description="Test")
    assert isinstance(resp, Box)
    assert resp.configured_name == "Test TLD"


@responses.activate
def test_update_url_category(zia, custom_categories):
    updated_category = custom_categories[0]
    updated_category["description"] = "Updated Test"
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/urlCategories/CUSTOM_02",
        json=custom_categories[0],
        status=200,
    )
    responses.add(
        method="PUT",
        url="https://zsapi.zscaler.net/api/v1/urlCategories/CUSTOM_02",
        json=updated_category,
        status=200,
        match=[matchers.json_params_matcher(updated_category)],
    )
    resp = zia.url_categories.update_url_category("CUSTOM_02", description="Updated Test")

    assert isinstance(resp, Box)
    assert resp.description == updated_category["description"]


@responses.activate
def test_add_urls_to_category(zia, custom_categories):
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/urlCategories/CUSTOM_02",
        json=custom_categories[0],
        status=200,
    )
    received_response = custom_categories[0]
    received_response["urls"] = ["update.example.com"]
    responses.add(
        method="PUT",
        url="https://zsapi.zscaler.net/api/v1/urlCategories/CUSTOM_02?action=ADD_TO_LIST",
        json={
            "configuredName": "Test URL",
            "customCategory": True,
            "customUrlsCount": 2,
            "dbCategorizedUrls": [],
            "description": "Test",
            "editable": True,
            "id": "CUSTOM_02",
            "keywords": [],
            "keywordsRetainingParentCategory": [],
            "superCategory": "TEST",
            "type": "URL_CATEGORY",
            "urls": ["test.example.com", "example.com", "update.example.com"],
            "urlsRetainingParentCategoryCount": 0,
            "val": 129,
        },
        status=200,
        match=[matchers.json_params_matcher(received_response)],
    )
    resp = zia.url_categories.add_urls_to_category("CUSTOM_02", urls=["update.example.com"])
    assert isinstance(resp, Box)
    assert resp.urls == ["test.example.com", "example.com", "update.example.com"]


@responses.activate
def test_delete_urls_from_category(zia, custom_categories):
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/urlCategories/CUSTOM_02",
        json=custom_categories[0],
        status=200,
    )
    received_response = {"configuredName": custom_categories[0]["configuredName"], "urls": ["example.com"]}
    responses.add(
        method="PUT",
        url="https://zsapi.zscaler.net/api/v1/urlCategories/CUSTOM_02?action=REMOVE_FROM_LIST",
        json={
            "configuredName": "Test URL",
            "customCategory": True,
            "customUrlsCount": 2,
            "dbCategorizedUrls": [],
            "description": "Test",
            "editable": True,
            "id": "CUSTOM_02",
            "keywords": [],
            "keywordsRetainingParentCategory": [],
            "superCategory": "TEST",
            "type": "URL_CATEGORY",
            "urls": ["test.example.com"],
            "urlsRetainingParentCategoryCount": 0,
            "val": 129,
        },
        status=200,
        match=[matchers.json_params_matcher(received_response)],
    )
    resp = zia.url_categories.delete_urls_from_category("CUSTOM_02", urls=["example.com"])
    assert isinstance(resp, Box)
    assert resp.urls[0] == "test.example.com"


@responses.activate
def test_delete_from_category(zia, custom_categories):
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/urlCategories/CUSTOM_02",
        json=custom_categories[0],
        status=200,
    )
    received_response = {
        "configuredName": custom_categories[0]["configuredName"],
        "urls": ["example.com"],
        "dbCategorizedUrls": ["news.com"],
    }
    responses.add(
        method="PUT",
        url="https://zsapi.zscaler.net/api/v1/urlCategories/CUSTOM_02?action=REMOVE_FROM_LIST",
        json={
            "configuredName": "Test URL",
            "customCategory": True,
            "customUrlsCount": 2,
            "dbCategorizedUrls": ["cnn.com"],
            "description": "Test",
            "editable": True,
            "id": "CUSTOM_02",
            "keywords": [],
            "keywordsRetainingParentCategory": [],
            "superCategory": "TEST",
            "type": "URL_CATEGORY",
            "urls": ["test.example.com"],
            "urlsRetainingParentCategoryCount": 0,
            "val": 129,
        },
        status=200,
        match=[matchers.json_params_matcher(received_response)],
    )
    resp = zia.url_categories.delete_from_category("CUSTOM_02", urls=["example.com"], db_categorized_urls=["news.com"])
    assert isinstance(resp, Box)
    assert resp.urls[0] == "test.example.com"
    assert resp.db_categorized_urls[0] == "cnn.com"


@responses.activate
def test_delete_url_category(zia):
    responses.add(
        method="DELETE",
        url="https://zsapi.zscaler.net/api/v1/urlCategories/CUSTOM_02",
        status=204,
    )
    resp = zia.url_categories.delete_category("CUSTOM_02")
    assert isinstance(resp, int)
    assert resp == 204
