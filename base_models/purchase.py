from typing import List
from pydantic import BaseModel


class BasePurchase(BaseModel):
    product_id: str
    quantity: int
    price: float = None
    total: float = None
    date: str


class BasePurchases(BaseModel):
    user_id: str
    purchases: List[BasePurchase]
