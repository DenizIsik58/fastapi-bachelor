import json
from datetime import datetime

from fastapi import APIRouter, Body, HTTPException, Depends
from starlette import status
from starlette.responses import JSONResponse

from base_models.review import Review
from database_schemas.product import ProductDocument
from database_schemas.review import ReviewDocument
from routers.authentication import get_current_user

reviews_router = APIRouter()

## PROTECTED ENDPOINT
@reviews_router.post("/products/reviews/add")
async def add_review(review: Review = Body(...), current_user=Depends(get_current_user)):
    product = ProductDocument.objects(id=review.product_id).first()

    if product is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This product does not exist!")

    if review.rating > 5 or review.rating < 1:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Rating must be between 1 and 5!")

    new_review = ReviewDocument(rater=current_user, rating=review.rating, comment=review.comment, product_id=review.product_id, timestamp=datetime.now()).save()

    created_review = new_review.to_json()

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=json.loads(created_review))


## PROTECTED ENDPOINT
@reviews_router.get("/products/reviews/{product_id}")
async def get_all_reviews(product_id, current_user=Depends(get_current_user)):
    # Return all reviews from the database
    if ProductDocument.objects(id=product_id).count() == 0:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This product does not exist!")

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=[json.loads(review.to_json()) for review in ReviewDocument.objects(product_id=product_id)])
