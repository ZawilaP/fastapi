# Create an API that will:
# - be able to accept file uploads in tasks/ directory
# - upon task end, the dir should be deleted with all of its content
# HiNT: use the python os module
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile
import shutil

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

@app.post("/upload/")
# Much better - asynchronous, has easier access to metadata, does not store files all-in-memory
async def create_upload_file(file: UploadFile):
    data = await file.read()
    with open(f'{path}/{file.filename}', 'wb') as f:
        f.write(data)
    return {"filename": file.filename, "size": len(data)}
