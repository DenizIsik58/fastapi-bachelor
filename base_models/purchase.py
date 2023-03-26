from typing import List
from pydantic import BaseModel


class BasePurchaseItem(BaseModel):
    product_id: str
    quantity: int


class BasePurchase(BaseModel):
    user_id: str = None
    purchase_date: str = None
    items: List[BasePurchaseItem]
