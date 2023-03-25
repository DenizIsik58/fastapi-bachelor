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

    new_product = ProductDocument(name=product.name, price=product.price, description=product.description).save()
    created_product = ProductDocument.objects(id=new_product.id).to_json()

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=json.loads(created_product))


# TODO: protet this endpoint
@products_router.get("/")
async def get_all_products():
    # Return all products from the database
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=([json.loads(product.to_json()) for product in ProductDocument.objects()]))
@products_router.get("/{_id}")
async def get_product_by_name(_id):
    if ProductDocument.objects(id=_id).count() == 0:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This product does not exist!")

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=json.loads(ProductDocument.objects(id=_id).first().to_json()))

