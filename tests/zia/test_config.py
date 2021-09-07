import responses


@responses.activate
def test_config_status(zia):
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/status",
        json={"status": "ACTIVE"},
        status=200,
    )
    resp = zia.config.status()

    assert resp == "ACTIVE"


@responses.activate
def test_config_activation(zia):
    responses.add(
        responses.POST,
        url="https://zsapi.zscaler.net/api/v1/status/activate",
        json={"status": "ACTIVE"},
        status=200,
    )
    resp = zia.config.activate()

    assert resp == "ACTIVE"
