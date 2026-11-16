def create_authenticated_user_headers(client, username="testuser", email="test@example.com", password="TestPassword123!"):
    client.post(
        "/users/register",
        json={
            "username": username,
            "email": email,
            "password": password
        }
    )

    response2 = client.post(
        "/users/login",
        data={
            "username": username,
            "password": password
        }
    )

    token = response2.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}