import json

from fastapi import APIRouter, Body, HTTPException
from starlette import status
from starlette.responses import JSONResponse
from database_schemas.product import ProductDocument
from base_models.product import BaseProduct


products_router = APIRouter()


# TODO: Do we need protection?
@products_router.post("/add")
async def add_product(product: BaseProduct = Body(...)):

    if ProductDocument.objects(name=product.name).count() > 0:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This bag already exists!")

    new_product = ProductDocument(name=product.name, price=product.price, description=product.description, reviews=[]).save()
    created_product = ProductDocument.objects(id=new_product.id).to_json()

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_product)


# TODO: protet this endpoint
@products_router.get("/")
async def get_all_products():
    # Return all products from the database
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=(ProductDocument.objects().to_json()))

# TODO: Should we remove products?
"""
@products_router.delete("/products/remove/{id}")
async def remove_product():
    # Remove a products from the database
    database.delete_from_collection("products", id)
    raise HTTPException(status_code=400, detail="Not implemented yet!")
"""
