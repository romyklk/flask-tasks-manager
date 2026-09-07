from app.app import create_app


def make_client():
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


def test_list_tasks_starts_empty():
    client = make_client()

    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.get_json() == []


def test_create_task_returns_it_with_an_id():
    client = make_client()

    response = client.post("/tasks", json={"title": "Acheter du pain"})

    assert response.status_code == 201
    body = response.get_json()
    assert body["title"] == "Acheter du pain"
    assert "id" in body


def test_created_task_appears_in_the_list():
    client = make_client()

    client.post("/tasks", json={"title": "Acheter du pain"})
    response = client.get("/tasks")

    titles = [task["title"] for task in response.get_json()]
    assert titles == ["Acheter du pain"]


def test_home_page_shows_created_tasks():
    client = make_client()
    client.post("/tasks", json={"title": "Acheter du pain"})

    response = client.get("/")

    assert response.status_code == 200
    assert b"Acheter du pain" in response.data


def test_delete_task_removes_it():
    client = make_client()
    created = client.post("/tasks", json={"title": "Acheter du pain"}).get_json()

    response = client.delete(f"/tasks/{created['id']}")

    assert response.status_code == 204
    assert client.get("/tasks").get_json() == []


def test_delete_missing_task_returns_404():
    client = make_client()

    response = client.delete("/tasks/999")

    assert response.status_code == 404


def test_update_task_can_mark_it_done():
    client = make_client()
    created = client.post("/tasks", json={"title": "Acheter du pain"}).get_json()

    response = client.patch(f"/tasks/{created['id']}", json={"done": True})

    assert response.status_code == 200
    assert response.get_json()["done"] is True
    assert client.get("/tasks").get_json()[0]["done"] is True


def test_update_missing_task_returns_404():
    client = make_client()

    response = client.patch("/tasks/999", json={"done": True})

    assert response.status_code == 404


def test_web_form_adds_a_task_and_redirects_home():
    client = make_client()

    response = client.post("/web/tasks", data={"title": "Acheter du pain"})

    assert response.status_code == 302
    assert b"Acheter du pain" in client.get("/").data


def test_web_form_deletes_a_task_and_redirects_home():
    client = make_client()
    created = client.post("/tasks", json={"title": "Acheter du pain"}).get_json()

    response = client.post(f"/web/tasks/{created['id']}/delete")

    assert response.status_code == 302
    assert client.get("/tasks").get_json() == []


def test_web_form_toggles_a_task_and_redirects_home():
    client = make_client()
    created = client.post("/tasks", json={"title": "Acheter du pain"}).get_json()

    response = client.post(f"/web/tasks/{created['id']}/toggle")

    assert response.status_code == 302
    assert client.get("/tasks").get_json()[0]["done"] is True
