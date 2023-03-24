from fastapi import APIRouter, Body, HTTPException, Depends, Header
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from starlette import status
from starlette.responses import JSONResponse
from database.mongo import get_collection, get_single_item, get_all_reviews_by_product_name
from models.review import Review
from routers.authentication import get_current_user

reviews_router = APIRouter()

## PROTECTED ENDPOINT
@reviews_router.post("/add")
async def add_review(review: Review = Body(...), current_user=Depends(get_current_user)):
    review.rater = current_user

    collection = get_collection("products")

    user = get_single_item(get_collection("users"), "username", review.rater)
    if user is None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This user does not exist!")

    # product = get_single_item(collection, "name", review.product_name)
    updated_result = collection.update_one({"name": review.product_name}, {"$push": {"reviews": review.dict()}})

    if updated_result.modified_count == 0:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This product does not exist!")

    if review.rating > 5 or review.rating < 1:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Rating must be between 1 and 5!")

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(review))


## PROTECTED ENDPOINT
@reviews_router.get("/{product_name}")
async def get_all_reviews(product_name: str, current_user=Depends(get_current_user)):
    # Return all reviews from the database
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=get_all_reviews_by_product_name(product_name=product_name))
