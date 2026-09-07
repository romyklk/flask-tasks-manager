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
