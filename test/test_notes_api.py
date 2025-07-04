import requests
import uuid

ENDPOINT = "http://127.0.0.1:8000"


def test_call_endpoint_positive():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200


def test_post_note_positive():
    payload = new_note_payload()
    create_response = post_note(payload)
    assert create_response.status_code == 200

    create_data = create_response.json()
    note_id = create_data["id"]

    get_response = get_note_by_id(note_id)
    assert get_response.status_code == 200

    get_data = get_response.json()

    assert get_data["title"] == payload["title"]
    assert get_data["content"] == payload["content"]

    assert delete_note_by_id(note_id).status_code == 200


def test_delete_note_positive():
    payload = new_note_payload()
    create_response = post_note(payload)

    assert create_response.status_code == 200
    note_id = create_response.json()["id"]

    delete_response = delete_note_by_id(note_id)
    assert delete_response.status_code == 200
    assert not get_note_by_id(note_id)
    # Check to understand return if ID doesnt exist


def test_get_all_notes_positive():
    payload = new_note_payload()
    create_response = requests.post(ENDPOINT + "/notes", json=payload)
    assert create_response.status_code == 200

    response = requests.get(ENDPOINT + "/notes")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

    assert delete_note_by_id(create_response.json()["id"]).status_code == 200


def test_put_note_by_id_positive():
    payload = new_note_payload()
    create_response = post_note(payload)

    assert create_response.status_code == 200
    note_id = create_response.json()["id"]

    new_payload = {"title": "new mock title", "content": "Here is the new mock data"}

    update_response = update_note_by_id(note_id, new_payload)
    assert update_response.status_code == 200

    get_response = get_note_by_id(note_id)
    assert get_response.status_code == 200
    update_data = get_response.json()

    assert update_data["title"] == new_payload["title"]
    assert update_data["content"] == new_payload["content"]

    assert delete_note_by_id(note_id).status_code == 200


def test_get_search_results():
    payload = new_note_payload()
    ids = []
    for _ in range(6):
        response = post_note(payload)
        assert response.status_code == 200
        ids.append(response.json()["id"])

    query = "tests and mocks and mocking and tests"

    search_response = search_notes(query)
    assert search_response.status_code == 200
    assert len(search_response.json()) == 5

    for id in ids:
        assert delete_note_by_id(id).status_code == 200


def post_note(payload):
    return requests.post(ENDPOINT + "/notes", json=payload)


def get_note_by_id(id):
    return requests.get(ENDPOINT + f"/notes/{id}")


def update_note_by_id(id, payload):
    return requests.put(ENDPOINT + f"/notes/{id}", json=payload)


def search_notes(query):
    params = {"q": query}
    return requests.get(ENDPOINT + "/search", params=params)


def delete_note_by_id(id):
    return requests.delete(ENDPOINT + f"/notes/{id}")


def new_note_payload():
    title = f"title_{uuid.uuid4().hex}"
    content = f"content_{uuid.uuid4().hex}"
    return {"title": title, "content": content}
