def test_get_activities_returns_activity_list(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()

    assert "Chess Club" in data
    assert data["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"
    assert "participants" in data["Chess Club"]
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_for_activity_success(client):
    response = client.post("/activities/Chess%20Club/signup?email=test.student@mergington.edu")

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["message"] == "Signed up test.student@mergington.edu for Chess Club"

    activities_response = client.get("/activities")
    assert "test.student@mergington.edu" in activities_response.json()["Chess Club"]["participants"]


def test_signup_duplicate_returns_error(client):
    duplicate_email = "michael@mergington.edu"
    response = client.post(f"/activities/Chess%20Club/signup?email={duplicate_email}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_remove_participant_success(client):
    email = "daniel@mergington.edu"
    response = client.delete(f"/activities/Chess%20Club/participants?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == "Removed daniel@mergington.edu from Chess Club"

    activities_response = client.get("/activities")
    assert email not in activities_response.json()["Chess Club"]["participants"]


def test_remove_nonexistent_participant_returns_error(client):
    email = "noone@mergington.edu"
    response = client.delete(f"/activities/Chess%20Club/participants?email={email}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"
