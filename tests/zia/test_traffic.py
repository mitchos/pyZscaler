import responses

from tests.conftest import stub_sleep


@responses.activate
@stub_sleep
def test_list_gre_tunnels_with_one_page(zia, paginated_items):
    items = paginated_items(200)

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/greTunnels",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/greTunnels",
        json=items[100:200],
        status=200,
    )

    resp = zia.traffic.list_gre_tunnels(max_pages=1, page_size=100)

    assert isinstance(resp, list)
    assert resp[50].id == 50
    assert len(resp) == 100


@responses.activate
@stub_sleep
def test_list_gre_tunnels_with_two_pages(zia, paginated_items):
    items = paginated_items(200)

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/greTunnels",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/greTunnels",
        json=items[100:200],
        status=200,
    )

    resp = zia.traffic.list_gre_tunnels(max_pages=2, page_size=100)

    assert isinstance(resp, list)
    assert resp[50].id == 50
    assert resp[150].id == 150
    assert len(resp) == 200


@responses.activate
@stub_sleep
def test_list_gre_tunnels_with_max_items_1(zia, paginated_items):
    items = paginated_items(200)

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/greTunnels",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/greTunnels",
        json=items[100:200],
        status=200,
    )

    resp = zia.traffic.list_gre_tunnels(max_items=1)

    assert isinstance(resp, list)
    assert len(resp) == 1


@responses.activate
@stub_sleep
def test_list_gre_tunnels_with_max_items_150(zia, paginated_items):
    items = paginated_items(200)

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/greTunnels",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/greTunnels",
        json=items[100:200],
        status=200,
    )

    resp = zia.traffic.list_gre_tunnels(max_items=150)

    assert isinstance(resp, list)
    assert len(resp) == 150


@responses.activate
@stub_sleep
def test_list_static_ips_with_one_page(zia, paginated_items):
    items = paginated_items(200)

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/staticIP",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/staticIP",
        json=items[100:200],
        status=200,
    )

    resp = zia.traffic.list_static_ips(max_pages=1, page_size=100)

    assert isinstance(resp, list)
    assert resp[50].id == 50
    assert len(resp) == 100


@responses.activate
@stub_sleep
def test_list_static_ips_with_two_pages(zia, paginated_items):
    items = paginated_items(200)

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/staticIP",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/staticIP",
        json=items[100:200],
        status=200,
    )

    resp = zia.traffic.list_static_ips(max_pages=2, page_size=100)

    assert isinstance(resp, list)
    assert resp[50].id == 50
    assert resp[150].id == 150
    assert len(resp) == 200


@responses.activate
@stub_sleep
def test_list_static_ips_with_max_items_1(zia, paginated_items):
    items = paginated_items(200)

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/staticIP",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/staticIP",
        json=items[100:200],
        status=200,
    )

    resp = zia.traffic.list_static_ips(max_items=1)

    assert isinstance(resp, list)
    assert len(resp) == 1


@responses.activate
@stub_sleep
def test_list_static_ips_with_max_items_150(zia, paginated_items):
    items = paginated_items(200)

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/staticIP",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/staticIP",
        json=items[100:200],
        status=200,
    )

    resp = zia.traffic.list_static_ips(max_items=150)

    assert isinstance(resp, list)
    assert len(resp) == 150


@responses.activate
@stub_sleep
def test_list_vips_with_one_page(zia, paginated_items):
    items = paginated_items(200)

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/vips",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/vips",
        json=items[100:200],
        status=200,
    )

    resp = zia.traffic.list_vips(max_pages=1, page_size=100)

    assert isinstance(resp, list)
    assert resp[50].id == 50
    assert len(resp) == 100


@responses.activate
@stub_sleep
def test_list_vips_with_two_pages(zia, paginated_items):
    items = paginated_items(200)

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/vips",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/vips",
        json=items[100:200],
        status=200,
    )

    resp = zia.traffic.list_vips(max_pages=2, page_size=100)

    assert isinstance(resp, list)
    assert resp[50].id == 50
    assert resp[150].id == 150
    assert len(resp) == 200


@responses.activate
@stub_sleep
def test_list_vips_with_max_items_1(zia, paginated_items):
    items = paginated_items(200)

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/vips",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/vips",
        json=items[100:200],
        status=200,
    )

    resp = zia.traffic.list_vips(max_items=1)

    assert isinstance(resp, list)
    assert len(resp) == 1


@responses.activate
@stub_sleep
def test_list_vips_with_max_items_150(zia, paginated_items):
    items = paginated_items(200)

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/vips",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/vips",
        json=items[100:200],
        status=200,
    )

    resp = zia.traffic.list_vips(max_items=150)

    assert isinstance(resp, list)
    assert len(resp) == 150


@responses.activate
@stub_sleep
def test_list_vpn_credentials_with_one_page(zia, paginated_items):
    items = paginated_items(200)

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/vpnCredentials",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/vpnCredentials",
        json=items[100:200],
        status=200,
    )

    resp = zia.traffic.list_vpn_credentials(max_pages=1, page_size=100)

    assert isinstance(resp, list)
    assert resp[50].id == 50
    assert len(resp) == 100


@responses.activate
@stub_sleep
def test_list_vpn_credentials_with_two_pages(zia, paginated_items):
    items = paginated_items(200)

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/vpnCredentials",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/vpnCredentials",
        json=items[100:200],
        status=200,
    )

    resp = zia.traffic.list_vpn_credentials(max_pages=2, page_size=100)

    assert isinstance(resp, list)
    assert resp[50].id == 50
    assert resp[150].id == 150
    assert len(resp) == 200


@responses.activate
@stub_sleep
def test_list_vpn_credentials_with_max_items_1(zia, paginated_items):
    items = paginated_items(200)

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/vpnCredentials",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/vpnCredentials",
        json=items[100:200],
        status=200,
    )

    resp = zia.traffic.list_vpn_credentials(max_items=1)

    assert isinstance(resp, list)
    assert len(resp) == 1


@responses.activate
@stub_sleep
def test_list_vpn_credentials_with_max_items_150(zia, paginated_items):
    items = paginated_items(200)

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/vpnCredentials",
        json=items[0:100],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/vpnCredentials",
        json=items[100:200],
        status=200,
    )

    resp = zia.traffic.list_vpn_credentials(max_items=150)

    assert isinstance(resp, list)
    assert len(resp) == 150
