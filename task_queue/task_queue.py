import redis
import json
import time
from typing import Any


class TaskQueue:
    def __init__(self, redis_url: str):
        self.redis = redis.Redis.from_url(redis_url)

    def add_task(self, task: dict[str, Any]) -> None:
        task_id = task.get("id")
        if not self.redis.exists(task_id):
            task["status"] = "pending"
            task["created_at"] = time.time()
            self.redis.set(task_id, json.dumps(task))
            self.redis.lpush("task_queue", task_id)
            self.redis.lpush("task_history", task_id)

    def get_task(self) -> dict[str, Any]:
        task_id = self.redis.rpop("task_queue")
        if task_id:
            task_data = self.redis.get(task_id)
            if task_data:
                task = json.loads(task_data)
                task["status"] = "processing"
                task["started_at"] = time.time()
                self.redis.set(task_id, json.dumps(task))
                return task
        return None

    def mark_task_as_done(self, task_id: str) -> None:
        task_data = self.redis.get(task_id)
        if task_data:
            task = json.loads(task_data)
            task["status"] = "completed"
            task["completed_at"] = time.time()
            self.redis.set(task_id, json.dumps(task))

    def mark_task_as_failed(self, task_id: str, task: dict[str, Any]) -> None:
        task["failed_at"] = time.time()
        self.redis.set(task_id, json.dumps(task))
        self.redis.lpush("failed_tasks", task_id)

    def get_all_tasks(self) -> list[dict[str, Any]]:
        tasks = []
        task_ids = self.redis.lrange("task_history", 0, -1)
        for task_id in task_ids:
            task_data = self.redis.get(task_id)
            if task_data:
                tasks.append(json.loads(task_data))
        return tasks

    def get_pending_tasks(self) -> list[dict[str, Any]]:
        tasks = []
        task_ids = self.redis.lrange("task_queue", 0, -1)
        for task_id in task_ids:
            task_data = self.redis.get(task_id)
            if task_data:
                tasks.append(json.loads(task_data))
        return tasks

    def get_failed_tasks(self) -> list[dict[str, Any]]:
        tasks = []
        task_ids = self.redis.lrange("failed_tasks", 0, -1)
        for task_id in task_ids:
            task_data = self.redis.get(task_id)
            if task_data:
                tasks.append(json.loads(task_data))
        return tasks
