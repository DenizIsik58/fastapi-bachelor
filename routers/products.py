from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse

from database.mongo import get_collection, insert_to_collection, get_count_items, get_single_item, \
    get_all_items_from_collection
from models.product import Product

products_router = APIRouter()


# TODO: protect this endpoint
@products_router.post("/add")
async def add_product(product: Product = Body(...)):
    collection = get_collection("products")

    if get_count_items(collection, "name", product.name) > 0:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This bag already exists!")

    new_product = insert_to_collection(collection, jsonable_encoder(product))
    created_product = get_single_item(collection, "_id", new_product.inserted_id)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_product)


# TODO: protet this endpoint
@products_router.get("/")
async def get_all_products():
    # Return all products from the database
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=get_all_items_from_collection(get_collection("products")))


# TODO: Should we remove products?
"""
@products_router.delete("/products/remove/{id}")
async def remove_product():
    # Remove a products from the database
    database.delete_from_collection("products", id)
    raise HTTPException(status_code=400, detail="Not implemented yet!")
"""
