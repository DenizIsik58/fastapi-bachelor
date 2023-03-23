import os

from pydantic import BaseModel


class Settings(BaseModel):
    authjwt_secret_key: str = os.getenv("secret")
