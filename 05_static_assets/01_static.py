from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/list")
async def listfiles():
    return {"files": [f for f in os.listdir('static/')]}
