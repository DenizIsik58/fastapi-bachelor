from datetime import datetime
from fastapi import APIRouter, Body, HTTPException, Depends
from starlette import status
from starlette.responses import JSONResponse
from base_models.review import Review
from database_schemas.product import ProductDocument
from database_schemas.review import ReviewDocument
from routers.authentication import get_current_user
from util.authentication_manager import get_user

reviews_router = APIRouter()

## PROTECTED ENDPOINT
@reviews_router.post("/add")
async def add_review(review: Review = Body(...), current_user=Depends(get_current_user)):
    review.rater = current_user
    review.timestamp = datetime.now()

    user = get_user(review.rater)
    if user is None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This user does not exist!")

    product = ProductDocument.objects(name=review.product_name).first()
    if product is None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This product does not exist!")

    if review.rating > 5 or review.rating < 1:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Rating must be between 1 and 5!")

    new_review = ReviewDocument(rater=review.rater, rating=review.rating, comment=review.comment, product_name=review.product_name, timestamp=review.timestamp)
    product.update(push__reviews=new_review)
    product.reload()

    created_review = ProductDocument.objects(name=review.product_name).first().reviews[-1].to_json()

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_review)


## PROTECTED ENDPOINT
@reviews_router.get("/{product_name}")
async def get_all_reviews(product_name: str, current_user=Depends(get_current_user)):
    # Return all reviews from the database
    if ProductDocument.objects(name=product_name).count() == 0:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This product does not exist!")

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=[review.to_json() for review in ProductDocument.objects(name=product_name).first().reviews])
