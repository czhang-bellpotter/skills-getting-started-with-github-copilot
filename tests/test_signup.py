from urllib.parse import quote


def test_signup_success_adds_participant(client):
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    response = client.post(
        f"/activities/{quote(activity_name)}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    activities_response = client.get("/activities")
    assert email in activities_response.json()[activity_name]["participants"]


def test_signup_returns_404_for_unknown_activity(client):
    email = "newstudent@mergington.edu"

    response = client.post(
        f"/activities/{quote('Unknown Club')}/signup",
        params={"email": email},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_returns_400_for_duplicate_participant(client):
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    response = client.post(
        f"/activities/{quote(activity_name)}/signup",
        params={"email": existing_email},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
