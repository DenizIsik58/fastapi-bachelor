import random
from datetime import datetime
from util.json_manager import to_json, to_json_purchases
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
    purchases = PurchaseDocument.objects(user_id=user_id)

    purchases = to_json_purchases(
        purchases,
        singular=False
    )

    return purchases


@purchase_router.get("/purchases/{purchase_id}")
async def get_purchase(purchase_id: str, current_user=Depends(get_current_user)):
    user_id = UserDocument.objects(username=current_user).first().id
    purchase = to_json_purchases(
        PurchaseDocument.objects(user_id=user_id, id=purchase_id).first(),
        singular=True
    )

    return purchase


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

        if purchase.quantity == 0:
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The quantity of the product must be greater than 0!"
            )

        images.append(product.image_url)

        purchases_saved.append(Purchase(
            product_id=product.id,
            quantity=purchase.quantity,
            price=product.price,
            name=product.name
        ))

        for purchase in purchases_saved:
            print(purchase.quantity)

    image = random.choice(images)

    new_purchase = PurchaseDocument(
        user_id=user_id,
        purchase_date=datetime.now(),
        items=purchases_saved,
        image_url=image
    ).save()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=to_json_purchases(new_purchase, singular=True)
    )
