import responses
from box import Box, BoxList


@responses.activate
def test_list_devices(zdx):
    url = "https://api.zdxcloud.net/v1/devices"
    mock_response = {
        "devices": [
            {"id": 40176154, "name": "LAPTOP-DQG97O6G (LENOVO 20WNS1HM01 Microsoft Windows 10 Pro;64 bit)", "userid": 76676623}
        ],
        "next_offset": "67677666",
    }
    responses.add(responses.GET, url, json=mock_response, status=200)

    result = zdx.devices.list_devices()

    assert isinstance(result, Box)
    assert result.devices[0].id == mock_response["devices"][0]["id"]


@responses.activate
def test_get_device(zdx):
    device_id = "30989301"
    url = f"https://api.zdxcloud.net/v1/devices/{device_id}"
    mock_response = {  # your large mock response here, truncated for brevity
        "id": 30989301,
        "name": "LAPTOP-S1IN4SIH (LENOVO 20T1S0Q303 Microsoft Windows 10 Pro;64 bit)",
        # More fields...
    }
    responses.add(responses.GET, url, json=mock_response, status=200)

    result = zdx.devices.get_device(device_id)

    assert isinstance(result, Box)
    assert result.id == mock_response["id"]
    assert result.name == mock_response["name"]


@responses.activate
def test_get_device_apps(zdx):
    device_id = "123456789"
    url = f"https://api.zdxcloud.net/v1/devices/{device_id}/apps"
    mock_response = [{"id": 1, "name": "Sharepoint", "score": 81}, {"id": 4, "name": "Salesforce", "score": 90}]
    responses.add(responses.GET, url, json=mock_response, status=200)

    result = zdx.devices.get_device_apps(device_id)

    assert isinstance(result, BoxList)
    assert len(result) == len(mock_response)
    for res, expected in zip(result, mock_response):
        assert res == Box(expected)


@responses.activate
def test_get_device_app(zdx):
    device_id = "123456789"
    app_id = "987654321"
    url = f"https://api.zdxcloud.net/v1/devices/{device_id}/apps/{app_id}"
    mock_response = {
        "metric": "score",
        "datapoints": [
            {"timestamp": 1644163200, "value": 80},
        ],
    }
    responses.add(responses.GET, url, json=mock_response, status=200)

    result = zdx.devices.get_device_app(device_id, app_id)

    assert isinstance(result, Box)
    assert result == Box(mock_response)


@responses.activate
def test_get_web_probes(zdx):
    device_id = "123456789"
    app_id = "987654321"
    url = f"https://api.zdxcloud.net/v1/devices/{device_id}/apps/{app_id}/web-probes"
    mock_response = [{"id": 4, "name": "Outlook Online Login Page Probe", "num_probes": 24, "avg_score": 85, "avg_pft": 2340}]
    responses.add(responses.GET, url, json=mock_response, status=200)

    result = zdx.devices.get_web_probes(device_id, app_id)

    assert isinstance(result, BoxList)
    assert len(result) == len(mock_response)
    for res, expected in zip(result, mock_response):
        assert res == Box(expected)


@responses.activate
def test_get_web_probe(zdx):
    device_id = "123456789"
    app_id = "987654321"
    probe_id = "123987456"
    url = f"https://api.zdxcloud.net/v1/devices/{device_id}/apps/{app_id}/web-probes/{probe_id}"
    mock_response = {"metric": "string", "unit": "string", "datapoints": [{"timestamp": 0, "value": 0}]}
    responses.add(responses.GET, url, json=mock_response, status=200)

    result = zdx.devices.get_web_probe(device_id, app_id, probe_id)

    assert isinstance(result, Box)
    assert result == Box(mock_response)


@responses.activate
def test_list_cloudpath_probes(zdx):
    device_id = "123456789"
    app_id = "987654321"
    url = f"https://api.zdxcloud.net/v1/devices/{device_id}/apps/{app_id}/cloudpath-probes"
    mock_response = [
        {
            "id": 4,
            "name": "Outlook Online CloudPath Probe",
            "num_probes": 12,
            "avg_latencies": [
                {"leg_src": "client", "leg_dst": "egress", "latency": 15},
                {"leg_src": "egress", "leg_dst": "zen", "latency": 34},
            ],
        }
    ]
    responses.add(responses.GET, url, json=mock_response, status=200)

    result = zdx.devices.list_cloudpath_probes(device_id, app_id)

    assert isinstance(result, BoxList)
    assert len(result) == len(mock_response)
    for res, expected in zip(result, mock_response):
        assert res == Box(expected)


@responses.activate
def test_get_cloudpath_probe(zdx):
    device_id = "123456789"
    app_id = "987654321"
    probe_id = "123987456"
    url = f"https://api.zdxcloud.net/v1/devices/{device_id}/apps/{app_id}/cloudpath-probes/{probe_id}"
    mock_response = {
        "leg_src": "string",
        "leg_dst": "string",
        "stats": [{"metric": "string", "unit": "string", "datapoints": [{"timestamp": 0, "value": 0}]}],
    }
    responses.add(responses.GET, url, json=mock_response, status=200)

    result = zdx.devices.get_cloudpath_probe(device_id, app_id, probe_id)

    assert isinstance(result, Box)
    assert result == Box(mock_response)


@responses.activate
def test_get_cloudpath(zdx):
    device_id = "123456789"
    app_id = "987654321"
    probe_id = "123987456"
    url = f"https://api.zdxcloud.net/v1/devices/{device_id}/apps/{app_id}/cloudpath-probes/{probe_id}/cloudpath"
    mock_response = {
        "timestamp": 0,
        "cloudpath": {
            "src": "string",
            "dst": "string",
            "num_hops": 0,
            "latency": 0,
        },
    }
    responses.add(responses.GET, url, json=mock_response, status=200)

    result = zdx.devices.get_cloudpath(device_id, app_id, probe_id)

    assert isinstance(result, Box)
    assert result == Box(mock_response)


@responses.activate
def test_get_call_quality_metrics(zdx):
    device_id = "123456789"
    app_id = "987654321"
    url = f"https://api.zdxcloud.net/v1/devices/{device_id}/apps/{app_id}/call-quality-metrics"
    mock_response = {
        "meet_id": "string",
        "meet_session_id": "string",
        "meet_subject": "string",
        "metrics": [{"metric": "string", "unit": "string", "datapoints": [{"timestamp": 0, "value": 0}]}],
    }
    responses.add(responses.GET, url, json=mock_response, status=200)

    result = zdx.devices.get_call_quality_metrics(device_id, app_id)

    assert isinstance(result, Box)
    assert result == Box(mock_response)


@responses.activate
def test_get_health_metrics(zdx):
    device_id = "123456789"
    url = f"https://api.zdxcloud.net/v1/devices/{device_id}/health-metrics"
    mock_response = {
        "category": "string",
        "instances": [
            {
                "name": "string",
                "metrics": [{"metric": "string", "unit": "string", "datapoints": [{"timestamp": 0, "value": 0}]}],
            }
        ],
    }
    responses.add(responses.GET, url, json=mock_response, status=200)

    result = zdx.devices.get_health_metrics(device_id)

    assert isinstance(result, Box)
    assert result == Box(mock_response)


@responses.activate
def test_get_events(zdx):
    device_id = "123456789"
    url = f"https://api.zdxcloud.net/v1/devices/{device_id}/events"
    mock_response = [
        {
            "timestamp": 1643525900,
            "events": [
                {"category": "Zscaler", "name": "tunType", "display_name": "Tunnel Change", "prev": "0", "curr": "3"},
            ],
        },
    ]
    responses.add(responses.GET, url, json=mock_response, status=200)

    result = zdx.devices.get_events(device_id)

    assert isinstance(result, BoxList)
    assert len(result) == len(mock_response)
    for res, expected in zip(result, mock_response):
        assert res == Box(expected)


@responses.activate
def test_list_deeptraces(zdx):
    device_id = "123456789"
    url = f"https://api.zdxcloud.net/v1/devices/{device_id}/deeptraces"
    mock_response = [
        {
            "trace_id": 0,
            "trace_details": {
                "session_name": "string",
                "user_id": 0,
                "username": "string",
                "device_id": 0,
                "device_name": "string",
                "web_probe_id": 0,
                "web_probe_name": "string",
            },
            "status": "not_started",
            "created_at": 0,
            "started_at": 0,
            "ended_at": 0,
        },
    ]
    responses.add(responses.GET, url, json=mock_response, status=200)

    result = zdx.devices.list_deeptraces(device_id)

    assert isinstance(result, BoxList)
    assert len(result) == len(mock_response)
    for res, expected in zip(result, mock_response):
        assert res == Box(expected)


@responses.activate
def test_start_deeptrace(zdx):
    device_id = "123456789"
    app_id = "987654321"
    session_name = "My Deeptrace"
    url = f"https://api.zdxcloud.net/v1/devices/{device_id}/deeptraces"
    mock_response = {"trace_id": 0, "status": "not_started", "expected_time": 0}
    responses.add(responses.POST, url, json=mock_response, status=200)

    result = zdx.devices.start_deeptrace(device_id, app_id, session_name)

    assert isinstance(result, Box)
    assert result == Box(mock_response)


@responses.activate
def test_get_deeptrace(zdx):
    device_id = "123456789"
    trace_id = "987654321"
    url = f"https://api.zdxcloud.net/v1/devices/{device_id}/deeptraces/{trace_id}"
    mock_response = {
        "trace_id": 0,
        "trace_details": {
            "session_name": "string",
            "user_id": 0,
            "username": "string",
            "device_id": 0,
            "device_name": "string",
            "web_probe_id": 0,
            "web_probe_name": "string",
        },
        "status": "not_started",
        "created_at": 0,
        "started_at": 0,
        "ended_at": 0,
    }
    responses.add(responses.GET, url, json=mock_response, status=200)

    result = zdx.devices.get_deeptrace(device_id, trace_id)

    assert isinstance(result, Box)
    assert result == Box(mock_response)


@responses.activate
def test_delete_deeptrace(zdx):
    device_id = "123456789"
    trace_id = "987654321"
    url = f"https://api.zdxcloud.net/v1/devices/{device_id}/deeptraces/{trace_id}"
    mock_response = {"trace_id": 0}
    responses.add(responses.DELETE, url, json=mock_response, status=200)

    result = zdx.devices.delete_deeptrace(device_id, trace_id)

    assert isinstance(result.trace_id, int)
    assert result == (mock_response)


@responses.activate
def test_get_deeptrace_webprobe_metrics(zdx):
    device_id = "123456789"
    trace_id = "987654321"
    url = f"https://api.zdxcloud.net/v1/devices/{device_id}/deeptraces/{trace_id}/webprobe-metrics"
    mock_response = {"metric": "string", "unit": "string", "datapoints": [{"timestamp": 0, "value": 0}]}
    responses.add(responses.GET, url, json=mock_response, status=200)

    result = zdx.devices.get_deeptrace_webprobe_metrics(device_id, trace_id)

    assert isinstance(result, Box)
    assert result == Box(mock_response)


@responses.activate
def test_get_deeptrace_cloudpath_metrics(zdx):
    device_id = "123456789"
    trace_id = "987654321"
    url = f"https://api.zdxcloud.net/v1/devices/{device_id}/deeptraces/{trace_id}/cloudpath-metrics"
    mock_response = {
        "leg_src": "string",
        "leg_dst": "string",
        "stats": [{"metric": "string", "unit": "string", "datapoints": [{"timestamp": 0, "value": 0}]}],
    }
    responses.add(responses.GET, url, json=mock_response, status=200)

    result = zdx.devices.get_deeptrace_cloudpath_metrics(device_id, trace_id)

    assert isinstance(result, Box)
    assert result == Box(mock_response)


@responses.activate
def test_get_deeptrace_cloudpath(zdx):
    device_id = "123456789"
    trace_id = "987654321"
    url = f"https://api.zdxcloud.net/v1/devices/{device_id}/deeptraces/{trace_id}/cloudpath"
    mock_response = {
        "timestamp": 0,
        "cloudpath": {
            "src": "string",
            "dst": "string",
            "num_hops": 0,
            "latency": 0,
            "loss": 0,
            "num_unresp_hops": 0,
            "tunnel_type": 0,
            "hops": [
                {
                    "ip": "string",
                    "gw_mac": "string",
                    "gw_mac_vendor": "string",
                    "pkt_sent": 0,
                    "pkt_rcvd": 0,
                    "latency_min": 0,
                    "latency_max": 0,
                    "latency_avg": 0,
                    "latency_diff": 0,
                }
            ],
        },
    }
    responses.add(responses.GET, url, json=mock_response, status=200)

    result = zdx.devices.get_deeptrace_cloudpath(device_id, trace_id)

    assert isinstance(result, Box)
    assert result == Box(mock_response)


@responses.activate
def test_get_deeptrace_health_metrics(zdx):
    device_id = "123456789"
    trace_id = "987654321"
    url = f"https://api.zdxcloud.net/v1/devices/{device_id}/deeptraces/{trace_id}/health-metrics"
    mock_response = {
        "category": "string",
        "instances": [
            {
                "name": "string",
                "metrics": [{"metric": "string", "unit": "string", "datapoints": [{"timestamp": 0, "value": 0}]}],
            }
        ],
    }
    responses.add(responses.GET, url, json=mock_response, status=200)

    result = zdx.devices.get_deeptrace_health_metrics(device_id, trace_id)

    assert isinstance(result, Box)
    assert result == Box(mock_response)


@responses.activate
def test_get_deeptrace_events(zdx):
    device_id = "123456789"
    trace_id = "987654321"
    url = f"https://api.zdxcloud.net/v1/devices/{device_id}/deeptraces/{trace_id}/events"
    mock_response = [
        {
            "timestamp": 1643525900,
            "events": [
                {
                    "category": "Zscaler",
                    "name": "tunType",
                },
                {
                    "category": "Zscaler",
                    "name": "ziaState",
                },
            ],
        },
        {
            "timestamp": 1643526200,
            "events": [
                {
                    "category": "Zscaler",
                    "name": "tunType",
                },
                {
                    "category": "Zscaler",
                    "name": "ziaState",
                },
            ],
        },
    ]
    responses.add(responses.GET, url, json=mock_response, status=200)

    result = zdx.devices.get_deeptrace_events(device_id, trace_id)

    assert isinstance(result, list)
    assert result == BoxList(mock_response)


@responses.activate
def test_get_deeptrace_top_processes(zdx):
    device_id = "123456789"
    trace_id = "987654321"
    url = f"https://api.zdxcloud.net/v1/devices/{device_id}/deeptraces/{trace_id}/top-processes"
    mock_response = {"timestamp": 0, "top_processes": [{"category": "string", "processes": [{"name": "string", "id": 0}]}]}
    responses.add(responses.GET, url, json=mock_response, status=200)

    result = zdx.devices.get_deeptrace_top_processes(device_id, trace_id)

    assert isinstance(result, Box)
    assert result == Box(mock_response)
