from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str
    salt: str
    hashed_pwd: str

class UserIn(BaseModel):
    email:str
    password: str


class UserInDB(User):
    hashed_password: str
