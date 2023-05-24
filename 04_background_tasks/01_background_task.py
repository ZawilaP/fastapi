from typing import Annotated
import collections
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel, Field
import time
app = FastAPI()


class Task(BaseModel):
    name: str | None = "Default Task"
    description: str | None = None  # Allow empty, map it to None type
    duration: float = Field(
        gt=0, le=120, description="Duration of the task in seconds. [0-120]")
    result: int | None = None


results = collections.deque()


def process_task(task: Task):
    time.sleep(int(task.duration))
    task.result = 1
    results.appendleft(task)


@app.post("/task/")
async def create_task(task: Task, bg: BackgroundTasks):  # Puts the task in queue
    bg.add_task(process_task, task)
    return {'message': 'Task put in queue!'}


@app.post("/task/many")
# Puts multiple tasks in queue
async def create_task(task: list[Task], bg: BackgroundTasks):
    for t in task:
        bg.add_task(process_task, t)
    return {'message': 'Task put in queue!'}


@app.get("/task/")
async def task_results():  # Get results!
    return {'results': [(t.name, t.result) for t in results]}
