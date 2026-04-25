def test_get_activities_returns_expected_structure(client):
    response = client.get("/activities")

    assert response.status_code == 200

    payload = response.json()
    assert isinstance(payload, dict)
    assert payload

    expected_keys = {"description", "schedule", "max_participants", "participants"}
    for details in payload.values():
        assert expected_keys.issubset(details.keys())
        assert isinstance(details["participants"], list)
