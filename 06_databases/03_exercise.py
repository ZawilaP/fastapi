# Create an API that will
# - Grab a task to do:
# -- Accept an image file from the user and save it to disk
# -- Process the task (processing function is implemented)
# -- Measure the time of the processing
# -- upload the status to a database and save the processed file on disk
# - List all tasks
# - List done tasks
# - Access specific done task

from pydantic import BaseModel
import sqlalchemy
import databases
from typing import List, Annotated
from fastapi import FastAPI, Form, HTTPException, UploadFile, BackgroundTasks
from PIL import Image
import time
from random import randint
import io

# This is done, no need to edit


async def process_image(filename: str, database, _id) -> str:
    start = time.time()
    pil_img = Image.open(filename)
    # pil_img.resize((64, 64))
    time.sleep(randint(0, 1))
    pil_img.save(f'{filename.replace("files/", "processed/")}')
    end = time.time()
    query = tasks.update().where(tasks.c.id == _id).values(
        status=True, duration=end-start)
    await database.execute(query)


app = FastAPI()


DATABASE_URL = "sqlite:///./fileprocessor.db"


database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

tasks = sqlalchemy.Table(
    ...
)


engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


class TaskAdd(BaseModel):
    ...


class Task(BaseModel):
    ...


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/tasks/", response_model=List[Task])
async def get_tasks():
    pass


@app.get("/tasks/done", response_model=List[Task])
async def get_tasks_done():
    pass


@app.post("/tasks/new")
async def process_file(file: UploadFile, bg: BackgroundTasks):
    pass
