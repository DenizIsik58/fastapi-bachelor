from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT

authentication_router = APIRouter()

@authentication_router.post('/refresh')
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
    return {"access_token": new_access_token}
