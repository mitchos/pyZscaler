import responses
from box import Box


@responses.activate
def test_audit_log_create(zia):
    responses.add(
        method="POST",
        url="https://zsapi.zscaler.net/api/v1/auditlogEntryReport",
        status=204,
    )
    resp = zia.audit_logs.create(start_time="1627221600000", end_time="1627271676622")

    assert isinstance(resp, int)
    assert resp == 204


@responses.activate
def test_audit_log_status(zia):
    audit_log_status = {
        "error_code": None,
        "error_message": None,
        "progress_end_time": 0,
        "progress_items_complete": 0,
        "status": "EXECUTING",
    }
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/auditlogEntryReport",
        json=audit_log_status,
        status=200,
    )
    resp = zia.audit_logs.status()
    assert isinstance(resp, Box)
    assert resp.status == "EXECUTING"


@responses.activate
def test_audit_log_cancel(zia):
    responses.add(
        method="DELETE",
        url="https://zsapi.zscaler.net/api/v1/auditlogEntryReport",
        status=204,
    )
    resp = zia.audit_logs.cancel()
    assert isinstance(resp, int)
    assert resp == 204


@responses.activate
def test_audit_log_get_report(zia):
    audit_report = (
        "Administrator,admin@test.example.com\n"
        'Report Created,"31 Dec 2021 23:59:59, AEDT"\n'
        'Start Time,"31 Dec 2021 23:59:59, AEST"\n'
        'End Time,"31 Dec 2021 23:59:59, AEST"\n'
        "Time,User,Action,AA in Cloud,Result,Client "
        "IP,Interface,Category,Subcategory,Resource,Pre Action,Post Action\n"
        '"31 Dec 2021 23:59:59, AEST",admin@test.example.com,Sign '
        "In,zscaler.net,Successful,203.0.113.1,UI,Login,Login,,,,\n"
    )

    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/auditlogEntryReport/download",
        body=audit_report,
        status=200,
    )
    resp = zia.audit_logs.get_report()
    assert isinstance(resp, str)
    assert resp == audit_report
