from fastapi import FastAPI


app = FastAPI()
elements = [1, 2, 3, 4, 5, 6]


@app.get("/data/")
async def get():  # Get list
    return {'message': elements}


@app.post("/data/{value}")
async def post(value: int):  # Add value to list
    elements.append(value)
    return {'message': elements}


@app.put("/data/{value}")
async def put(value: int):  # Add value to list
    if value not in elements:
        elements.append(value)
    return {'message': elements}


@app.delete("/data/{value}")
async def delete(value: int):  # Add value to list
    if value in elements:
        elements.remove(value)
    return {'message': elements}
# Todo!
assets = {'asset1': 'up', 'asset2': 'up', 'asset3': 'down', 'asset4': 'up', 'asset5': 'down'}
# Create an API that allows:
# - listing all assets
# - listing assets in any state
# - changing single asset's state