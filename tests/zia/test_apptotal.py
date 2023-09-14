import responses
from box import Box


@responses.activate
def test_get_app(zia):
    app_info = {"id": "12345", "name": "AppName", "verbose": False}
    responses.add(
        method="GET", url="https://zsapi.zscaler.net/api/v1/apps/app?app_id=12345&verbose=False", json=app_info, status=200
    )
    resp = zia.apptotal.get_app(app_id="12345", verbose=False)
    assert isinstance(resp, Box)
    assert resp.id == "12345"
    assert resp.name == "AppName"


@responses.activate
def test_scan_app(zia):
    scan_status = {
        "id": "12345",
        "status": "Scanned",
    }
    responses.add(method="POST", url="https://zsapi.zscaler.net/api/v1/apps/app", json=scan_status, status=200)
    resp = zia.apptotal.scan_app(app_id="12345")
    assert isinstance(resp, Box)
    assert resp.id == "12345"
    assert resp.status == "Scanned"
