from fastapi import FastAPI
from pydantic import BaseModel
import collections


class Task(BaseModel):
    name: str
    description: str | None = None  # Allow empty, map it to None type
    duration: float


app = FastAPI()
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

# Now something more difficult.
# Create a BaseModel child class that will represent a patient waiting for a visit.
# Each patient has a first name, last name and age
# Create a queue of patients (eg. collections.deque)
# We need endpoints to:
# - add more patients to the queue (details are sent in the body)
# - "treat" patients (take them out of queue)
# - get current patient queue length
# - (*) Extra credit! for ensuring that the queue is never longer than 20
class Patient(BaseModel):
    pass

# ???
