from fastapi import FastAPI, Query, Path
from typing import Annotated

app = FastAPI()
data = [f"item{i}" for i in range(100)]


@app.get("/v1/items/{key}")
async def get(key: int):  # key is string or None
    if key:
        return data[key]
    else:
        return data


@app.get("/v2/items/{key}")
# key is string or None
async def get(key: Annotated[int | None, Path(ge=0, lt=len(data)-1)]):
    if key:
        return data[key]
    else:
        return data
dictdata = {'someguy': {'meta1': 'value 1', 'meta2': 'value2'},
            'otherguy': {'meta1': 'other value 1', 'meta2': 'other value 2'}}


# Requirement: Name (query argument) can be between 3 and 25 chars. Use Query class with min_length and max_length arguments
@app.get("/v2/people")
async def count(name: int = 0):
    return {f'error': 'not implemented'}


# For those who are bored. Use regex validation, allow only latin alphanumeric chars so that !@#$%^ doesn't pass validation
@app.get("/v2/people2/")
async def count(_id: int = 0):
    return {f'error': 'not implemented'}
