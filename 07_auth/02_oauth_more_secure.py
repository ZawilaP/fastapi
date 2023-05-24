from typing import Annotated
from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext

users = {
    "admin": {
        "name": "admin",
        "fullname": "administrator",
        # This is obviously not a good idea...
        "password": "$2b$12$Qj8Djnx8y7KNDpKOH7xCH.9UpQq4EZY/JhVmbbHYFtfbKEtQzqiv2",
        "is_admin": True,
        "active": True
    },
    "user": {
        "name": "user",
        "fullname": "John Doe",
        "password": "$2b$12$0WC9QtfR7YtZ8LVqFIntQeQyf5oYAAuqeGp3U49KhrBvQIv9t1Vs.",
        "is_admin": True,
        "active": True
    },
    "test": {
        "name": "test",
        "fullname": "Some Guy",
        "password": "$2b$12$js2jyWhqrj8pIoLDLnqZ/uokwwBLh1aii.mhBRtjudFs3W5bnRVJa",
        "is_admin": True,
        "active": False
    }
}

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_context.hash(password)


print([get_password_hash(p)
      for p in ['topsecret', 'longpassword', 'easypass']])


def authenticate(users, username: str, password: str):
    user = get_user(users, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def make_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


class User(BaseModel):
    name: str
    fullname: str | None = None
    is_admin: bool | None = False
    active: bool | None = False


class UserInDB(User):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    name: str | None = None


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


@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate(users, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = make_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


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
