from fastapi import FastAPI

app = FastAPI()


@app.get("/hello-there")  # Just a hello message...
async def root():
    return {'message': 'Hello World!'}
