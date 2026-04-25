from urllib.parse import quote


def test_unregister_success_removes_participant(client):
    activity_name = "Basketball Team"
    email = "alex@mergington.edu"

    response = client.delete(
        f"/activities/{quote(activity_name)}/participants",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"

    activities_response = client.get("/activities")
    assert email not in activities_response.json()[activity_name]["participants"]


def test_unregister_returns_404_for_unknown_activity(client):
    email = "alex@mergington.edu"

    response = client.delete(
        f"/activities/{quote('Unknown Club')}/participants",
        params={"email": email},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_404_for_non_participant(client):
    activity_name = "Basketball Team"
    email = "notenrolled@mergington.edu"

    response = client.delete(
        f"/activities/{quote(activity_name)}/participants",
        params={"email": email},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not signed up for this activity"
