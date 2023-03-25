import os

from dotenv import dotenv_values
from pydantic import BaseModel


class Settings(BaseModel):
    authjwt_secret_key: str = "ewkjn34lrgjeklrj23lk4jnr"
