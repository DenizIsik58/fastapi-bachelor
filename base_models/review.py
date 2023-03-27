from pydantic import BaseModel


class Review(BaseModel):
    comment: str
    product_id: str
    rating: int

