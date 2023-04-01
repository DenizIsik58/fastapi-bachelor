from util.json_manager import to_json
from datetime import datetime

from fastapi import APIRouter, Body, Depends
from starlette import status
from starlette.responses import JSONResponse

from base_models.review import Review
from database_schemas.product import ProductDocument
from database_schemas.review import ReviewDocument
from routers.authentication import get_current_user

reviews_router = APIRouter()


@reviews_router.post("/products/reviews/add")
async def add_review(review: Review = Body(...), current_user=Depends(get_current_user)):
    product = ProductDocument.objects(id=review.product_id).first()

    if product is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": "PRODUCT_NOT_FOUND",
                "message": f"No product was found with the given ID {review.product_id}!"
            }
        )

    if review.rating > 5 or review.rating < 1:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "INVALID_RATING",
                "message": "The rating must be between 1 and 5!"
            }
        )

    new_review = ReviewDocument(
        rater=current_user,
        rating=review.rating,
        comment=review.comment,
        product_id=review.product_id,
        timestamp=datetime.now()
    ).save()

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=to_json(new_review, singular=True)
    )


# PROTECTED ENDPOINT
@reviews_router.get("/products/reviews/{product_id}")
async def get_all_reviews(product_id):
    """
    Return all reviews for the given product
    """
    if not ProductDocument.objects(id=product_id).count():
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "PRODUCT_NOT_FOUND",
                "message": f"No product was found with the given ID {product_id}!"
            }
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=to_json(
            ReviewDocument.objects(product_id=product_id),
            singular=False
        )
    )
