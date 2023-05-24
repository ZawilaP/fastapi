from typing import List

import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel


DATABASE_URL = "sqlite:///./test.db"


database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

tasks = sqlalchemy.Table(
    "tasks",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("status", sqlalchemy.Boolean),
    sqlalchemy.Column("duration", sqlalchemy.Float),
)


engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


class TaskAdd(BaseModel):
    description: str
    status: bool


class Task(BaseModel):
    id: int
    description: str
    status: bool


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


@app.post("/tasks/", response_model=TaskAdd)
async def create_note(task: TaskAdd):
    query = tasks.insert().values(description=task.description, status=task.status)
    last_record_id = await database.execute(query)
    return {**task.dict(), "id": last_record_id}
