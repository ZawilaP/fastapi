# Create an API that will
# - keep a list of people (each person has a unique name and some metadata)
# - add a new person to the set
# - remove a person from the set
# - set metadata to a specified value
# - count unique people
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Person(BaseModel):
    first_name: str
    surname: str
    age: int = Field(
        gt=0, le=100, description='Age of the person')
    hobby: str


people = {}


@app.put('/people/')
async def add_person(person: Person):
    people[person.first_name + person.surname] = person
    return {'message': 'added person'}


@app.delete('/people/')
async def delete_person(person: Person):
    if (person.first_name + person.surname) in people:
        del people[person.first_name + person.surname]
        return {'message': f'deleted {person}'}
    else:
        return {'message': 'person doesn\'t exist in the dataset'}


@app.get('/people')
async def count_people():
    return {'message': f'there are {len(people)} people in the dataset'}
