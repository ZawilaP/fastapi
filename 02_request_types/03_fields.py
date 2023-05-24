from typing import Annotated
import collections
from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Task(BaseModel):
    name: str
    description: str | None = None  # Allow empty, map it to None type
    duration: float = Field(
        gt=0, le=120, description="Duration of the task in seconds. [0-120]")


todo = collections.deque()


@app.post("/task/dummy")
async def create_task(task: Task):  # Does not do anything
    return task


@app.post("/task/")
async def create_task(task: Task):  # Puts the task in queue
    todo.appendleft(task)
    return {'message': 'ok'}


@app.get("/task/")
async def get_task(task: Task):  # Consume the task from the queue
    if len(todo) != 0:
        return {'task': todo.pop()}
    else:
        return {'task': 'None'}


# TODO!
@app.get("/task/count")
async def task_count(task: Task):  # Get number of tasks!
    return {'error': 'unimplemented'}
