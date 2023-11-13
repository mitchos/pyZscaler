import pytest
import responses
from box import BoxList
from responses import matchers


@pytest.fixture
def shadow_it_report():
    return (
        'Administrator,"admin@example.com"\n'
        'Report Created,"Nov 13, 2023 6:26:52 AM AEDT"\n'
        'Start Time,"Nov 11, 2023 11:00:00 AM AEDT"\n'
        'End Time,"Nov 12, 2023 11:00:00 AM AEDT"\n'
        'Vendor,"zscaler.net"\n'
        "No.,Application,Application Category,Application Status,Application Risk Index,Upload Bytes,Download Bytes,"
        "Total Bytes,Users,Locations,Notes,Integrations,Integration Risks,Certifications,Poor Terms of Service,"
        "Data Breaches in Last 3 Years,Source IP Restriction,MFA Support,Admin Audit Logs,File Sharing,"
        "Password Strength,SSL Pinned,Data Encryption in Transit,Evasive,HTTP Security Header Support,"
        "DNS CAA Policy,Weak Cipher Support,Valid SSL Certificate,Published CVE Vulnerability,SSL Cert Key Size,"
        "Vulnerable to Heartbleed,Vulnerable to Poodle,Vulnerable to Logjam,Support for WAF,Remote Access Screen "
        "Sharing,"
        "Vulnerability Disclosure Policy,Sender Policy Framework,DomainKeys Identified Mail,"
        "Domain-Based Message Authentication,Malware Scanning Content\n"
    )


@pytest.fixture(name="cloud_apps")
def fixture_cloud_apps():
    return [{"id": 1, "name": "App1"}, {"id": 2, "name": "App2"}]


@pytest.fixture(name="custom_tags")
def fixture_custom_tags():
    return [{"id": 101, "name": "Tag1"}, {"id": 102, "name": "Tag2"}]


@responses.activate
def test_export_shadow_it_csv(zia, shadow_it_report):
    responses.add(
        method="POST",
        url="https://zsapi.zscaler.net/api/v1/shadowIT/applications/USER/exportCsv",
        body=shadow_it_report,
        status=200,
    )

    report_csv = zia.cloud_apps.export_shadow_it_csv(application="ExampleApp", entity="USER")
    assert report_csv == shadow_it_report


@responses.activate
def test_export_shadow_it_csv_with_id_filters(zia, shadow_it_report):
    # Setup
    application = "test_app"
    entity = "USER"
    duration = "LAST_7_DAYS"
    user_ids = ["123", "456"]
    location_ids = ["789", "101"]
    department_ids = ["112", "113"]

    # Mocking the API response
    responses.add(
        method="POST",
        url=f"https://zsapi.zscaler.net/api/v1/shadowIT/applications/{entity}/exportCsv",
        json=shadow_it_report,
        status=200,
    )

    # Calling the method with additional id filters
    resp = zia.cloud_apps.export_shadow_it_csv(
        application=application,
        entity=entity,
        duration=duration,
        users=user_ids,
        locations=location_ids,
        departments=department_ids,
    )

    # Assertions
    assert isinstance(resp, str)
    assert (
        responses.calls[0].request.body.decode("utf-8")
        == '{"application": "test_app", "duration": "LAST_7_DAYS", "users": [{"id": "123"}, {"id": "456"}], '
        '"locations": [{"id": "789"}, {"id": "101"}], "departments": [{"id": "112"}, {"id": "113"}]}'
    )


@responses.activate
def test_export_shadow_it_report(zia, shadow_it_report):
    responses.add(
        method="POST",
        url="https://zsapi.zscaler.net/api/v1/shadowIT/applications/export",
        body=shadow_it_report,
        status=200,
    )

    report = zia.cloud_apps.export_shadow_it_report()
    assert report == shadow_it_report


@responses.activate
def test_list_apps(zia, cloud_apps):
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/cloudApplications/lite",
        json=cloud_apps,
        status=200,
    )

    resp = zia.cloud_apps.list_apps()

    assert isinstance(resp, BoxList)
    assert len(resp) == 2
    assert resp[0].id == 1
    assert resp[0].name == "App1"


@responses.activate
def test_list_custom_tags(zia, custom_tags):
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/customTags",
        json=custom_tags,
        status=200,
    )

    resp = zia.cloud_apps.list_custom_tags()

    assert isinstance(resp, BoxList)
    assert len(resp) == 2
    assert resp[0].id == 101
    assert resp[0].name == "Tag1"


@responses.activate
def test_bulk_update(zia):
    sanction_state = "sanctioned"
    api_sanction_state = "SANCTIONED"
    application_ids = ["12345"]
    custom_tag_ids = ["67890"]
    payload = {
        "sanctionedState": api_sanction_state,
        "applicationIds": application_ids,
        "customTags": [{"id": tag_id} for tag_id in custom_tag_ids],
    }

    # Mock response
    responses.add(
        method="PUT",
        url="https://zsapi.zscaler.net/api/v1/cloudApplications/bulkUpdate",
        status=204,
        match=[matchers.json_params_matcher(payload)],
    )

    # Call the method
    resp = zia.cloud_apps.bulk_update(sanction_state, application_ids=application_ids, custom_tag_ids=custom_tag_ids)

    # Assertions
    assert isinstance(resp, int)
    assert resp == 204


def test_bulk_update_invalid_sanction_state(zia):
    # Set up an invalid sanction state
    invalid_sanction_state = "not_valid_state"
    application_ids = ["12345"]

    with pytest.raises(ValueError) as excinfo:
        zia.cloud_apps.bulk_update(invalid_sanction_state, application_ids=application_ids)

    assert (
        str(excinfo.value)
        == f"Invalid sanction state: {invalid_sanction_state}. Accepted values are 'sanctioned', 'unsanctioned', or 'any'."
    )
