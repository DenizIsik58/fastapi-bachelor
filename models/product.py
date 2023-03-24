from typing import List

from pydantic import BaseModel

from models.review import Review


class Product(BaseModel):
    name: str
    description: str
    price: int
    reviews: List[Review] = []
