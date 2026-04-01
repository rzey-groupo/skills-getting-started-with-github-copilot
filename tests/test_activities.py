def test_get_activities_returns_activity_map(client):
    response = client.get("/activities")

    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"

    payload = response.json()
    assert isinstance(payload, dict)
    assert "Chess Club" in payload
    assert "Science Club" in payload

    chess = payload["Chess Club"]
    assert chess["description"]
    assert chess["schedule"]
    assert isinstance(chess["max_participants"], int)
    assert isinstance(chess["participants"], list)
