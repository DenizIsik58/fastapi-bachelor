from typing import List
from pydantic import BaseModel
from base_models.review import Review


class BaseProduct(BaseModel):
    name: str
    description: str
    price: float
    reviews: List[Review] = []
