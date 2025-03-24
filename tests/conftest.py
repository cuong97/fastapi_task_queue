import pytest
import os
from task_queue.task_queue import TaskQueue
from task_queue.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def test_client():
    return TestClient(app)


@pytest.fixture
def task_queue():
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    return TaskQueue(redis_url=redis_url)
