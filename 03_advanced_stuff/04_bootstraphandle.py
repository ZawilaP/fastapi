from contextlib import asynccontextmanager
import numpy as np
from fastapi import FastAPI


def _predict(x: list[np.array], z: float):
    return np.mean(x[0] @ x[1] * z)


model = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing model...")
    global model
    # Load the ML model
    model.append(np.ones(1000)*42)
    model.append(np.ones(1000)*(1/2.))
    print("Done!")
    yield  # Trick...
    # Clean up the ML models and release the resources
    print("Cleaning up...")
    model = None
    print("Done!")


app = FastAPI(lifespan=lifespan)


@app.get("/predict")
async def predict(x: float):
    result = _predict(model, x)
    return {"result": result}
