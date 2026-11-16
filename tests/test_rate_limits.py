from tests.helpers import create_authenticated_user_headers


def test_registration_rate_limit(client, enable_rate_limiting):
    for i in range(4):
        response = client.post(
            "/users/register",
            json={
                "username": f"user{i}",
                "email": f"test{i}@example.com",
                "password": "password",
            }
        )

        if i == 3:
            assert response.status_code == 429
        else:
            assert response.status_code == 201


def test_login_rate_limit(client, enable_rate_limiting):
    create_authenticated_user_headers(client)

    for i in range(5):
        response = client.post(
            "/users/login",
            data={
                "username": "testuser",
                "password": "randompassword"
            }
        )

        if i == 4:
            assert response.status_code == 429
        else:
            assert response.status_code == 401


def test_default_rate_limit(client, enable_rate_limiting):
    headers = create_authenticated_user_headers(client)

    for i in range(101):
        response = client.get(
            "/tasks",
            headers=headers
        )

        if i == 100:
            assert response.status_code == 429
        else:
            assert response.status_code == 200
