from util.json_manager import to_json

from fastapi import APIRouter, Body, HTTPException
from starlette import status
from starlette.responses import JSONResponse
from database_schemas.product import ProductDocument
from base_models.product import BaseProduct


products_router = APIRouter()


# TODO: Do we need protection?
@products_router.post("/products/add")
async def add_product(product: BaseProduct = Body(...)):
    if ProductDocument.objects(name=product.name).count() > 0:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This bag already exists!"
        )

    new_product = ProductDocument(
        name=product.name,
        price=product.price,
        long_description=product.long_description,
        image_url=product.image_url,
        short_description=product.short_description
    ).save()

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=to_json(new_product, singular=True)
    )


@products_router.get("/products")
async def get_all_products():
    """
    Get all products from the database
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=to_json(ProductDocument.objects(), singular=False)
    )


@products_router.get("/frontpage-products")
async def get_first_6_products():
    """
    Get the first 6 products from the database
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=to_json(ProductDocument.objects[:6], singular=False)
    )


@products_router.get("/products/{_id}")
async def get_product_by_id(_id):
    if ProductDocument.objects(id=_id).count() == 0:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This product does not exist!"
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=to_json(ProductDocument.objects(id=_id).first(), singular=True)
    )
