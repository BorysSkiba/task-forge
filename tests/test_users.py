def test_register_user(client):
    response = client.post(
        "/users/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "hashed_password" not in data
    assert "password" not in data


def test_register_duplicate_user(client):
    response = client.post(
        "/users/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
    )

    response2 = client.post(
        "/users/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
    )

    assert response.status_code == 201
    assert response2.status_code == 409


def test_login_user(client):
    response = client.post(
        "/users/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
    )

    response2 = client.post(
        "/users/login",
        data={
            "username": "testuser",
            "password": "TestPassword123!"
        }
    )

    data = response2.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert response.status_code == 201
    assert response2.status_code == 200


def test_login_user_wrong_password(client):
    response = client.post(
        "/users/login",
        data={
            "username": "testuser",
            "password": "WrongPassword123!"
        }
    )

    assert response.status_code == 401


def test_login_user_unknown_username(client):
    response = client.post(
        "/users/login",
        data={
            "username": "nonexistent",
            "password": "WrongPassword123!"
        }
    )

    assert response.status_code == 401


def test_create_user_invalid_email(client):
    response = client.post(
        "/users/register",
        json={
            "username": "user_a",
            "email": "not-a-valid-email",
            "password": "password"
        }
    )

    assert response.status_code == 422


def test_create_user_blank_username(client):
    response = client.post(
        "/users/register",
        json={
            "username": "     ",
            "email": "test@example.com",
            "password": "password"
        }
    )

    assert response.status_code == 422


def test_create_user_unexpected_field(client):
    response = client.post(
        "/users/register",
        json={
            "username": "user_a",
            "email": "test@example.com",
            "password": "password",
            "user_id": 100
        }
    )

    assert response.status_code == 422
