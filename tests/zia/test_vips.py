import pytest
import responses
from box import Box, BoxList


@pytest.fixture(name="pubse_vips")
def fixture_pubse_vips():
    return {
        "zscaler.net": {
            "continent : apac": {
                "city :_auckland": [
                    {
                        "range": "124.248.141.0/24",
                        "vpn": "akl1-vpn.zscaler.net",
                        "gre": "124.248.141.8",
                        "hostname": "akl1.sme.zscaler.net",
                        "latitude": "-37",
                        "longitude": "175",
                    }
                ],
                "city :_auckland ii": [
                    {
                        "range": "136.226.248.0/23",
                        "vpn": "",
                        "gre": "",
                        "hostname": "",
                        "latitude": "-36.85088270000001",
                        "longitude": "174.7644881",
                    }
                ],
            },
            "continent : emea": {
                "city :_abu_dhabi i": [
                    {
                        "range": "147.161.174.0/23",
                        "vpn": "",
                        "gre": "",
                        "hostname": "",
                        "latitude": "24.453884",
                        "longitude": "54.3773438",
                    }
                ],
                "city :_capetown": [
                    {
                        "range": "196.23.154.64/27",
                        "vpn": "capetown1-vpn.zscaler.net",
                        "gre": "196.23.154.86",
                        "hostname": "capetown1.sme.zscaler.net",
                        "latitude": "-34",
                        "longitude": "18",
                    }
                ],
            },
            "continent :_americas": {
                "city :_boston i": [
                    {
                        "range": "136.226.70.0/23",
                        "vpn": "bos1-vpn.zscaler.net",
                        "gre": "136.226.70.20",
                        "hostname": "bos1.sme.zscaler.net",
                        "latitude": "42.3600825",
                        "longitude": "-71.0588801",
                    },
                    {
                        "range": "136.226.72.0/23",
                        "vpn": "",
                        "gre": "136.226.70.20",
                        "hostname": "",
                        "latitude": "42.3600825",
                        "longitude": "-71.0588801",
                    },
                    {
                        "range": "136.226.74.0/23",
                        "vpn": "",
                        "gre": "136.226.70.20",
                        "hostname": "",
                        "latitude": "42.3600825",
                        "longitude": "-71.0588801",
                    },
                ],
                "city :_mexico_city i": [
                    {
                        "range": "136.226.0.0/23",
                        "vpn": "mex1-vpn.zscaler.net",
                        "gre": "136.226.0.12",
                        "hostname": "mex1.sme.zscaler.net",
                        "latitude": "19.4326077",
                        "longitude": "-99.133208",
                    }
                ],
            },
        }
    }


@pytest.fixture(name="ca_vips")
def fixture_ca_vips():
    return {
        "ranges": [
            "104.129.193.85",
            "104.129.195.85",
            "104.129.197.85",
            "104.129.193.102",
            "104.129.197.102",
            "104.129.195.102",
            "165.225.73.179",
            "185.46.213.44",
            "185.46.215.209",
        ]
    }


@pytest.fixture(name="pac_vips")
def fixture_pac_vips():
    return {
        "ip": ["104.129.193.65", "104.129.195.65", "104.129.197.65", "104.129.193.103", "104.129.195.103", "104.129.197.103"]
    }


@responses.activate
def test_list_public_se(zia, pubse_vips):
    responses.add(
        method="GET",
        url="https://api.config.zscaler.com/zscaler.net/cenr/json",
        json=pubse_vips,
        status=200,
    )
    resp = zia.vips.list_public_se(cloud="zscaler")
    assert isinstance(resp, Box)
    assert resp["continent : apac"]["city :_auckland"][0].latitude == "-37"


@responses.activate
def test_list_public_se_by_continent_amer(zia, pubse_vips):
    responses.add(
        method="GET",
        url="https://api.config.zscaler.com/zscaler.net/cenr/json",
        json=pubse_vips,
        status=200,
    )
    resp = zia.vips.list_public_se(cloud="zscaler", continent="amer")
    assert isinstance(resp, Box)
    assert resp["city :_mexico_city i"][0].latitude == "19.4326077"


@responses.activate
def test_list_public_se_by_continent_other(zia, pubse_vips):
    responses.add(
        method="GET",
        url="https://api.config.zscaler.com/zscaler.net/cenr/json",
        json=pubse_vips,
        status=200,
    )
    resp = zia.vips.list_public_se(cloud="zscaler", continent="emea")
    assert isinstance(resp, Box)
    assert resp["city :_capetown"][0].latitude == "-34"


@responses.activate
def test_list_ca(zia, ca_vips):
    responses.add(
        method="GET",
        url="https://api.config.zscaler.com/zscaler.net/ca/json",
        json=ca_vips,
        status=200,
    )
    resp = zia.vips.list_ca("zscaler")
    assert isinstance(resp, BoxList)
    assert resp[0] == "104.129.193.85"


@responses.activate
def test_list_pac(zia, pac_vips):
    responses.add(
        method="GET",
        url="https://api.config.zscaler.com/zscaler.net/pac/json",
        json=pac_vips,
        status=200,
    )
    resp = zia.vips.list_pac("zscaler")
    assert isinstance(resp, BoxList)
    assert resp[0] == "104.129.193.65"
