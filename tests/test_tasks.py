from tests.helpers import create_authenticated_user_headers


def test_create_task(client):
    headers = create_authenticated_user_headers(client)

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
    headers = create_authenticated_user_headers(client)

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
    headers = create_authenticated_user_headers(client)

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
    headers = create_authenticated_user_headers(client)

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
    headers = create_authenticated_user_headers(client)

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


def test_create_task_blank_title(client):
    headers = create_authenticated_user_headers(client)

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
    headers = create_authenticated_user_headers(client)

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
    headers = create_authenticated_user_headers(client)

    response = client.get(
        "/tasks?limit=101",
        headers=headers
    )

    assert response.status_code == 422


def test_get_task_nonexistent_large_id(client):
    headers = create_authenticated_user_headers(client)

    response = client.get(
        "/tasks/999999999",
        headers=headers
    )

    assert response.status_code == 404


def test_get_task_negative_id(client):
    headers = create_authenticated_user_headers(client)

    response = client.get(
        "/tasks/-1",
        headers=headers
    )

    assert response.status_code == 404


def test_get_task_id_is_not_a_number(client):
    headers = create_authenticated_user_headers(client)

    response = client.get(
        "/tasks/not-a-number",
        headers=headers
    )

    assert response.status_code == 422
