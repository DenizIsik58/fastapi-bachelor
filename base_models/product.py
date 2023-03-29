from pydantic import BaseModel


class BaseProduct(BaseModel):
    name: str
    long_description: str
    short_description: str
    price: float
    image_url: str
