from typing import Annotated

from fastapi import FastAPI, Form, HTTPException

app = FastAPI()


@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    print(username, password)
    if username == "foo" and password == "bar":  # This is absolutely not secure ;)
        return {"message": "hello!"}
    else:
        return {"message": "Unknown username!"}
        raise HTTPException(status_code=403, detail="Nope, unauthorized")
