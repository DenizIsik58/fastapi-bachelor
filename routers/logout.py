from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from routers.authentication import get_current_user

logout_router = APIRouter()
@logout_router.get("/logout")
async def logout(current_user=Depends(get_current_user), Authorize: AuthJWT = Depends()):
    Authorize.unset_jwt_cookies()
    Authorize.unset_access_cookies()
    Authorize.unset_refresh_cookies()

    return {"message": "Successfully logged out!"}