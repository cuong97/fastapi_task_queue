import time
from typing import Any
from task_queue.task_queue import TaskQueue
import redis


class Worker:
    def __init__(self, task_queue: TaskQueue):
        self.task_queue = task_queue
        self.running = True
        self.retry_interval = 1
        self.max_retries = 3

    def check_redis_connection(self) -> bool:
        try:
            self.task_queue.redis.ping()
            return True
        except (redis.ConnectionError, redis.TimeoutError):
            print("Lost connection to Redis. Retrying...")
            return False

    def run(self):
        while self.running:
            current_task = None
            try:
                if not self.check_redis_connection():
                    time.sleep(self.retry_interval)
                    continue

                current_task = self.task_queue.get_task()
                if current_task:
                    self.process_task(current_task)
                else:
                    time.sleep(0.5)
            except Exception as e:
                print(f"Error in worker: {e}")
                if current_task:
                    self.handle_failed_task(current_task, str(e))
                time.sleep(self.retry_interval)

    def handle_failed_task(self, task: dict[str, Any], error_message: str) -> None:
        task_id = task.get("id")
        retry_count = task.get("retry_count", 0)

        if retry_count < self.max_retries:
            task["retry_count"] = retry_count + 1
            task["last_error"] = error_message
            task["last_retry_time"] = time.time()
            print(f"Retrying task {task_id} (attempt {retry_count + 1}/{self.max_retries})")
            self.task_queue.add_task(task)
        else:
            print(f"Task {task_id} failed permanently after {self.max_retries} retries")
            task["status"] = "failed"
            task["final_error"] = error_message
            self.task_queue.mark_task_as_failed(task_id, task)

    def process_task(self, task: dict[str, Any]) -> None:
        task_id = task.get("id")
        try:
            print(f"Processing task: {task}")
            self.task_queue.mark_task_as_done(task_id)
            print(f"Task {task_id} completed.")
        except Exception as e:
            print(f"Task {task_id} failed: {e}")
            self.handle_failed_task(task, str(e))
