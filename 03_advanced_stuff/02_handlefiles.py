from typing import Annotated
import os
from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.get("/files/")
async def files():
    return {"file list": [f for f in os.listdir('files/')]}


@app.post("/files/")
# Good for small files
async def create_upload_file(file: Annotated[bytes, File()]):
    with open('files/uploaded', 'wb') as f:
        f.write(file)
    return {"filesize": len(file)}


@app.post("/bigfiles/")
# Much better - asynchronous, has easier access to metadata, does not store files all-in-memory
async def create_upload_file(file: UploadFile):
    data = await file.read()
    with open(f'files/{file.filename}', 'wb') as f:
        f.write(data)
    return {"filename": file.filename, "size": len(data)}
