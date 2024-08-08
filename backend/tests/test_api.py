def test_successful_get_profile(client):
    response = client.get("/api/SteamProfileService/v1/GetRandomProfile")
    assert response.status_code == 200


def test_failed_post_profile(client):
    request = {"steamid": "76561199550021925"}

    response = client.post("/api/SteamProfileService/v1/PostSteamID", json=request)

    assert response.status_code == 400
    assert b'{"error":"Profile has already been added."}\n' in response.data

