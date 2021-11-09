import pytest
import responses
from box import Box, BoxList
from responses import matchers


@pytest.fixture(name="firewall_rules")
def fixture_firewall_rules():
    yield [
        {
            "accessControl": "READ_WRITE",
            "enableFullLogging": False,
            "id": 1,
            "name": "Default Firewall Filtering Rule",
            "order": -1,
            "rank": 7,
            "action": "BLOCK_DROP",
            "state": "ENABLED",
            "destIpCategories": [],
            "destCountries": [],
            "predefined": False,
            "defaultRule": True,
        },
        {
            "accessControl": "READ_WRITE",
            "enableFullLogging": False,
            "id": 2,
            "name": "Test",
            "order": 5,
            "rank": 7,
            "action": "ALLOW",
            "state": "ENABLED",
            "destIpCategories": [],
            "destCountries": [],
            "nwServices": [
                {"id": 1, "name": "ICMP_ANY", "isNameL10nTag": True},
                {"id": 2, "name": "QUIC", "isNameL10nTag": True},
            ],
            "predefined": False,
            "defaultRule": False,
        },
    ]


@pytest.fixture(name="ip_destination_groups")
def fixture_ip_destination_groups():
    yield [
        {
            "id": 1,
            "name": "Test 1",
            "type": "DSTN_FQDN",
            "addresses": ["www.example.com", "example.com"],
            "description": "Test",
            "ipCategories": [],
            "countries": [],
            "urlCategories": [],
            "ipAddresses": ["www.example.com", "example.com"],
        },
        {
            "id": 2,
            "name": "Test 2",
            "type": "DSTN_IP",
            "addresses": ["1.1.1.1", "8.8.8.8"],
            "description": "Test",
            "ipCategories": [],
            "countries": [],
            "urlCategories": [],
            "ipAddresses": ["1.1.1.1", "8.8.8.8"],
        },
    ]


@pytest.fixture(name="ip_source_groups")
def fixture_ip_source_groups():
    yield [
        {"id": 1, "name": "Test 1", "ipAddresses": ["1.1.1.1", "8.8.8.8"], "description": "Test"},
        {"id": 2, "name": "Test 2", "ipAddresses": ["2.2.2.2", "9.9.9.9"], "description": "Test"},
    ]


@pytest.fixture(name="network_application_groups")
def fixture_network_application_groups():
    yield [
        {"id": 1, "name": "Test 1", "networkApplications": ["YAMMER", "OFFICE365"], "description": "Test 1"},
        {"id": 1, "name": "Test 2", "networkApplications": ["SHAREPOINT_ONLINE", "ONEDRIVE"], "description": "Test 2"},
    ]


@pytest.fixture(name="network_applications")
def fixture_network_applications():
    yield [
        {"id": "TEST1", "parentCategory": "APP_SERVICE", "description": "TEST1_DESC", "deprecated": False},
        {"id": "TEST2", "parentCategory": "APP_SERVICE", "description": "TEST2_DESC", "deprecated": True},
    ]


@pytest.fixture(name="network_service_groups")
def fixture_network_service_groups():
    yield [
        {"id": 1, "description": "Test", "name": "Test 1", "services": [{"id": 1, "name": "SSH", "isNameL10nTag": True}]},
        {"id": 2, "name": "Test 2", "services": [{"id": 2, "name": "TELNET", "isNameL10nTag": True}]},
    ]


@pytest.fixture(name="network_services")
def fixture_network_services():
    yield [
        {
            "id": 1,
            "name": "TEST_ANY",
            "tag": "TEST_ANY",
            "type": "STANDARD",
            "description": "TEST_ANY_DESC",
            "isNameL10nTag": True,
        },
        {
            "id": 2,
            "name": "TEST",
            "tag": "TEST",
            "srcTcpPorts": [],
            "destTcpPorts": [{"start": 1}, {"end": 2}],
            "srcUdpPorts": [],
            "destUdpPorts": [{"start": 1}],
            "type": "PREDEFINED",
            "description": "TEST_DESC",
            "isNameL10nTag": True,
        },
    ]


@responses.activate
def test_firewall_list_rules(zia, firewall_rules):
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/firewallFilteringRules",
        json=firewall_rules,
        status=200,
    )

    resp = zia.firewall.list_rules()
    assert isinstance(resp, BoxList)
    assert resp[0].id == 1
    assert len(resp) == 2


@responses.activate
def test_firewall_add_rule(zia, firewall_rules):
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/firewallFilteringRules",
        json=firewall_rules,
        status=200,
    )
    responses.add(
        method="POST",
        url="https://zsapi.zscaler.net/api/v1/firewallFilteringRules",
        json=firewall_rules[1],
        status=200,
        match=[
            matchers.json_params_matcher(
                {
                    "name": "Test",
                    "action": "ALLOW",
                    "order": "5",
                    "state": "ENABLED",
                    "nwServices": [{"id": "1"}, {"id": "2"}],
                }
            )
        ],
    )
    resp = zia.firewall.add_rule(name="Test", action="ALLOW", order="5", state="ENABLED", nw_services=["1", "2"])

    assert isinstance(resp, Box)
    assert resp.id == 2


@responses.activate
def test_firewall_get_rule(zia, firewall_rules):
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/firewallFilteringRules/1",
        json=firewall_rules[0],
        status=200,
    )

    resp = zia.firewall.get_rule("1")
    assert isinstance(resp, Box)
    assert resp.id == 1


@responses.activate
def test_firewall_update_rule(zia, firewall_rules):
    updated_rule = firewall_rules[1]
    updated_rule["name"] = "Test Update"
    updated_rule["nwServices"] = [{"id": "3"}]

    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/firewallFilteringRules/1",
        json=firewall_rules[1],
        status=200,
    )
    responses.add(
        method="PUT",
        url="https://zsapi.zscaler.net/api/v1/firewallFilteringRules/1",
        json=updated_rule,
        status=200,
        match=[matchers.json_params_matcher(updated_rule)],
    )
    resp = zia.firewall.update_rule("1", name="Test Update", nw_services=["3"])
    assert isinstance(resp, Box)
    assert resp.name == updated_rule["name"]
    assert resp.nw_services == updated_rule["nwServices"]


@responses.activate
def test_firewall_delete_rule(zia):
    responses.add(
        method="DELETE",
        url="https://zsapi.zscaler.net/api/v1/firewallFilteringRules/1",
        status=200,
    )
    resp = zia.firewall.delete_rule("1")
    assert isinstance(resp, int)
    assert resp == 200


@responses.activate
def test_firewall_list_ip_destination_groups(zia, ip_destination_groups):
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/ipDestinationGroups",
        json=ip_destination_groups,
        status=200,
    )

    resp = zia.firewall.list_ip_destination_groups()
    assert isinstance(resp, BoxList)
    assert len(resp) == 2
    assert resp[0].id == 1


@responses.activate
def test_firewall_get_ip_destination_group(zia, ip_destination_groups):
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/ipDestinationGroups/1",
        json=ip_destination_groups[0],
        status=200,
    )

    resp = zia.firewall.get_ip_destination_group("1")
    assert isinstance(resp, Box)
    assert resp.id == 1


@responses.activate
def test_firewall_delete_ip_destination_group(zia):
    responses.add(
        method="DELETE",
        url="https://zsapi.zscaler.net/api/v1/ipDestinationGroups/1",
        status=200,
    )
    resp = zia.firewall.delete_ip_destination_group(1)
    assert isinstance(resp, int)
    assert resp == 200


@responses.activate
def test_firewall_add_ip_destination_group(zia, ip_destination_groups):
    responses.add(
        method="POST",
        url="https://zsapi.zscaler.net/api/v1/ipDestinationGroups",
        json=ip_destination_groups[0],
        status=200,
        match=[
            matchers.json_params_matcher(
                {"name": "Test 1", "type": "DSTN_FQDN", "addresses": ["www.example.com", "example.com"], "description": "Test"}
            )
        ],
    )
    resp = zia.firewall.add_ip_destination_group(
        name="Test 1", type="DSTN_FQDN", addresses=["www.example.com", "example.com"], description="Test"
    )
    assert isinstance(resp, Box)
    assert resp.id == 1
    assert resp.addresses[0] == "www.example.com"


@responses.activate
def test_firewall_update_ip_destination_group(zia, ip_destination_groups):
    updated_destination_group = ip_destination_groups[0]
    updated_destination_group["name"] = "Test Updated"

    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/ipDestinationGroups/1",
        json=ip_destination_groups[0],
        status=200,
    )

    responses.add(
        method="PUT",
        url="https://zsapi.zscaler.net/api/v1/ipDestinationGroups/1",
        json=updated_destination_group,
        status=200,
        match=[matchers.json_params_matcher(updated_destination_group)],
    )
    resp = zia.firewall.update_ip_destination_group("1", name="Test Updated")
    assert isinstance(resp, Box)
    assert resp.id == updated_destination_group["id"]
    assert resp.name == updated_destination_group["name"]


@responses.activate
def test_list_ip_source_groups(zia, ip_source_groups):
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/ipSourceGroups",
        json=ip_source_groups,
        status=200,
    )

    resp = zia.firewall.list_ip_source_groups()
    assert isinstance(resp, BoxList)
    assert len(resp) == 2
    assert resp[0].id == 1


@responses.activate
def test_get_ip_source_group(zia, ip_source_groups):
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/ipSourceGroups/1",
        json=ip_source_groups[0],
        status=200,
    )

    resp = zia.firewall.get_ip_source_group(1)
    assert isinstance(resp, Box)
    assert resp.id == 1


@responses.activate
def test_delete_ip_source_group(zia):
    responses.add(
        method="DELETE",
        url="https://zsapi.zscaler.net/api/v1/ipSourceGroups/1",
        status=200,
    )
    resp = zia.firewall.delete_ip_source_group("1")
    assert isinstance(resp, int)
    assert resp == 200


@responses.activate
def test_add_ip_source_group(zia, ip_source_groups):
    responses.add(
        method="POST",
        url="https://zsapi.zscaler.net/api/v1/ipSourceGroups",
        json=ip_source_groups[0],
        status=200,
        match=[matchers.json_params_matcher({"name": "Test 1", "ipAddresses": ["1.1.1.1", "8.8.8.8"], "description": "Test"})],
    )
    resp = zia.firewall.add_ip_source_group(name="Test 1", ip_addresses=["1.1.1.1", "8.8.8.8"], description="Test")

    assert isinstance(resp, Box)
    assert resp.id == 1
    assert resp.ip_addresses[0] == "1.1.1.1"


@responses.activate
def test_update_ip_source_group(zia, ip_source_groups):
    updated_source_group = ip_source_groups[0]
    updated_source_group["name"] = "Test Updated"

    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/ipSourceGroups/1",
        json=ip_source_groups[0],
        status=200,
    )

    responses.add(
        method="PUT",
        url="https://zsapi.zscaler.net/api/v1/ipSourceGroups/1",
        json=ip_source_groups[0],
        status=200,
        match=[matchers.json_params_matcher(updated_source_group)],
    )
    resp = zia.firewall.update_ip_source_group("1", name="Test Updated")

    assert isinstance(resp, Box)
    assert resp.id == updated_source_group["id"]
    assert resp.name == updated_source_group["name"]


@responses.activate
def test_list_network_app_groups(zia, network_application_groups):
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/networkApplicationGroups",
        json=network_application_groups,
        status=200,
    )
    resp = zia.firewall.list_network_app_groups()
    assert isinstance(resp, BoxList)
    assert len(resp) == 2
    assert resp[0].id == 1


@responses.activate
def test_get_network_app_group(zia, network_application_groups):
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/networkApplicationGroups/1",
        json=network_application_groups[0],
        status=200,
    )
    resp = zia.firewall.get_network_app_group("1")
    assert isinstance(resp, Box)
    assert resp.id == 1


@responses.activate
def test_list_network_apps(zia, network_applications):
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/networkApplications",
        json=network_applications,
        status=200,
    )
    resp = zia.firewall.list_network_apps()
    assert isinstance(resp, BoxList)
    assert len(resp) == 2
    assert resp[0].id == "TEST1"


@responses.activate
def test_get_network_app(zia, network_applications):
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/networkApplications/1",
        json=network_applications[0],
        status=200,
    )
    resp = zia.firewall.get_network_app("1")
    assert isinstance(resp, Box)
    assert resp.id == "TEST1"


@responses.activate
def test_list_network_svc_groups(zia, network_service_groups):
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/networkServiceGroups",
        json=network_service_groups,
        status=200,
    )
    resp = zia.firewall.list_network_svc_groups()
    assert isinstance(resp, BoxList)
    assert len(resp) == 2
    assert resp[0].id == 1


@responses.activate
def test_get_network_svc_group(zia, network_service_groups):
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/networkServiceGroups/1",
        json=network_service_groups[0],
        status=200,
    )
    resp = zia.firewall.get_network_svc_group("1")
    assert isinstance(resp, Box)
    assert resp.id == 1


@responses.activate
def test_delete_network_svc_group(zia):
    responses.add(
        method="DELETE",
        url="https://zsapi.zscaler.net/api/v1/networkServiceGroups/1",
        status=200,
    )
    resp = zia.firewall.delete_network_svc_group("1")
    assert isinstance(resp, int)
    assert resp == 200


@responses.activate
def test_add_network_svc_group(zia, network_service_groups):
    responses.add(
        method="POST",
        url="https://zsapi.zscaler.net/api/v1/networkServiceGroups",
        json=network_service_groups[0],
        status=200,
        match=[
            matchers.json_params_matcher(
                {
                    "name": "Test 1",
                    "description": "Test",
                    "services": [{"id": 1}, {"id": 2}],
                }
            )
        ],
    )
    resp = zia.firewall.add_network_svc_group(name="Test 1", description="Test", service_ids=[1, 2])

    assert isinstance(resp, Box)
    assert resp.id == 1
    assert resp.services[0].name == "SSH"


@responses.activate
def test_list_network_services(zia, network_services):
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/networkServices",
        json=network_services,
        status=200,
    )
    resp = zia.firewall.list_network_services()
    assert isinstance(resp, BoxList)
    assert len(resp) == 2
    assert resp[0].id == 1


@responses.activate
def test_get_network_service(zia, network_services):
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/networkServices/1",
        json=network_services[0],
        status=200,
    )
    resp = zia.firewall.get_network_service("1")
    assert isinstance(resp, Box)
    assert resp.id == 1


@responses.activate
def test_delete_network_service(zia):
    responses.add(
        method="DELETE",
        url="https://zsapi.zscaler.net/api/v1/networkServices/1",
        status=200,
    )
    resp = zia.firewall.delete_network_service("1")
    assert isinstance(resp, int)
    assert resp == 200


@responses.activate
def test_add_network_service(zia, network_services):
    responses.add(
        method="POST",
        url="https://zsapi.zscaler.net/api/v1/networkServices",
        json=network_services[1],
        status=200,
        match=[
            matchers.json_params_matcher(
                {"name": "TEST", "description": "Test", "destTcpPorts": [{"start": 1}], "destUdpPorts": [{"start": 1}]}
            )
        ],
    )
    resp = zia.firewall.add_network_service(name="TEST", description="Test", ports=[("dest", "tcp", 1, 2), ("dest", "udp", 1)])

    assert isinstance(resp, Box)
    assert resp.id == 2
    assert resp.dest_tcp_ports[0].start == 1


@responses.activate
def test_update_network_service(zia, network_services):
    updated_network_service = network_services[1]
    updated_network_service["description"] = "Updated Description"
    updated_network_service["destUdpPorts"] = [{"start": 1}, {"end": 2}]

    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/networkServices/2",
        json=network_services[1],
        status=200,
    )

    responses.add(
        method="PUT",
        url="https://zsapi.zscaler.net/api/v1/networkServices/2",
        json=updated_network_service,
        status=200,
        match=[matchers.json_params_matcher(updated_network_service)],
    )
    resp = zia.firewall.update_network_service(
        "2", name="TEST", description="Updated Description", ports=[("dest", "tcp", 1, 2), ("dest", "udp", 1, 2)]
    )

    assert isinstance(resp, Box)
    assert resp.id == 2
    assert resp.dest_udp_ports[1].end == 2
