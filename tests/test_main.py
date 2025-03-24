from fastapi.testclient import TestClient
from task_queue.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_create_task():
    task_data = {"id": "test_task_1", "data": "test data"}
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Task added to queue"
    assert response.json()["task_id"] == task_data["id"]


def test_list_tasks():
    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert "all_tasks" in data
    assert "pending_tasks" in data
    assert "total_tasks" in data
    assert "pending_count" in data
