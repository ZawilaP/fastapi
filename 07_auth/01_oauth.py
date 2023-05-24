from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel


users = {
    "admin": {
        "name": "admin",
        "fullname": "administrator",
        "password": "topsecret",  # This is obviously not a good idea...
        "is_admin": True,
        "active": True
    },
    "user": {
        "name": "user",
        "fullname": "John Doe",
        "password": "longpassword",
        "is_admin": True,
        "active": True
    },
    "test": {
        "name": "test",
        "fullname": "Some Guy",
        "password": "easypass",
        "is_admin": True,
        "active": False
    }
}

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    name: str
    fullname: str | None = None
    is_admin: bool | None = False
    active: bool | None = False


class UserInDB(User):
    password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        print(user_dict)
        return UserInDB(**user_dict)


def user_by_token(token):
    return get_user(users, token)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = user_by_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if not current_user.active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = users.get(form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = get_user(users, form_data.username).password
    print(hashed_password, user.password)
    if not hashed_password == user.password:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    return {"access_token": user.name, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user


@app.get("/logout")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return {'message': 'logout success'}  # Can't do anything...
