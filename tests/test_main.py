def helper_create_authenticated_user_headers(client, username="testuser", email="test@example.com", password="TestPassword123!"):
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

def test_mai(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "TaskForge API is running"
    }


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


def test_create_task(client):
    headers = helper_create_authenticated_user_headers(client)

    response = client.post(
        "/tasks",
        json={
            "title": "Test Task",
            "description": "Test Description"
        },
        headers=headers
    )

    data = response.json()

    assert response.status_code == 201
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["completed"] is False
    assert "id" in data


def test_list_tasks(client):
    headers = helper_create_authenticated_user_headers(client)

    response = client.post(
        "/tasks",
        json={
            "title": "Test Task 1",
            "description": "First Task"
        },
        headers=headers
    )

    response2 = client.post(
        "/tasks",
        json={
            "title": "Test Task 2",
            "description": "Second Task"
        },
        headers=headers
    )

    data = response.json()
    data2 = response2.json()

    response3 = client.get(
        "/tasks?sort_by=id&sort_order=asc",
        headers=headers
    )

    data3 = response3.json()

    assert response.status_code == 201
    assert response2.status_code == 201
    assert response3.status_code == 200
    assert data3 == [data, data2]


def test_get_one_task(client):
    headers = helper_create_authenticated_user_headers(client)

    response = client.post(
        "/tasks",
        json={
            "title": "Test Task",
            "description": "Test Description"
        },
        headers=headers
    )

    data = response.json()

    response2 = client.get(
        f"/tasks/{data['id']}",
        headers=headers
    )

    data2 = response2.json()

    assert response.status_code == 201
    assert response2.status_code == 200
    assert data == data2


def test_patch_task(client):
    headers = helper_create_authenticated_user_headers(client)

    response = client.post(
        "/tasks",
        json={
            "title": "Test Task",
            "description": "Test Description"
        },
        headers=headers
    )

    data = response.json()

    response2 = client.patch(
        f"/tasks/{data['id']}",
        json={
            "title": "Patched Task",
            "description": "Patched Description",
            "completed": True
        },
        headers=headers
    )

    data2 = response2.json()

    assert response.status_code == 201
    assert response2.status_code == 200
    assert data2["title"] == "Patched Task"
    assert data2["description"] == "Patched Description"
    assert data2["completed"] is True


def test_delete_task(client):
    headers = helper_create_authenticated_user_headers(client)

    response = client.post(
        "/tasks",
        json={
            "title": "Test Task",
            "description": "Test Description"
        },
        headers=headers
    )

    data = response.json()

    response2 = client.delete(
        f"/tasks/{data['id']}",
        headers=headers
    )

    data2 = response2.json()

    response3 = client.get(
        f"/tasks/{data['id']}",
        headers=headers
    )

    assert response.status_code == 201
    assert response2.status_code == 200
    assert data2 == {"message": f"Task {data['id']} deleted"}
    assert response3.status_code == 404


def test_task_authorization_between_users(client):
    headers_a = helper_create_authenticated_user_headers(
        client,
        username="user_a",
        email="a@example.com"
    )

    headers_b = helper_create_authenticated_user_headers(
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
    headers_a = helper_create_authenticated_user_headers(
        client,
        username="user_a",
        email="a@example.com"
    )

    headers_b = helper_create_authenticated_user_headers(
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
    headers_a = helper_create_authenticated_user_headers(
        client,
        username="user_a",
        email="a@example.com"
    )

    headers_b = helper_create_authenticated_user_headers(
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
    headers_a = helper_create_authenticated_user_headers(
        client,
        username="user_a",
        email="a@example.com"
    )

    headers_b = helper_create_authenticated_user_headers(
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


def test_create_task_blank_title(client):
    headers = helper_create_authenticated_user_headers(client)

    response = client.post(
        "/tasks",
        json={
            "title": "",
            "description": "Test Description",
            "project_id": None
        },
        headers=headers
    )

    assert response.status_code == 422


def test_create_task_negative_project_id(client):
    headers = helper_create_authenticated_user_headers(client)

    response = client.post(
        "/tasks",
        json={
            "title": "Test Task",
            "description": "Test Description",
            "project_id": -1
        },
        headers=headers
    )

    assert response.status_code == 422


def test_get_tasks_invalid_pagination(client):
    headers = helper_create_authenticated_user_headers(client)

    response = client.get(
        "/tasks?limit=101",
        headers=headers
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