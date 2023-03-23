"""from datetime import timedelta, datetime

import jwt
from fastapi import Depends, HTTPException
from passlib.context import CryptContext
from starlette import status

from database.mongo import get_collection
from models.token import TokenData
from models.user import UserInDB
from routers.register import oauth2_scheme

SECRET_KEY = "b5111f00721e7b9efd79243655fd64ab8fceafee69a5829e18e4b1d6355d9f2c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)



def create_access_token(data: dict, expires_delta: timedelta | None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

"""
import os
from datetime import datetime

import bcrypt
import dotenv
import jwt
from fastapi import Depends, HTTPException
from pydantic.datetime_parse import timedelta
from starlette import status
from database.mongo import get_collection
from models.token import TokenData
from routers.register import oauth2_scheme


def get_user(username: str):
    user = get_collection("users").find_one({"username": username})
    print(user)
    if user is None:
        return None
    return user

def authenticate_and_verify_passwords(username, password):
    user = get_user(username)
    if user is None:
        return False

    return bcrypt.checkpw(password.encode("utf-8"),
                          bcrypt.hashpw(password.encode("utf-8"), user["salt"].encode("utf-8")))


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
