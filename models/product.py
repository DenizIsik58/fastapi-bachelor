from pydantic import BaseModel, Field
from models.pyobject import PyObjectId


class Product(BaseModel):
    name: str
    description: str
    price: float
