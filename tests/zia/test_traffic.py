import pytest
import responses
from box import Box


@pytest.fixture(name="gre_tunnels")
def fixture_gre_tunnels():
    return [
        {
            "id": 1,
            "sourceIp": "1.1.1.1",
            "primaryDestVip": {
                "id": 1,
                "virtualIp": "1.1.1.1",
                "privateServiceEdge": False,
                "datacenter": "TESTA",
                "latitude": -1.0,
                "longitude": 1.0,
                "city": "Test",
                "countryCode": "TEST  ",
                "region": "Test",
            },
            "secondaryDestVip": {
                "id": 2,
                "virtualIp": "1.1.1.1",
                "privateServiceEdge": False,
                "datacenter": "TESTB",
                "latitude": -2.0,
                "longitude": 2.0,
                "city": "Test",
                "countryCode": "TEST  ",
                "region": "Test",
            },
            "internalIpRange": "1.1.1.1",
            "last_modification_time": 1,
            "lastModifiedBy": {"id": 1, "name": "DEFAULT ADMIN"},
            "comment": "Test",
            "ipUnnumbered": False,
        },
        {
            "id": 2,
            "sourceIp": "1.1.1.1",
            "primaryDestVip": {
                "id": 1,
                "virtualIp": "1.1.1.1",
                "privateServiceEdge": False,
                "datacenter": "TESTA",
                "latitude": -1.0,
                "longitude": 1.0,
                "city": "Test",
                "countryCode": "TEST  ",
                "region": "Test",
            },
            "secondaryDestVip": {
                "id": 2,
                "virtualIp": "1.1.1.1",
                "privateServiceEdge": False,
                "datacenter": "TESTB",
                "latitude": -2.0,
                "longitude": 2.0,
                "city": "Test",
                "countryCode": "TEST  ",
                "region": "Test",
            },
            "internalIpRange": "1.1.1.1",
            "last_modification_time": 1,
            "lastModifiedBy": {"id": 1, "name": "DEFAULT ADMIN"},
            "comment": "Test",
            "ipUnnumbered": False,
        },
    ]


@responses.activate
def test_get_gre_tunnel(zia, gre_tunnels):
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/greTunnels/1",
        json=gre_tunnels[0],
        status=200,
    )

    resp = zia.traffic.get_gre_tunnel("1")

    assert isinstance(resp, Box)
    assert resp.id == 1


@responses.activate
def test_list_gre_ranges(zia):
    pass


@responses.activate
def test_add_gre_tunnel(zia):
    pass


@responses.activate
def test_get_static_ip(zia):
    pass


@responses.activate
def test_add_static_ip(zia):
    pass


@responses.activate
def test_check_static_ip(zia):
    pass


@responses.activate
def test_update_static_ip(zia):
    pass


@responses.activate
def test_delete_static_ip(zia):
    pass


@responses.activate
def test_list_vips_recommended(zia):
    pass


@responses.activate
def test_get_closest_diverse_vip_ids(zia):
    pass


@responses.activate
def test_add_vpn_credentials(zia):
    pass


@responses.activate
def test_bulk_delete_vpn_credentials(zia):
    pass


@responses.activate
def test_get_vpn_credentials(zia):
    pass


@responses.activate
def test_update_vpn_credentials(zia):
    pass


@responses.activate
def test_delete_vpn_credential(zia):
    pass

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
