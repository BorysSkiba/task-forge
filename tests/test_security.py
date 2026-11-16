from app.security import create_expired_token
from tests.helpers import create_authenticated_user_headers


def test_authentication(client):
    response = client.post(
        "/users/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
    )

    registered_user = response.json()

    response2 = client.post(
        "/users/login",
        data={
            "username": "testuser",
            "password": "TestPassword123!"
        }
    )

    token = response2.json()["access_token"]

    response3 = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    data = response3.json()

    assert response.status_code == 201
    assert response2.status_code == 200
    assert response3.status_code == 200
    assert data["id"] == registered_user["id"]
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"


def test_authentication_no_token(client):
    response = client.get(
        "/users/me"
    )

    assert response.status_code == 401


def test_authentication_invalid_token(client):
    response = client.get(
        "/users/me",
        headers={"Authorization": "Bearer gibberish"}
    )

    assert response.status_code == 401


def test_task_authorization_between_users(client):
    headers_a = create_authenticated_user_headers(
        client,
        username="user_a",
        email="a@example.com"
    )

    headers_b = create_authenticated_user_headers(
        client,
        username="user_b",
        email="b@example.com"
    )

    user_a_post = client.post(
        "/tasks",
        json={
            "title": "Test Task",
            "description": "Test Description"
        },
        headers=headers_a
    )

    user_a_post_data = user_a_post.json()

    user_b_get = client.get(
        "/tasks",
        headers=headers_b
    )

    user_b_get_data = user_b_get.json()

    user_b_get_one = client.get(
        f"/tasks/{user_a_post_data['id']}",
        headers=headers_b
    )

    user_b_patch = client.patch(
        f"/tasks/{user_a_post_data['id']}",
        json={},
        headers=headers_b
    )

    user_b_delete = client.delete(
        f"/tasks/{user_a_post_data['id']}",
        headers=headers_b
    )

    user_a_get = client.get(
        f"/tasks/{user_a_post_data['id']}",
        headers=headers_a
    )

    user_a_get_data = user_a_get.json()

    assert user_a_post.status_code == 201
    assert user_b_get.status_code == 200
    assert user_b_get_data == []
    assert user_b_get_one.status_code == 404
    assert user_b_patch.status_code == 404
    assert user_b_delete.status_code == 404
    assert user_a_get.status_code == 200
    assert user_a_get_data["id"] == user_a_post_data["id"]
    assert user_a_get_data["title"] == "Test Task"
    assert user_a_get_data["description"] == "Test Description"
    assert user_a_get_data["completed"] is False


def test_project_authorization_between_users(client):
    headers_a = create_authenticated_user_headers(
        client,
        username="user_a",
        email="a@example.com"
    )

    headers_b = create_authenticated_user_headers(
        client,
        username="user_b",
        email="b@example.com"
    )

    user_a_post = client.post(
        "/projects",
        json={
            "name": "Test Project",
            "description": "Test Description"
        },
        headers=headers_a
    )

    user_a_post_data = user_a_post.json()

    user_b_get = client.get(
        "/projects",
        headers=headers_b
    )

    user_b_get_data = user_b_get.json()

    user_b_get_one = client.get(
        f"/projects/{user_a_post_data['id']}",
        headers=headers_b
    )

    user_b_patch = client.patch(
        f"/projects/{user_a_post_data['id']}",
        json={},
        headers=headers_b
    )

    user_b_delete = client.delete(
        f"/projects/{user_a_post_data['id']}",
        headers=headers_b
    )

    user_a_get = client.get(
        f"/projects/{user_a_post_data['id']}",
        headers=headers_a
    )

    user_a_get_data = user_a_get.json()

    assert user_a_post.status_code == 201
    assert user_b_get.status_code == 200
    assert user_b_get_data == []
    assert user_b_get_one.status_code == 404
    assert user_b_patch.status_code == 404
    assert user_b_delete.status_code == 404
    assert user_a_get.status_code == 200
    assert user_a_get_data["id"] == user_a_post_data["id"]
    assert user_a_get_data["name"] == "Test Project"
    assert user_a_get_data["description"] == "Test Description"


def test_creating_task_in_other_user_project(client):
    headers_a = create_authenticated_user_headers(
        client,
        username="user_a",
        email="a@example.com"
    )

    headers_b = create_authenticated_user_headers(
        client,
        username="user_b",
        email="b@example.com"
    )

    user_a_post = client.post(
        "/projects",
        json={
            "name": "Test Project",
            "description": "Test Description"
        },
        headers=headers_a
    )

    user_a_post_data = user_a_post.json()

    user_b_post = client.post(
        "/tasks",
        json={
            "title": "Test Task",
            "description": "Test Description",
            "project_id": user_a_post_data["id"],
        },
        headers=headers_b
    )

    user_b_get = client.get(
        "/tasks",
        headers=headers_b
    )

    user_b_get_data = user_b_get.json()

    assert user_a_post.status_code == 201
    assert user_b_post.status_code == 404
    assert user_b_get.status_code == 200
    assert user_b_get_data == []


def test_patching_task_to_other_user_project(client):
    headers_a = create_authenticated_user_headers(
        client,
        username="user_a",
        email="a@example.com"
    )

    headers_b = create_authenticated_user_headers(
        client,
        username="user_b",
        email="b@example.com"
    )

    user_a_post = client.post(
        "/projects",
        json={
            "name": "Test Project",
            "description": "Test Description"
        },
        headers=headers_a
    )

    user_a_post_data = user_a_post.json()

    user_b_post = client.post(
        "/tasks",
        json={
            "title": "Test Task",
            "description": "Test Description"
        },
        headers=headers_b
    )

    user_b_post_data = user_b_post.json()

    user_b_patch = client.patch(
        f"/tasks/{user_b_post_data['id']}",
        json={
            "project_id": user_a_post_data["id"],
        },
        headers=headers_b
    )

    user_b_get = client.get(
        f"/tasks/{user_b_post_data['id']}",
        headers=headers_b
    )

    user_b_get_data = user_b_get.json()

    assert user_a_post.status_code == 201
    assert user_b_post.status_code == 201
    assert user_b_patch.status_code == 404
    assert user_b_get.status_code == 200
    assert user_b_get_data["project_id"] is None


def test_tampered_jwt_token(client):
    response = client.post(
        "/users/register",
        json={
            "username": "user",
            "email": "test@example.com",
            "password": "password",
        }
    )

    response2 = client.post(
        "/users/login",
        data={
            "username": "user",
            "password": "password"
        }
    )

    token = response2.json()["access_token"]

    replacement = "a" if token[-1] != "a" else "b"
    tampered_token = token[:-1] + replacement

    response3 = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {tampered_token}"}
    )

    assert response.status_code == 201
    assert response2.status_code == 200
    assert response3.status_code == 401
    assert response3.json()["detail"] == "Could not validate credentials"


def test_expired_jwt_token(client):
    response = client.post(
        "/users/register",
        json={
            "username": "user",
            "email": "test@example.com",
            "password": "password",
        }
    )

    user_id = response.json()["id"]

    expired_token = create_expired_token(user_id)

    response2 = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {expired_token}"}
    )

    assert response.status_code == 201
    assert response2.status_code == 401


def test_sql_injection_login(client):
    response = client.post(
        "/users/login",
        data={
            "username": "' OR 1=1; --",
            "password": "anything"
        }
    )

    assert response.status_code == 401


def test_sql_injection_task_title(client):
    headers = create_authenticated_user_headers(client)

    injection_string = "' OR 1=1; --"

    response = client.post(
        "/tasks",
        json={
            "title": injection_string,
            "description": "Security test"
        },
        headers=headers
    )

    assert response.status_code == 201

    task = response.json()

    response2 = client.get(
        f"/tasks/{task['id']}",
        headers=headers
    )

    assert response2.status_code == 200
    assert response2.json()["title"] == injection_string


def test_sql_injection_sort_by(client):
    headers = create_authenticated_user_headers(client)

    response = client.get(
        "/tasks?sort_by=id%20DESC%3B%20DROP%20TABLE%20tasks%3B--",
        headers=headers
    )

    assert response.status_code == 400


def test_users_me_no_data_leakage(client):
    headers = create_authenticated_user_headers(client)

    response = client.get(
        "/users/me",
        headers=headers
    )

    assert response.status_code == 200
    assert "password" not in response.json()
    assert "hashed_password" not in response.json()


def test_enabled_docs(client):
    response = client.get(
        "/docs"
    )

    assert response.status_code == 200


def test_disabled_docs(disable_docs_client):
    response = disable_docs_client.get(
        "/docs"
    )

    response2 = disable_docs_client.get(
        "/redoc",
    )

    response3 = disable_docs_client.get(
        "/openapi.json",
    )

    assert response.status_code == 404
    assert response2.status_code == 404
    assert response3.status_code == 404


def test_valid_host(client):
    response = client.get(
        "/",
        headers={"Host": "localhost"}
    )

    assert response.status_code == 200


def test_invalid_host(client):
    response = client.get(
        "/",
        headers={"Host": "attacker.example"}
    )

    assert response.status_code == 400