from fastapi import FastAPI, HTTPException
import threading
import os
from typing import Any

from fastapi import FastAPI, HTTPException
from task_queue.task_queue import TaskQueue
from task_queue.worker import Worker

app = FastAPI()
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
task_queue = TaskQueue(redis_url=redis_url)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/tasks/")
async def create_task(task: dict[str, Any]):
    try:
        task_queue.add_task(task)
        return {"message": "Task added to queue", "task_id": task.get("id")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tasks/")
async def list_tasks():
    try:
        all_tasks = task_queue.get_all_tasks()
        pending_tasks = task_queue.get_pending_tasks()
        return {
            "message": "List of all tasks",
            "all_tasks": all_tasks,
            "pending_tasks": pending_tasks,
            "total_tasks": len(all_tasks),
            "pending_count": len(pending_tasks)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    worker = Worker(task_queue)
    threading.Thread(target=worker.run, daemon=True).start()
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
