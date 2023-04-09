from pydantic import BaseModel


class BaseLogin(BaseModel):
    username: str
    password: str