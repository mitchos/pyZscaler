import responses
from box import Box


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
