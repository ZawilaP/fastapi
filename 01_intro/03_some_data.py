from fastapi import FastAPI

app = FastAPI()
data = [f"item{i}" for i in range(100)]


@app.get("/v1/get-item")  # add query params...
async def get(_id: int = 0):
    return {f'{_id}': data[_id]}


@app.get("/v2/get-item")  # add ugly&simple validation...
async def get(_id: int = 0):
    if _id < 0 or _id >= len(data):
        return {f'message': 'not found'}
    return {f'{_id}': data[_id]}

# TODO!


@app.get("/v2/get-item/all")
async def count(_id: int = 0):
    return {f'error': 'not implemented'}
