from pydantic import BaseModel


class Review(BaseModel):
    review: str
    product_name: str
    rating: int
    rater: str
    timestamp: str

