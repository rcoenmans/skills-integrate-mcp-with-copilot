import pytest
from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_list_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    # At least one seeded activity
    assert any(a.get("name") == "Chess Club" for a in data)


def test_signup_and_unregister():
    email = "teststudent@mergington.edu"
    # ensure activity exists
    res = client.post("/activities/Chess Club/signup", params={"email": email})
    assert res.status_code == 200
    assert "Signed up" in res.json().get("message", "")

    # double signup -> 400
    res = client.post("/activities/Chess Club/signup", params={"email": email})
    assert res.status_code == 400

    # unregister
    res = client.delete("/activities/Chess Club/unregister", params={"email": email})
    assert res.status_code == 200
