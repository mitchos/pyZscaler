import copy

import pytest
import responses
from box import Box
from responses import matchers


@pytest.fixture(name="rules")
def fixture_get_all_rules():
    return [
        {
            "access_control": "READ_WRITE",
            "id": 2669,
            "order": 7,
            "protocols": ["ANY_RULE"],
            "rank": 7,
            "description": "Block all Confidential Information and send an email to the auditor email alias.",
            "dlp_engines": [{"id": 1, "name": "Confidential Information"}],
            "cloud_applications": [],
            "min_size": 0,
            "action": "ALLOW",
            "state": "ENABLED",
            "external_auditor_email": "danny.douglas@corp.com",
            "notification_template": {"id": 1152, "name": "End User Allow Notification"},
            "match_only": True,
            "icap_server": {"id": 1247, "name": "IR"},
            "without_content_inspection": False,
            "name": "Confidential",
            "ocr_enabled": False,
            "dlp_download_scan_enabled": False,
            "zcc_notifications_enabled": False,
            "zscaler_incident_reciever": True,
        },
        {
            "access_control": "READ_WRITE",
            "id": 2670,
            "order": 2,
            "protocols": ["ANY_RULE"],
            "rank": 7,
            "description": "Block all other PCI data and send an email to the auditor email alias.",
            "dlp_engines": [{"id": 61, "name": "PCI", "is_name_l10n_tag": True}],
            "file_types": [
                "PDF_DOCUMENT",
                "MS_MSG",
                "MS_POWERPOINT",
                "MS_WORD",
                "MS_MDB",
                "MS_RTF",
                "FORM_DATA_POST",
                "MS_EXCEL",
            ],
            "cloud_applications": [],
            "min_size": 0,
            "action": "BLOCK",
            "state": "ENABLED",
            "external_auditor_email": "danny.douglas@corp.com",
            "notification_template": {"id": 1151, "name": "End User Block Notification"},
            "match_only": False,
            "icap_server": {"id": 1247, "name": "IR"},
            "without_content_inspection": False,
            "name": "PCI",
            "ocr_enabled": False,
            "dlp_download_scan_enabled": False,
            "zcc_notifications_enabled": False,
            "zscaler_incident_reciever": True,
        },
    ]


@pytest.fixture(name="rules_lite")
def fixture_get_rules_lite():
    return [
        {
            "access_control": "READ_WRITE",
            "id": 2669,
            "description": "Block all Confidential Information and send an email to the auditor email alias.",
            "cloud_applications": [],
            "min_size": 0,
            "state": "ENABLED",
            "match_only": False,
            "icap_server": {"id": 1247, "name": "IR"},
            "without_content_inspection": False,
            "ocr_enabled": False,
            "dlp_download_scan_enabled": False,
            "zcc_notifications_enabled": False,
            "zscaler_incident_reciever": True,
        },
        {
            "access_control": "READ_WRITE",
            "id": 2671,
            "description": "Allow PCI information going to Salesforce for Finance users only",
            "departments": [{"id": 72342, "name": "Finance"}],
            "cloud_applications": ["SALESFORCE"],
            "min_size": 0,
            "state": "ENABLED",
            "match_only": False,
            "icap_server": {},
            "without_content_inspection": False,
            "ocr_enabled": False,
            "dlp_download_scan_enabled": False,
            "zcc_notifications_enabled": False,
            "zscaler_incident_reciever": True,
        },
    ]


@responses.activate
def test_web_dlp_get_rule(rules, zia):
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/webDlpRules/2669",
        json=rules[0],
        status=200,
    )
    resp = zia.web_dlp.get_rule("2669")

    assert isinstance(resp, dict)
    assert resp.id == 2669


@responses.activate
def test_web_dlp_get_all_rules(rules, zia):
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/webDlpRules",
        json=[rules],
        status=200,
    )
    resp = zia.web_dlp.get_all_rules()

    assert isinstance(resp, list)


@responses.activate
def test_web_dlp_get_rules_lite(rules_lite, zia):
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/webDlpRules/lite",
        json=[rules_lite],
        status=200,
    )
    resp = zia.web_dlp.get_rules_lite()

    assert isinstance(resp, list)


@responses.activate
def test_web_dlp_add_rule(zia, rules):
    responses.add(
        method="POST",
        url="https://zsapi.zscaler.net/api/v1/webDlpRules",
        json=rules[0],
        status=200,
        match=[
            matchers.json_params_matcher(
                {
                    "order": 7,
                    "rank": 7,
                    "name": "Confidential",
                    "protocols": ["ANY_RULE"],
                    "action": "ALLOW",
                }
            )
        ],
    )

    payload = {
        "order": 7,
        "rank": 7,
        "name": "Confidential",
        "protocols": ["ANY_RULE"],
        "action": "ALLOW",
    }

    resp = zia.web_dlp.add_rule(payload=payload)

    assert isinstance(resp, dict)
    assert resp.id == 2669
    assert resp.rank == 7
    assert resp.order == 7


@responses.activate
def test_web_dlp_update_rule(zia, rules):
    updated_user = copy.deepcopy(rules[0])
    updated_user["name"] = "New Name"
    updated_user["comments"] = "Updated Test"

    responses.add(
        responses.GET,
        "https://zsapi.zscaler.net/api/v1/webDlpRules/2669",
        json=rules[0],
        status=200,
    )

    responses.add(
        responses.PUT,
        url="https://zsapi.zscaler.net/api/v1/webDlpRules/2669",
        json=updated_user,
        match=[matchers.json_params_matcher(updated_user)],
    )

    resp = zia.web_dlp.update_rule("2669", name="New Name", comments="Updated Test")

    assert isinstance(resp, Box)
    assert resp.name == updated_user["name"]
    assert resp.comments == updated_user["comments"]


@responses.activate
def test_web_dlp_delete_rule(zia):
    responses.add(method="DELETE", url="https://zsapi.zscaler.net/api/v1/webDlpRules/2669", status=204)
    resp = zia.users.delete_user("2669")
    assert resp == 204
