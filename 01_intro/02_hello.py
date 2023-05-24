from fastapi import FastAPI

app = FastAPI()


@app.get("/hello-there")  # Just a hello message...
async def hi():
    return {'message': 'Hello World!'}


@app.get("/hello-there/{name}")  # Personalized message...
async def hello(name):
    return {'message': f'Hello, {name}!'}


@app.get("/hello-there/{name}")  # add query params...
async def welcome(name, age: int = 0):
    return {'message': f'Hello, {name}, you are {age} years old!'}

# @app.get("/hello-there/")  # Do it yourself!
# async def root(name, age: ???, hobby: ???):
#     return {'message': f'Hello, {name}, you are {age} years old! You like {hobby}'}
