from pydantic import BaseModel


class Review(BaseModel):
    comment: str
    product_name: str
    rating: int
    rater: str = None
    timestamp: str = None

