from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse
from database.mongo import get_collection
from models.product import Product
from util.json_manager import serialize_models

products_router = APIRouter()


# TODO: protect this endpoint
@products_router.post("/add")
async def add_product(product: Product = Body(...)):
    # Remove a product from the database
    if get_collection("products").count_documents({"name": product.name}) > 0:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This bag already exists!")

    new_product = get_collection("products").insert_one(jsonable_encoder(product))
    created_product = get_collection("products").find_one({"_id": new_product.inserted_id})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=serialize_models(created_product))


# TODO: protet this endpoint
@products_router.get("/")
async def get_all_products():
    # Return all products from the database
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=list(serialize_models(get_collection("products").find({}))))


# TODO: Should we remove products?
"""
@products_router.delete("/products/remove/{id}")
async def remove_product():
    # Remove a products from the database
    database.delete_from_collection("products", id)
    raise HTTPException(status_code=400, detail="Not implemented yet!")
"""
