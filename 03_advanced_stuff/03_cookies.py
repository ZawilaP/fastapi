from typing import Annotated
from fastapi import Cookie, FastAPI, Response

app = FastAPI()


@app.get("/cookie/")
async def read_items(response: Response, counter: Annotated[int | None, Cookie()] = 0, name: Annotated[str | None, Cookie()] = "unknown"):
    if name != "unknown":
        response.set_cookie(key="counter", value=counter+1)
    return {"name": name, "visit count": counter}


@app.get("/firstvisit/")
async def read_items(response: Response, name: str | None = None):
    if name is not None:
        response.set_cookie(key="name", value=name)
        return {"message": "ok"}
    return {"message": "not set!"}
