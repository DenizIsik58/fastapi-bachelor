import random
from datetime import datetime
from util.json_manager import to_json

from fastapi import APIRouter, Depends, Body, HTTPException
from starlette import status
from starlette.responses import JSONResponse

from base_models.purchase import BasePurchase
from database_schemas.product import ProductDocument
from database_schemas.purchase import Purchase, PurchaseDocument
from database_schemas.user import UserDocument
from routers.authentication import get_current_user

purchase_router = APIRouter()


@purchase_router.get("/purchases")
async def get_purchases(current_user=Depends(get_current_user)):
    user_id = UserDocument.objects(username=current_user).first().id

    purchases = to_json(
        PurchaseDocument.objects(user_id=user_id),
        singular=False
    )

    return purchases


@purchase_router.post("/purchase")
async def purchase_products(purchases: BasePurchase = Body(...), current_user=Depends(get_current_user)):
    user_id = UserDocument.objects(username=current_user).first().id

    purchases_saved = []
    images = []

    for purchase in purchases.items:
        product = ProductDocument.objects(id=purchase.product_id).first()

        if product is None:
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The product with id {purchase.product_id} doesn't exists!"
            )

        images.append(product.image_url)
        purchases_saved.append(Purchase(
            product_id=product.id,
            quantity=purchase.quantity,
            price=product.price
        ))

    image = random.choice(images)

    new_purchase = PurchaseDocument(
        user_id=user_id,
        purchase_date=datetime.now(),
        items=purchases_saved,
        image_url=image
    ).save()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=to_json(new_purchase.to_json(), singular=True)
    )
