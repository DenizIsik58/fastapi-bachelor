from typing import List
from pydantic import BaseModel


class BasePurchaseItem(BaseModel):
    product_id: str
    quantity: int


class BasePurchase(BaseModel):
    items: List[BasePurchaseItem]
