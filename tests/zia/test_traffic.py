import pytest
import responses
from box import Box, BoxList
from responses import matchers

from tests.conftest import stub_sleep


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


@pytest.fixture(name="gre_ranges")
def fixture_gre_ranges():
    return [
        {"startIpAddress": "192.0.2.40", "endIpAddress": "192.0.2.47"},
        {"startIpAddress": "192.0.2.48", "endIpAddress": "192.0.2.55"},
        {"startIpAddress": "192.0.2.56", "endIpAddress": "192.0.2.63"},
        {"startIpAddress": "192.0.2.64", "endIpAddress": "192.0.2.71"},
        {"startIpAddress": "192.0.2.72", "endIpAddress": "192.0.2.79"},
        {"startIpAddress": "192.0.2.80", "endIpAddress": "192.0.2.87"},
        {"startIpAddress": "192.0.2.88", "endIpAddress": "192.0.2.95"},
        {"startIpAddress": "192.0.2.96", "endIpAddress": "192.0.2.103"},
        {"startIpAddress": "192.0.2.104", "endIpAddress": "192.0.2.111"},
        {"startIpAddress": "192.0.2.112", "endIpAddress": "192.0.2.119"},
    ]


@pytest.fixture(name="static_ips")
def fixture_static_ips():
    return [
        {
            "city": {"id": 1, "name": "Test, Test, Test"},
            "comment": "Test",
            "geoOverride": True,
            "id": 1,
            "ipAddress": "203.0.113.1",
            "lastModificationTime": 1620779633,
            "lastModifiedBy": {"id": 1, "name": "DEFAULT ADMIN"},
            "latitude": -1.0,
            "longitude": 1.0,
            "routableIP": True,
        },
        {
            "city": {"id": 2, "name": "Test, Test, Test"},
            "comment": "Test",
            "geoOverride": True,
            "id": 1,
            "ipAddress": "203.0.113.2",
            "lastModificationTime": 1620779633,
            "lastModifiedBy": {"id": 1, "name": "DEFAULT ADMIN"},
            "latitude": -1.0,
            "longitude": 1.0,
            "routableIP": True,
        },
    ]


@pytest.fixture(name="recommended_vips")
def fixture_recommended_vips():
    yield [
        {
            "id": 1,
            "virtualIp": "203.0.113.10",
            "privateServiceEdge": False,
            "datacenter": "TEST",
            "latitude": -1.0,
            "longitude": 1.0,
            "city": "Test A",
            "countryCode": "TT",
            "region": "Test",
        },
        {
            "id": 2,
            "virtualIp": "203.0.113.11",
            "privateServiceEdge": False,
            "datacenter": "TEST",
            "latitude": -2.0,
            "longitude": 2.0,
            "city": "Test A",
            "countryCode": "TT",
            "region": "Test",
        },
        {
            "id": 3,
            "virtualIp": "203.0.113.12",
            "privateServiceEdge": False,
            "datacenter": "TEST",
            "latitude": -3.0,
            "longitude": 3.0,
            "city": "Test B",
            "countryCode": "TT",
            "region": "Test",
        },
    ]


@pytest.fixture(name="vips")
def fixture_vips():
    return [
        {
            "cloudName": "zscaler.net",
            "region": "Oceania",
            "country": "Test",
            "city": "Test",
            "dataCenter": "TESTA",
            "location": "1 E, 1 S",
            "vpnIps": ["203.0.113.1"],
            "vpnDomainName": "test-vpn.zscaler.net",
            "greIps": ["203.0.113.2"],
            "greDomainName": "test.gre.zscaler.net",
            "pacIps": ["203.0.113.3"],
            "pacDomainName": "test.sme.zscaler.net",
            "svpnIps": ["203.0.113.4"],
            "svpnDomainName": "test.svpn.zscaler.net",
        },
        {
            "cloudName": "zscaler.net",
            "region": "Europe",
            "country": "Test",
            "city": "Test",
            "dataCenter": "TESTB",
            "location": "1 E, 1 S",
            "vpnIps": ["203.0.113.1"],
            "vpnDomainName": "test-vpn.zscaler.net",
            "greIps": ["203.0.113.2"],
            "greDomainName": "test.gre.zscaler.net",
            "pacIps": ["203.0.113.3"],
            "pacDomainName": "test.sme.zscaler.net",
            "svpnIps": ["203.0.113.4"],
            "svpnDomainName": "test.svpn.zscaler.net",
        },
    ]


@pytest.fixture(name="vpn_credentials")
def fixture_vpn_credentials():
    return [
        {
            "id": 1,
            "ipAddress": "203.0.113.1",
            "location": {"id": 1, "name": "Test"},
            "type": "IP",
        },
        {
            "fqdn": "test@example.com",
            "id": 2,
            "location": {"id": 1, "name": "Test"},
            "type": "UFQDN",
        },
    ]


@pytest.fixture(name="ipv6_prefixes")
def fixture_ipv64_prefixes():
    return [
        {"id": 0, "name": "sample1", "prefixMask": "mask1", "dnsPrefix": True},
        {"id": 1, "name": "sample2", "prefixMask": "mask2", "dnsPrefix": False},
    ]


@responses.activate
@stub_sleep
def test_list_gre_tunnels(zia, gre_tunnels):
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/greTunnels?page=1",
        json=gre_tunnels,
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/greTunnels?page=2",
        json=[],
        status=200,
    )

    resp = zia.traffic.list_gre_tunnels()

    assert isinstance(resp, BoxList)
    assert len(resp) == 2
    assert resp[0].id == 1


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
def test_list_gre_ranges(zia, gre_ranges):
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/greTunnels/availableInternalIpRanges",
        json=gre_ranges,
        status=200,
    )
    resp = zia.traffic.list_gre_ranges(internal_ip_range="192.0.2.0")
    assert isinstance(resp, BoxList)
    assert len(resp) == 10
    assert resp[0].start_ip_address == "192.0.2.40"


@responses.activate
def test_add_gre_tunnel_with_defaults(zia, gre_tunnels, recommended_vips):
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/vips/recommendedList?sourceIp=203.0.113.1",
        json=recommended_vips,
        status=200,
    )
    responses.add(
        responses.POST,
        url="https://zsapi.zscaler.net/api/v1/greTunnels",
        json=gre_tunnels[0],
        status=200,
    )
    resp = zia.traffic.add_gre_tunnel(source_ip="203.0.113.1")
    assert isinstance(resp, Box)
    assert resp.id == 1


@responses.activate
def test_add_gre_tunnel_with_params(zia, gre_tunnels, recommended_vips):
    responses.add(
        responses.POST,
        url="https://zsapi.zscaler.net/api/v1/greTunnels",
        json=gre_tunnels[0],
        status=200,
    )
    resp = zia.traffic.add_gre_tunnel(
        source_ip="203.0.113.1", primary_dest_vip_id="1", secondary_dest_vip_id="2", comment="Test"
    )
    assert isinstance(resp, Box)
    assert resp.id == 1


@responses.activate
def test_list_static_ips(zia, static_ips):
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/staticIP?ipAddress=203.0.113.0&page=1",
        json=static_ips,
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/staticIP?ipAddress=203.0.113.0&page=2",
        json=[],
        status=200,
    )
    resp = zia.traffic.list_static_ips(ip_address="203.0.113.0")
    assert isinstance(resp, BoxList)
    assert len(resp) == 2
    assert resp[0].id == 1


@responses.activate
def test_get_static_ip(zia, static_ips):
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/staticIP/1",
        json=static_ips[0],
        status=200,
    )
    resp = zia.traffic.get_static_ip("1")
    assert isinstance(resp, Box)
    assert resp.id == 1


@responses.activate
def test_add_static_ip(zia, static_ips):
    responses.add(
        responses.POST,
        url="https://zsapi.zscaler.net/api/v1/staticIP",
        json=static_ips[0],
        status=200,
    )
    resp = zia.traffic.add_static_ip(ip_address="203.0.113.1", comment="Test", routable_ip=True)
    assert isinstance(resp, Box)
    assert resp.id == 1


@responses.activate
def test_update_static_ip(zia, static_ips):
    updated_ip = static_ips[0]
    updated_ip["comment"] = "Test"
    updated_ip["geoOverride"] = False

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/staticIP/1",
        json=static_ips[0],
        status=200,
    )

    responses.add(
        responses.PUT,
        url="https://zsapi.zscaler.net/api/v1/staticIP/1",
        json=updated_ip,
        status=200,
        match=[matchers.json_params_matcher(updated_ip)],
    )

    resp = zia.traffic.update_static_ip("1", comment="Test", geo_override=False)

    assert isinstance(resp, Box)
    assert resp.id == 1
    assert resp.comment == updated_ip["comment"]
    assert resp.geo_override == updated_ip["geoOverride"]


@responses.activate
def test_delete_static_ip(zia):
    responses.add(
        responses.DELETE,
        url="https://zsapi.zscaler.net/api/v1/staticIP/1",
        status=204,
    )
    resp = zia.traffic.delete_static_ip("1")
    assert isinstance(resp, int)
    assert resp == 204


@responses.activate
def test_check_static_ip(zia):
    responses.add(
        responses.POST,
        url="https://zsapi.zscaler.net/api/v1/staticIP/validate",
        match=[matchers.json_params_matcher({"ipAddress": "203.0.113.1"})],
        status=200,
    )
    resp = zia.traffic.check_static_ip("203.0.113.1")
    assert isinstance(resp, int)
    assert resp == 200


@responses.activate
def test_list_vips_recommended(zia, recommended_vips):
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/vips/recommendedList?sourceIp=203.0.113.1&routableIP=True",
        json=recommended_vips,
        status=200,
    )
    resp = zia.traffic.list_vips_recommended(source_ip="203.0.113.1", routable_ip=True)
    assert isinstance(resp, BoxList)
    assert len(resp) == 3
    assert resp[0].id == 1


@responses.activate
def test_get_closest_diverse_vip_ids(zia, recommended_vips):
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/vips/recommendedList?sourceIp=203.0.113.1",
        json=recommended_vips,
        status=200,
    )
    resp = zia.traffic.get_closest_diverse_vip_ids(ip_address="203.0.113.1")
    assert isinstance(resp, tuple)
    assert resp == (1, 3)


@responses.activate
@stub_sleep
def test_list_vpn_credentials(zia, vpn_credentials):
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/vpnCredentials?page=1",
        json=vpn_credentials,
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/vpnCredentials?page=2",
        json=[],
        status=200,
    )

    resp = zia.traffic.list_vpn_credentials()

    assert isinstance(resp, BoxList)
    assert len(resp) == 2
    assert resp[0].id == 1


@responses.activate
def test_add_vpn_credentials(zia, vpn_credentials):
    responses.add(
        responses.POST,
        url="https://zsapi.zscaler.net/api/v1/vpnCredentials",
        json=vpn_credentials[0],
        status=200,
    )
    resp = zia.traffic.add_vpn_credential(authentication_type="IP", pre_shared_key="Test", location_id="1", comments="Test")
    assert isinstance(resp, Box)
    assert resp.id == 1


@responses.activate
def test_bulk_delete_vpn_credentials(zia):
    responses.add(
        responses.POST,
        url="https://zsapi.zscaler.net/api/v1/vpnCredentials/bulkDelete",
        status=200,
    )
    resp = zia.traffic.bulk_delete_vpn_credentials(["1", "2"])
    assert isinstance(resp, int)
    assert resp == 200


@responses.activate
def test_get_vpn_credential_by_id(zia, vpn_credentials):
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/vpnCredentials/1",
        json=vpn_credentials[0],
        status=200,
    )
    resp = zia.traffic.get_vpn_credential("1")
    assert isinstance(resp, Box)
    assert resp.id == 1


@responses.activate
@stub_sleep
def test_get_vpn_credential_by_fqdn(zia, vpn_credentials):
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/vpnCredentials?search=test@example.com&page=1",
        json=[vpn_credentials[1]],
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/vpnCredentials?search=test@example.com&page=2",
        json=[],
        status=200,
    )
    resp = zia.traffic.get_vpn_credential(fqdn="test@example.com")
    assert isinstance(resp, Box)
    assert resp.id == 2


def test_get_vpn_credential_error(zia):
    with pytest.raises(Exception):
        zia.traffic.get_vpn_credential("1", "test@example.com")


@responses.activate
def test_update_vpn_credentials(zia, vpn_credentials):
    updated_credential = vpn_credentials[0]
    updated_credential["comments"] = "Test"
    updated_credential["preSharedKey"] = "Test"
    updated_credential["location"] = {"id": "2"}

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/vpnCredentials/1",
        json=vpn_credentials[0],
        status=200,
    )

    responses.add(
        responses.PUT,
        url="https://zsapi.zscaler.net/api/v1/vpnCredentials/1",
        json=updated_credential,
        status=200,
        match=[matchers.json_params_matcher(updated_credential)],
    )
    resp = zia.traffic.update_vpn_credential("1", comments="Test", pre_shared_key="Test", location_id="2")

    assert isinstance(resp, Box)
    assert resp.id == 1
    assert resp.comments == updated_credential["comments"]
    assert resp.pre_shared_key == updated_credential["preSharedKey"]
    assert resp.location == updated_credential["location"]


@responses.activate
def test_delete_vpn_credential(zia):
    responses.add(
        responses.DELETE,
        url="https://zsapi.zscaler.net/api/v1/vpnCredentials/1",
        status=204,
    )
    resp = zia.traffic.delete_vpn_credential("1")
    assert isinstance(resp, int)
    assert resp == 204


@responses.activate
@stub_sleep
def test_list_vips(zia, vips):
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/vips?page=1",
        json=vips,
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/vips?page=2",
        json=[],
        status=200,
    )

    resp = zia.traffic.list_vips()

    assert isinstance(resp, BoxList)
    assert len(resp) == 2
    assert resp[0].data_center == "TESTA"


@responses.activate
def test_list_dns64_prefixes(zia, ipv6_prefixes):
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/ipv6config/dns64prefix",
        json=ipv6_prefixes,
        status=200,
    )
    resp = zia.traffic.list_dns64_prefixes()
    assert isinstance(resp, BoxList)
    assert len(resp) == 2


@stub_sleep
@responses.activate
def test_list_nat64_prefixes(zia, ipv6_prefixes):
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/ipv6config/nat64prefix?page=1",
        json=ipv6_prefixes,
        status=200,
    )
    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/ipv6config/nat64prefix?page=2",
        json=[],
        status=200,
    )
    resp = zia.traffic.list_nat64_prefixes()
    assert isinstance(resp, BoxList)
    assert len(resp) == 2


@responses.activate
def test_list_gre_ip_addresses(zia):
    gre_ip_addresses_data = [
        {"ipAddress": "192.168.1.1", "greEnabled": True, "greTunnelIP": "10.0.0.1"},
        {"ipAddress": "192.168.1.2", "greEnabled": False, "greTunnelIP": "10.0.0.2"},
    ]

    responses.add(
        responses.GET,
        url="https://zsapi.zscaler.net/api/v1/orgProvisioning/ipGreTunnelInfo",
        json=gre_ip_addresses_data,
        status=200,
    )
    resp = zia.traffic.list_gre_ip_addresses()
    assert isinstance(resp, BoxList)
    assert len(resp) == 2
