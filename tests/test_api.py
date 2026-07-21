import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture
def client():
    with TestClient(app_module.app) as test_client:
        yield test_client


def test_get_activities_returns_data(client):
    # Arrange
    # No setup needed for this request.

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "teststudent@example.com"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]

    # Cleanup
    client.delete(f"/activities/{activity_name}/unregister?email={email}")


def test_signup_rejects_duplicate_registration(client):
    # Arrange
    activity_name = "Chess Club"
    email = "duplicate@example.com"

    # Act
    first_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    second_response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student already signed up for this activity"

    # Cleanup
    client.delete(f"/activities/{activity_name}/unregister?email={email}")
