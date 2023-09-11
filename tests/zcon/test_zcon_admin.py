import json

import responses


@responses.activate
def test_add_role(zcon):
    # Mock the endpoint that `add_role` would hit
    responses.add(responses.POST, url="https://connector.zscaler.net/api/v1/adminRoles", json={}, status=200)

    # Call the function with minimum arguments
    resp_min_args = zcon.admin.add_role(name="NewRole")
    assert isinstance(resp_min_args, dict)

    # Verify request payload for minimum arguments
    request_payload_min = json.loads(responses.calls[0].request.body.decode("utf-8"))
    assert request_payload_min["name"] == "NewRole"

    # Reset responses.calls
    responses.reset()

    # Call the function with additional arguments
    resp_with_args = zcon.admin.add_role(
        name="AdvancedRole",
        policy_access="READ_ONLY",
        feature_permissions_tuples=[("APIKEY_MANAGEMENT", "READ_ONLY"), ("EDGE_CONNECTOR_CLOUD_PROVISIONING", "NONE")],
        alerting_access="READ_WRITE",
    )
    assert isinstance(resp_with_args, dict)

    # Verify request payload for additional arguments
    request_payload_args = json.loads(responses.calls[0].request.body.decode("utf-8"))
    assert request_payload_args["name"] == "AdvancedRole"
    assert request_payload_args["policy_access"] == "READ_ONLY"
    assert "feature_permissions" in request_payload_args
    assert request_payload_args["feature_permissions"]["APIKEY_MANAGEMENT"] == "READ_ONLY"
    assert request_payload_args["feature_permissions"]["EDGE_CONNECTOR_CLOUD_PROVISIONING"] == "NONE"
    assert request_payload_args["alerting_access"] == "READ_WRITE"
