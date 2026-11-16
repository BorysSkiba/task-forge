from tests.helpers import create_authenticated_user_headers


def test_get_project_negative_id(client):
    headers = create_authenticated_user_headers(client)

    response = client.get(
        "/projects/-1",
        headers=headers
    )

    assert response.status_code == 404


def test_get_project_id_is_not_a_number(client):
    headers = create_authenticated_user_headers(client)

    response = client.get(
        "/projects/not-a-number",
        headers=headers
    )

    assert response.status_code == 422