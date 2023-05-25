# Create an app with two endpoints:
# 1. Upload a file and calculate its checksum in the background, then save it to a simple text file
# (format: filename:checksum, one line per file, new ones appended at the end)
# 2. Access that file and return it (format: json with nested list, eg:
# {file: [file1:hash1, file2:hash2 ... ]} )

import collections
import shutil
from contextlib import asynccontextmanager

from fastapi import FastAPI, BackgroundTasks, UploadFile
from pydantic import BaseModel, Field
import time

path = "05_exercise"


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing the directory...")
    global model
    import os
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)
    print("The new directory is created!")
    yield  # Trick...
    # Clean up the ML models and release the resources
    print("Cleaning up, deleting directory...")
    shutil.rmtree(path)
    print("Done!")


app = FastAPI(lifespan=lifespan)


results = []


async def process_task(file: UploadFile):
    time.sleep(10)
    data = await file.read()
    results.append(len(data))
    with open(f'{path}/{file.filename}', 'wb') as f:
        f.write(data)


@app.post("/task/")
async def create_task(task: UploadFile, bg: BackgroundTasks):  # Puts the task in queue
    bg.add_task(process_task, task)
    return {'message': 'Task put in queue!'}


@app.get("/task/")
async def task_results():  # Get results!
    return {'results': str(results)}
