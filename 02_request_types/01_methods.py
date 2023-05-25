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


@app.get("/assets")
async def get():
    return {'message': assets}


@app.get('/assets/{state}')
async def get(state: str):
    def my_filtering_function(pair):
        key, value = pair
        if value == state:
            return True  # filter pair out of the dictionary
        else:
            return False  # keep pair in the filtered dictionary

    return {'message': dict(filter(my_filtering_function, assets.items()))}


@app.put('/assets/{state_name}/{state_value}')
async def get(state_name: str, state_value: str):
    assets[state_name] = state_value
    return {'message': f'added element {state_name}: {state_value}'}
