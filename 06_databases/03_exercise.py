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


async def process_image(filename: str, database, _id) -> str:
    start = time.time()
    pil_img = Image.open(filename)
    # pil_img.resize((64, 64))
    time.sleep(randint(0, 1))
    pil_img.save(f'{filename.replace("files/", "processed/")}')
    end = time.time()
    print(end-start)
    query = tasks.update().where(tasks.c.id == _id).values(
        status=True, duration=end-start)
    await database.execute(query)


app = FastAPI()


DATABASE_URL = "sqlite:///./fileprocessor.db"


database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

tasks = sqlalchemy.Table(
    "tasks",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("filename", sqlalchemy.String),
    sqlalchemy.Column("status", sqlalchemy.Boolean),
    sqlalchemy.Column("duration", sqlalchemy.Float),
)


engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


class TaskAdd(BaseModel):
    filename: str
    status: bool


class Task(BaseModel):
    id: int
    filename: str
    status: bool
    duration: float | None


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/tasks/", response_model=List[Task])
async def get_tasks():
    query = tasks.select()
    return await database.fetch_all(query)


@app.get("/tasks/done", response_model=List[Task])
async def get_tasks():
    query = tasks.select().where(tasks.c.status == True)
    return await database.fetch_all(query)


@app.post("/tasks/new")
async def process_file(file: UploadFile, bg: BackgroundTasks):
    data = await file.read()
    with open(f'files/{file.filename}', 'wb') as f:
        f.write(data)
        query = tasks.insert().values(filename=file.filename, status=False)
        last_record_id = await database.execute(query)
        bg.add_task(
            process_image, f'files/{file.filename}', database, last_record_id)

    return {"filename": file.filename, "processing": len(data)}
