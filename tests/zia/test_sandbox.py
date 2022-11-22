import os

import responses
from box import Box
from responses import matchers


@responses.activate
def test_sandbox_get_quota(zia):
    sandbox_response = [
        {
            "allowed": 1000,
            "scale": "DAYS",
            "start_time": -1,
            "unused": 1000,
            "used": 0,
        }
    ]

    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/sandbox/report/quota",
        json=sandbox_response,
        status=200,
    )

    resp = zia.sandbox.get_quota()
    assert isinstance(resp, Box)
    assert resp.allowed == 1000


@responses.activate
def test_sandbox_get_report(zia):
    sandbox_response = {"summary": "test"}

    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/sandbox/report/HASH?details=summary",
        json=sandbox_response,
        status=200,
    )

    resp = zia.sandbox.get_report("HASH")
    assert isinstance(resp, Box)
    assert resp.summary == "test"


@responses.activate
def test_sandbox_submit_file(zia):
    with open("sandboxtest.txt", "w") as f:
        f.write("Sandbox Test")

    params = {"api_token": "SANDBOXTOKEN", "force": 1}

    responses.add(
        method="POST",
        url="https://csbapi.zscaler.net/zscsb/submit?api_token=SANDBOXTOKEN&force=1",
        json={
            "code": 200,
            "message": "/submit response OK",
            "virus_name": "malicious beha",
            "virus_type": "Sandbox Malware",
            "file_type": "exe",
            "md5": "XYZ",
            "sandbox_submission": "Sandbox Malware",
        },
        match=[matchers.query_param_matcher(params)],
        status=200,
    )

    resp = zia.sandbox.submit_file("sandboxtest.txt", True)
    os.remove("sandboxtest.txt")

    assert resp.code == 200
