from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from starlette.responses import JSONResponse

from base_models.token import Access_Token

authentication_router = APIRouter()


@authentication_router.post('/refresh', response_model=Access_Token)
def refresh(Authorize: AuthJWT = Depends()):
    """
    The jwt_refresh_token_required() function ensures a valid refresh
    token is present in the request before running any code below that function.
    we can use the get_jwt_subject() function to get the subject of the refresh
    token, and use the create_access_token() function again to make a new access token
    """
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    return JSONResponse(status_code=200, content=Access_Token(access_token=new_access_token).json())


# In case we need to fetch the user for protected endpoints
async def get_current_user(Authorize: AuthJWT = Depends()):
    try:
        # This will ensure that the endpoint is protected
        Authorize.jwt_required()

        # access_token is the JWT token sent in the "access_token" header
        current_user = Authorize.get_jwt_subject()
        return current_user
    except AuthJWTException:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
