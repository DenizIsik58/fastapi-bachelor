import datetime
import json
from typing import List

from fastapi import APIRouter, Depends, Body, HTTPException
from starlette import status
from starlette.responses import JSONResponse
from base_models.purchase import BasePurchases, BasePurchase
from database_schemas.product import ProductDocument
from database_schemas.purchase import Purchase, PurchaseDocuments
from database_schemas.user import UserDocument
from routers.authentication import get_current_user
from util.json_manager import serialize_models

purchase_router = APIRouter()


@purchase_router.get("/")
async def get_purchases(current_user=Depends(get_current_user)):
    user_id = UserDocument.objects(username=current_user).first().id
    purchases = [json.loads(purchase.to_json()) for purchase in PurchaseDocuments.objects(user_id=user_id)]
    if len(purchases) == 0:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "No purchases found"})
    return JSONResponse(status_code=status.HTTP_200_OK, content=purchases)


@purchase_router.post("/purchase")
async def purchase_products(purchases: List[BasePurchase] = Body(...), current_user=Depends(get_current_user)):
    user_id = UserDocument.objects(username=current_user).first().id

    purchases_saved = []
    for purchase in purchases:
        product = ProductDocument.objects(id=purchase.product_id).first()
        if product is None:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This product does not exist!")

        purchases_saved.append(Purchase(product_id=purchase.product_id, quantity=purchase.quantity, price=product.price,
                                  total=purchase.total, date=datetime.datetime.now()))

    if PurchaseDocuments.objects(user_id=user_id).count() == 0:
        purchase_documents = PurchaseDocuments(user_id=user_id, purchases=purchases_saved).save()
    else:
        purchase_documents = PurchaseDocuments.objects(user_id=user_id).first()
        purchase_documents.update(purchases=purchases)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=serialize_models(purchase_documents))